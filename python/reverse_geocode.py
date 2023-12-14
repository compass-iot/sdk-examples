from client import create_gateway_client
import compassiot.location.v1.location_pb2 as location


def main():
    client = create_gateway_client()

    request = location.ReverseGeocodeRequest(
        polygon_wkt="POLYGON ((151.21229795582838 -33.89101682624773, 151.19573365832508 -33.87414013405557, 151.20665103622446 -33.858041660571004, 151.22490940960853 -33.870545592545284, 151.21229795582838 -33.89101682624773))"
    )

    response = client.ReverseGeocode(request)

    print(response.name)


if __name__ == "__main__":
    main()
