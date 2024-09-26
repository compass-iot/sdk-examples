from client import create_gateway_client, get_enum_str

import grpc
import compassiot.gateway.v1.gateway_pb2_grpc as gateway
import compassiot.compass.v1.time_pb2 as time
import compassiot.platform.v1.streaming_pb2 as streaming


def main():
    client = create_gateway_client()

    request = streaming.RealtimeTrajectoryByPath(
        linestring_wkt="LINESTRING (151.188277 -33.884699, 151.18862 -33.884707, 151.189805 -33.884734, 151.190091 -33.884743, 151.19063 -33.884758, 151.190909 -33.884747, 151.191247 -33.884724, 151.191281 -33.884723, 151.191439 -33.88471, 151.191552 -33.884699, 151.191722 -33.884682, 151.192145 -33.884643, 151.192449 -33.884608)",
    )

    for response in client.RealtimeTrajectoryByPath(request):
        ## helper to print enum objects
        # print("Vehicle Type:", get_enum_str(response, streaming.ProcessedPoint.VEHICLE_TYPE_FIELD_NUMBER, response.vehicle_type))
        print(response)


if __name__ == "__main__":
    main()
