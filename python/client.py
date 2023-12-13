import asyncio
import inspect
import requests
from typing import Any, Callable

from grpc import ClientCallDetails, RpcError, UnaryUnaryClientInterceptor, intercept_channel, secure_channel, ssl_channel_credentials
from grpc_interceptor.client import ClientInterceptor, ClientCallDetails

from compassiot.gateway.v1.gateway_pb2 import AuthenticateRequest
from compassiot.gateway.v1.gateway_pb2_grpc import ServiceStub


HOST = "beta.api.compassiot.cloud"
SECRET = "__INSERT_YOUR_COMPASSIOT_API_KEY__"


def create_gateway_client() -> ServiceStub:
	# UnaryRestInterceptor must be last as it's the layer which makes the API call,
	# unlike AccessTokenInterceptor which just populates the header
	interceptors = [AccessTokenInterceptor(HOST, SECRET), UnaryRestInterceptor(HOST)]
	channel = secure_channel(HOST, ssl_channel_credentials())
	channel = intercept_channel(channel, *interceptors)
	return ServiceStub(channel)


class UnaryRestInterceptor(UnaryUnaryClientInterceptor):
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
			stub_method_tuples = list(filter(lambda member: not member[0].startswith("__"), inspect.getmembers(mock_service)))
			map = {}
			for (k, v) in stub_method_tuples:
				map[k] = v._response_deserializer
			return map

	def __init__(self, host: str):
		self.host = host
		self.deserializer_map = self._build_deserializer_map()

	def _call_rest(self, request: Any, call_details: ClientCallDetails):
		url = "https://%s/%s" % (self.host, call_details.method.strip("/"))

		# Copy headers
		headers = self._HTTP_HEADERS.copy()
		if call_details.metadata is not None:
			for (k, v) in call_details.metadata:
				headers[k] = v

		# Make request & deserialize it
		response = requests.post(url, data=request.SerializeToString(True), headers=headers, auth=call_details.credentials)
		response.raise_for_status()

		# Wrap into future
		rpc = call_details.method.split("/")[-1]
		deserializer = self.deserializer_map[rpc]
		future = asyncio.get_event_loop().create_future()
		future.set_result(deserializer(response.content))
		return future

	def intercept_unary_unary(self, next, call_details: ClientCallDetails, request: Any):
		return self._call_rest(request, call_details)	


class AccessTokenInterceptor(ClientInterceptor):
	def __init__(self, host: str, secret: str) -> None:
		self.host = host
		self.secret = secret

		interceptors = [UnaryRestInterceptor(host)]
		with intercept_channel(secure_channel(host, ssl_channel_credentials()), *interceptors) as channel:
			service = ServiceStub(channel)
			response = service.Authenticate(AuthenticateRequest(token=secret))
			self.access_token = response.access_token			

	@staticmethod
	def _create_details_with_auth(call_details: ClientCallDetails, access_token: str) -> ClientCallDetails:
		return ClientCallDetails(
			call_details.method,
			call_details.timeout,
			[("authorization", "Bearer %s" % (access_token))],
			call_details.credentials,
			call_details.wait_for_ready,
			call_details.compression,
		)
	
	def intercept(self, method: Callable[..., Any], request_or_iterator: Any, call_details: ClientCallDetails):
		try:
			return method(request_or_iterator, self._create_details_with_auth(call_details, self.access_token))
		except RpcError as error:
			print("Error: ", error)
