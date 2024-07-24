from client import create_gateway_client, get_enum_str

import grpc
import compassiot.gateway.v1.gateway_pb2_grpc as gateway
import compassiot.compass.v1.time_pb2 as time
import compassiot.platform.v1.streaming_pb2 as streaming


def paginate_processed_point(client: gateway.ServiceStub, req: streaming.ProcessedPointByGeometryRequest):
    stream = client.ProcessedPointByGeometry(req)
    while True:
        try:
            for response in stream:
                req.last_received_timestamp.CopyFrom(response.timestamp)
                yield response
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                print("DeadlineExceed, retrying")
                stream = client.ProcessedPointByGeometry(req)
                continue
            else:
                raise e
        break


def main():
    client = create_gateway_client()

    request = streaming.ProcessedPointByGeometryRequest(
        linestring_or_polygon_wkt="POLYGON ((151.116490002445 -34.136652437446564, 150.76133775468065 -33.970878990313345,150.8238645588653 -33.68832143811975, 150.93391173422782 -33.51542003355166, 151.17151359012706 -33.594622738528074, 151.3165757758332 -33.67583417052261, 151.3115736314981 -33.80478175152794, 151.22903824997502 -34.03515466768564, 151.116490002445 -34.136652437446564))",
        date_time_range= time.DateTimeRange(
            start=time.LocalDate(
                day=1,
                month=10,
                year=2023
            ),
            end=time.LocalDate(
                day=31,
                month=10,
                year=2023
            ),
            day_of_week=[
                time.DayOfWeek.SATURDAY,
                time.DayOfWeek.SUNDAY
            ],
            hour_of_day=[i for i in range(24)]  # 0 to 23
        ),
        filters=[streaming.RawRequestFilter.UNSPECIFIED]
    )

    for response in paginate_processed_point(client, request):
        ## helper to print enum objects
        # print("Vehicle Type:", get_enum_str(response, streaming.ProcessedPoint.VEHICLE_TYPE_FIELD_NUMBER, response.vehicle_type))
        print(response)


if __name__ == "__main__":
    main()
