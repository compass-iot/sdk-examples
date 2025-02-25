import asyncio
import inspect
import time

from dataclasses import dataclass
from typing import Any, Callable, Generator, Optional, Tuple, Union
from collections import deque
from functools import wraps

from google.protobuf.internal.well_known_types import Timestamp
import requests
from grpc import (
    RpcError,
    StatusCode,
    intercept_channel,
    secure_channel,
    ssl_channel_credentials,
)
import grpc
from grpc_interceptor.client import ClientCallDetails, ClientInterceptor

from compassiot.gateway.v1.gateway_pb2 import AuthenticateRequest
from compassiot.gateway.v1.gateway_pb2_grpc import ServiceStub

# Supply your client secret
SECRET = "---Your Secret Here---"


class UnaryRestInterceptor(grpc.UnaryUnaryClientInterceptor):
    """
    Shim to convert unary gRPC calls to pure REST, due to several suspected regressions in
    core gRPC library:
    - https://github.com/grpc/grpc/issues/29706
    - https://github.com/grpc/grpc/issues/33935
    """

    _HTTP_HEADERS = {"content-type": "application/proto"}

    @staticmethod
    def _build_deserializer_map():
        with secure_channel("mock", ssl_channel_credentials()) as channel:
            mock_service = ServiceStub(channel)
            stub_method_tuples = list(
                filter(
                    lambda member: not member[0].startswith("__"),
                    inspect.getmembers(mock_service),
                )
            )
            map = {}
            for k, v in stub_method_tuples:
                map[k] = v._response_deserializer
            return map

    @staticmethod
    def _cast_grpc_error(response: requests.Response):
        has_error = False
        error = RpcError()
        if response.status_code >= 200 and response.status_code < 300:
            has_error = False
        if response.status_code == 400:
            error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
            has_error = True
        if response.status_code == 401:
            error.code = lambda: grpc.StatusCode.UNAUTHENTICATED
            has_error = True
        if response.status_code == 403:
            error.code = lambda: grpc.StatusCode.PERMISSION_DENIED
            has_error = True
        if response.status_code == 404:
            error.code = lambda: grpc.StatusCode.NOT_FOUND
            has_error = True
        if response.status_code == 412:
            error.code = lambda: grpc.StatusCode.FAILED_PRECONDITION
            has_error = True
        if response.status_code == 429:
            error.code = lambda: grpc.StatusCode.RESOURCE_EXHAUSTED
            has_error = True
        if response.status_code >= 500:
            error.code = lambda: grpc.StatusCode.INTERNAL
            has_error = True

        if has_error is True:
            error.details = lambda: response.content.decode()
            return error
        else:
            return None

    def __init__(self, host: str):
        self.host = host
        self.deserializer_map = self._build_deserializer_map()

    def _call_rest(self, request: Any, call_details: ClientCallDetails):
        url = "https://%s/%s" % (self.host, call_details.method.strip("/"))

        # Copy headers
        headers = self._HTTP_HEADERS.copy()
        if call_details.metadata is not None:
            for k, v in call_details.metadata:
                headers[k] = str(v)

        # Create future
        future = asyncio.get_event_loop().create_future()

        # Make request & deserialize it
        response = requests.post(
            url, data=request.SerializeToString(True), headers=headers
        )
        error = self._cast_grpc_error(response)
        if error is not None:
            future.set_exception(error)
        else:
            rpc = call_details.method.split("/")[-1]
            deserializer = self.deserializer_map[rpc]
            future.set_result(deserializer(response.content))
        return future

    def intercept_unary_unary(
        self, next, call_details: ClientCallDetails, request: Any
    ):
        return self._call_rest(request, call_details)


