from google.protobuf.empty_pb2 import Empty
from client import create_gateway_client


def main():
    client = create_gateway_client()
    request = Empty()
    response = client.NativeGetVehicles(request)
    print(response)

     
if __name__ == "__main__":
    main()
