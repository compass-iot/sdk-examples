from google.protobuf.empty_pb2 import Empty

from compassiot.location.v1.location_pb2 import ReverseGeocodeRequest
from client import create_gateway_client


def main():
	client = create_gateway_client()

	request = ReverseGeocodeRequest(polygon_wkt="POLYGON ((151.3614711724905 -33.42188098251515, 151.34152608798246 -33.4171079590409, 151.3416655640977 -33.402554438990045, 151.36216855306685 -33.39603367115148, 151.37974254361256 -33.41151969574161, 151.3614711724905 -33.42188098251515))")
	response = client.ReverseGeocode(request)
	print("ReverseGeocode:")
	print(response.name)
	print()

	request = Empty()
	response = client.NativeGetVehicles(request)
	print("NativeGetVehicles:")
	print(response.provider_get)


if __name__ == "__main__":
	main()