class AccessTokenInterceptor(ClientInterceptor):
    def __init__(self, host: str, secret: str) -> None:
        self.host = host
        self.secret = secret
        self.access_token = self._get_access_token(host, secret)

    def access_header(self) -> Tuple[str, str]:
        return ("authorization", "Bearer %s" % (self.access_token))

    @staticmethod
    def _get_access_token(host: str, secret: str) -> str:
        interceptors = [UnaryRestInterceptor(host)]
        with intercept_channel(
            secure_channel(host, ssl_channel_credentials()), *interceptors
        ) as channel:
            service = ServiceStub(channel)
            response = service.Authenticate(AuthenticateRequest(token=secret))
            return response.access_token

    def __call_details(
        self, call_details: grpc.ClientCallDetails
    ) -> grpc.ClientCallDetails:
        headers = []

        # Create headers
        headers.extend(call_details.metadata if call_details.metadata else [])
        headers.append(self.access_header())

        return call_details._replace(metadata=headers)

    def intercept(
        self,
        method: Callable[..., Any],
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ):
        try:
            return method(request_or_iterator, self.__call_details(call_details))
        except RpcError as error:
            if error.code == grpc.StatusCode.UNAUTHENTICATED:
                print("Access token expired, refreshing...")
                self.access_token = self._get_access_token(self.host, self.secret)
                return method(
                    request_or_iterator,
                    self.__call_details(call_details),
                )
            else:
                print("Didn't detect anything, finishing...")
                raise error


class StreamUtils:
    StreamError = str
    InternalMessage = str

    @dataclass
    class Update[T]:
        value: T
        timestamp: float
        data_rate: float

    @dataclass
    class Internal:
        message: str
        error: Optional[RpcError]

    @dataclass
    class Finished:
        error: Optional[RpcError]
        pass


type StreamUpdate[T] = Union[
    StreamUtils.Update[T], StreamUtils.Internal, StreamUtils.Finished
]


