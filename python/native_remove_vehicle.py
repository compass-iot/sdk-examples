from client import create_gateway_client
import compassiot.native.v1.native_pb2 as native


def main():
    client = create_gateway_client()

    request = native.RemoveVehicleRequest(
        vins=[]
    )

    # Returns empty, check using NativeGetVehicles
    client.NativeRemoveVehicle(request)

     
if __name__ == "__main__":
    main()
