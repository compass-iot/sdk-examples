import requests

from google.protobuf.message import Message
from google.protobuf.empty_pb2 import Empty

from compassiot.gateway.v1.gateway_pb2 import AuthenticateRequest, AuthenticateResponse
from compassiot.location.v1.location_pb2 import ReverseGeocodeRequest, ReverseGeocodeResponse
from compassiot.native.v1.native_pb2 import GetVehiclesResponse
from client import HOST, SECRET


METHOD_PREFIX = "/compassiot.gateway.v1.Service"
HTTP_HEADERS = {"content-type": "application/proto"}


def call_unary(host: str, secret: str, method: str, request: Message):
	# Get access token first
	auth_url = "https://%s/%s/%s" % (host, METHOD_PREFIX, "Authenticate")
	auth_req = AuthenticateRequest(token=secret).SerializeToString(True)
	auth_future = requests.post(auth_url, data=auth_req, headers=HTTP_HEADERS)
	auth_res = AuthenticateResponse.FromString(auth_future.content)

	# Attach access token to header
	headers = HTTP_HEADERS.copy()
	headers["Authorization"] = "Bearer %s" % auth_res.access_token

	url = "https://%s/%s/%s" % (host, METHOD_PREFIX, method.strip("/"))
	response = requests.post(url, data=request.SerializeToString(True), headers=headers)
	return response.content


def main():
	request = ReverseGeocodeRequest(polygon_wkt="POLYGON ((151.3614711724905 -33.42188098251515, 151.34152608798246 -33.4171079590409, 151.3416655640977 -33.402554438990045, 151.36216855306685 -33.39603367115148, 151.37974254361256 -33.41151969574161, 151.3614711724905 -33.42188098251515))")
	bytes = call_unary(HOST, SECRET, "ReverseGeocode", request)
	response = ReverseGeocodeResponse.FromString(bytes)
	print("ReverseGeocode:")
	print(response.name)
	print()

	request = Empty()
	bytes = call_unary(HOST, SECRET, "NativeGetVehicles", request)
	response = GetVehiclesResponse.FromString(bytes)
	print("NativeGetVehicles:")
	print(response.provider_get)

if __name__ == "__main__":
  main()