class RoadIntelligenceClient(ServiceStub):
    TIMEOUT_MS = (
        1000 * 60 * 4.5
    )  # 4.5 minutes. 30s below the 5 minute upstream timeout.

    secret: str
    host: str
    client: ServiceStub

    def __init__(self, secret: str, host="api.compassiot.cloud"):
        self.secret = secret
        self.host = host
        self.client = self.__create_stub()

    def __create_stub(self):
        assert self.host is not None
        assert self.secret is not None

        # UnaryRestInterceptor must be last as it's the layer which makes the API call,
        # unlike AccessTokenInterceptor which just populates the header
        interceptors = [
            AccessTokenInterceptor(self.host, self.secret),
        ]

        # Create an SSL connection to the host with the appropriate interceptors
        channel = secure_channel(self.host, ssl_channel_credentials())
        channel = intercept_channel(channel, *interceptors)

        return ServiceStub(channel)

    def __getattr__(self, name):
        # If the attribute exists in self.client, return it
        attr = getattr(self.client, name, None)
        if attr is not None and callable(attr):  # Ensure we only wrap methods
            return self.__wrap_method(name, attr)
        return attr

    def __wrap_method(self, name: str, method: Any):
        if name in self.__method_shims__():
            return self.__method_shims__()[name](method)
        return method  # Default passthrough

    def __method_shims__(self):
        """Defines custom wrappers for specific methods."""
        return {
            # Pickup
            "ProcessedPointByGeometry": self.__with_pickup__,
            # Retry
            "RealtimeRawPointByGeometry": self.__with_retry__,
            "RealtimeTrajectoryByPathRequest": self.__with_retry__,
        }

    def __with_pickup__(self, func: grpc.UnaryStreamMultiCallable):
        """Example wrapper to pick up a function's output."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.__masked_pickup__(func, *args, **kwargs)

        return wrapper

    def __masked_pickup__[Req, Res](
        self, stream: grpc.UnaryStreamMultiCallable, request: Req
    ) -> Generator[Res, None]:
        generator = self.__pickup_stream__(stream, request)

        for item in generator:
            yield item
            # match item:
            #     case StreamUtils.Update(value):
            #         yield value
            #     case _:
            #         pass

    """
    Applies "pickup" logic to a stream in order to prevent the stream from being closed by external measures.
    This involves storing the timestamp last returned, and reinitializing the stream with this last timestamp.
    """

    def __pickup_stream__[Req, Res](
        self, stream: grpc.UnaryStreamMultiCallable, request: Req
    ) -> Generator[StreamUpdate[Res], None]:
        # Do not initially provide a "last_received_timestamp"
        generator = stream(request, timeout=RoadIntelligenceClient.TIMEOUT_MS)

        timestamps = deque()
        window = 60

        last_recieved: Timestamp | None = None

        while True:
            try:
                # Consume generator as usual, return each item.
                for item in generator:
                    # Assign the timestamp as we obtain it
                    last_recieved = item.timestamp

                    now = time.time()
                    timestamps.append(now)

                    while timestamps and timestamps[0] < now - window:
                        timestamps.popleft()

                    data_rate = len(timestamps) / window
                    yield StreamUtils.Update(item, data_rate=data_rate, timestamp=now)
            except RpcError as error:
                refresh_codes = [
                    StatusCode.DEADLINE_EXCEEDED,
                    StatusCode.UNAVAILABLE,
                    StatusCode.INTERNAL,
                ]
                err_code = error.code()

                if err_code in refresh_codes:
                    # If the server is requesting a restart, or encounters a network error, do so.
                    # Here, we provide the timestamp labelled on the last recieved point so we can
                    # determine where to restart from.
                    #
                    # Note: This **must** be present on any value being shimmed with pickup logic.
                    if last_recieved:
                        request.last_received_timestamp = last_recieved.ToDatetime()

                    generator = stream(request)
                    yield StreamUtils.Internal("Reconnecting to stream.", error)
                else:
                    yield StreamUtils.Finished(error=error)
                    break

    def __with_retry__(self, func: grpc.UnaryStreamMultiCallable):
        """Example wrapper to retry a function on failure."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.__masked_retry__(func, *args, **kwargs)

        return wrapper

    def __masked_retry__[Req, Res](
        self, stream: grpc.UnaryStreamMultiCallable, request: Req
    ) -> Generator[Res, None]:
        generator = self.__retry_stream__(stream, request)

        for item in generator:
            match item:
                case StreamUtils.Update(value):
                    yield value
                case _:
                    pass

    """
    Applies "retry" logic to a stream in order to reconnect to the stream on failure. This does not involve
    checks or balances in terms of applying or tagging requests with metadata, but rather simply reconnects.
    """

    def __retry_stream__[Req, Res](
        self, stream: grpc.UnaryStreamMultiCallable, request: Req
    ) -> Generator[StreamUpdate[Res], None]:
        generator = stream(request, timeout=RoadIntelligenceClient.TIMEOUT_MS)

        timestamps = deque()
        window = 60

        while True:
            try:
                # Consume generator as usual, return each item.
                for item in generator:
                    now = time.time()
                    timestamps.append(now)

                    while timestamps and timestamps[0] < now - window:
                        timestamps.popleft()

                    data_rate = len(timestamps) / window
                    yield StreamUtils.Update(item, data_rate=data_rate, timestamp=now)
            except RpcError as error:
                refresh_codes = [
                    StatusCode.DEADLINE_EXCEEDED,
                    StatusCode.UNAVAILABLE,
                    StatusCode.INTERNAL,
                ]
                err_code = error.code()

                if err_code in refresh_codes:
                    # If the server is requesting a restart, or encounters a network error, do so.
                    generator = stream(request)
                    yield StreamUtils.Internal("Reconnecting to stream.", error)
                else:
                    yield StreamUtils.Finished(error=error)
                    break


### Debug Retry Mechanism
#
# print("Begining ingestion...")
# request = native.RealtimeRawPointByVinsRequest(vins=vins, max_staleness_minutes=7)
#
# generator = client.RealtimeRawPointByVins(request)
#
# for position in generator:
#     data_rate = 0
#     formatted_time = "Now"
#
#     print(position)
#
#     match position:
#         case StreamUtils.Update(_, data_rate=dr, timestamp=t):
#             formatted_time = datetime.fromtimestamp(t).strftime("%H:%M:%S")
#             data_rate=dr
#         case StreamUtils.Internal(message, error):
#             print(f"\nReceived internal update: {message}\n", error)
#         case StreamUtils.Finished(error):
#             if error is not None:
#                 print(f"\nStream finished with error: {error}", error.trailing_metadata())
#             else:
#                 print("\nStream finished successfully.\n")
#
#     # Print progress dynamically (overwriting the same line)
#     sys.stdout.write(f"\rData Rate: {data_rate:.2f} points/sec. Time: {formatted_time}")
#     sys.stdout.flush()
#
# print("\nDone.")
