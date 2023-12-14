from client import create_gateway_client
import compassiot.compass.v1.time_pb2 as time
import compassiot.platform.v1.streaming_pb2 as streaming


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
            hour_of_day=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
            day_of_week=[
                time.DayOfWeek.SATURDAY,
                time.DayOfWeek.SUNDAY,
                time.DayOfWeek.MONDAY,
                time.DayOfWeek.TUESDAY,
                time.DayOfWeek.WEDNESDAY,
                time.DayOfWeek.THURSDAY,
                time.DayOfWeek.FRIDAY,
            ]
        ),
        filters=[streaming.RawRequestFilter.UNSPECIFIED]
    )

    for response in client.ProcessedPointByGeometry(request):
        print(response)


if __name__ == "__main__":
    main()
