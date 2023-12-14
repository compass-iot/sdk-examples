from client import create_gateway_client
import compassiot.native.v1.native_pb2 as native


def main():
    client = create_gateway_client()

    request = native.GetLatestPointRequest(
        vin=""
    )

    response = client.NativeGetLatestPoint(request)

    print(response.event)

     
if __name__ == "__main__":
    main()
