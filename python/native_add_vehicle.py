from client import create_gateway_client
import compassiot.native.v1.native_pb2 as native


def main():
    client = create_gateway_client()

    request = native.AddVehicleRequest(
        provider_auth=native.AuthRequest(
            tesla=native.TeslaAuth(
                vin=""
            )
        )
    )

    response = client.NativeAddVehicle(request)

    print(response.message, response.add_vehicle_status)

     
if __name__ == "__main__":
    main()
