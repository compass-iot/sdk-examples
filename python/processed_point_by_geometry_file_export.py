from client import RoadIntelligenceClient, SECRET

import compassiot.compass.v1.time_pb2 as time
import compassiot.platform.v1.streaming_pb2 as streaming
import compassiot.compass.v1.vehicle_pb2 as vehicle
import compassiot.compass.v1.file_pb2 as file


def main():
    client = RoadIntelligenceClient(SECRET)

    request = streaming.ProcessedPointByGeometryFileExportRequest(
        linestring_or_polygon_wkt="LINESTRING(151.18703722810923 -33.8695894847834,151.18361472940623 -33.868689747746664)",
        date_time_range=time.DateTimeRange(
            start=time.LocalDate(day=1, month=10, year=2023),
            end=time.LocalDate(day=31, month=10, year=2023),
            day_of_week=[
                time.DayOfWeek.SATURDAY,
                time.DayOfWeek.SUNDAY,
                time.DayOfWeek.MONDAY,
                time.DayOfWeek.TUESDAY,
            ],
            hour_of_day=[i for i in range(24)],  # 0 to 23
            # include the list of dates you would like to exclude from the query, if any
            exclude_date=[
                time.LocalDate(day=10, month=10, year=2023),
                time.LocalDate(day=11, month=10, year=2023),
            ],
        ),
        # specify if any filter exists, leave empty for all data
        filters=[streaming.RawRequestFilter.UNSPECIFIED],
        # specify all vehicle types that you would like to receive in the response, leave empty for all vehicle types
        vehicle_type_filter=[vehicle.VehicleType.CAR],
        file_type=file.CSV,
    )

    response = client.ProcessedPointByGeometryFileExport(request)
    print(response)


if __name__ == "__main__":
    main()
