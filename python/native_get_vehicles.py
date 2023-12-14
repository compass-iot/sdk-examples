from client import create_gateway_client
from google.protobuf.empty_pb2 import Empty


def main():
    client = create_gateway_client()
    request = Empty()
    response = client.NativeGetVehicles(request)
    print(response.provider_get)

     
if __name__ == "__main__":
    main()
