from client import create_gateway_client
import compassiot.native.v1.native_pb2 as native


def main():
    client = create_gateway_client()

    request = native.UpdateVehicleRequest(
        provider_auth=native.AuthRequest(
            tesla=native.TeslaAuth(
                vin=""
            )
        )
    )

    # Returns empty, check using NativeGetLatestPoint
    client.NativeUpdateVehicle(request)

     
if __name__ == "__main__":
    main()
