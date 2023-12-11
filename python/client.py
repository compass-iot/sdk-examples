from typing import Any, Callable

from grpc import ClientCallDetails, RpcError, intercept_channel, secure_channel, ssl_channel_credentials
from grpc_interceptor.client import ClientInterceptor, ClientCallDetails, ClientInterceptorReturnType

from compassiot.gateway.v1.gateway_pb2 import AuthenticateRequest
from compassiot.gateway.v1.gateway_pb2_grpc import ServiceStub


HOST = "beta.api.compassiot.cloud"
SECRET = "__insert_your_api_key__"


def create_gateway_client() -> ServiceStub:
	interceptors = [AccessTokenInterceptor(HOST, SECRET)]
	channel = secure_channel(HOST, ssl_channel_credentials())
	channel = intercept_channel(channel, *interceptors)
	return ServiceStub(channel)


class AccessTokenInterceptor(ClientInterceptor):
	def __init__(self, host: str, secret: str) -> None:
		channel = secure_channel(host, ssl_channel_credentials())
		service = ServiceStub(channel)
		self.access_token = service.Authenticate(AuthenticateRequest(token=secret)).access_token
		self.host = host
		self.secret = secret

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
	
	def intercept(self, method: Callable[..., Any], request_or_iterator: Any, call_details: ClientCallDetails) -> ClientInterceptorReturnType:
		try:
			return method(request_or_iterator, self._create_details_with_auth(call_details, self.access_token))
		except RpcError as error:
			print("Error: ", error)
