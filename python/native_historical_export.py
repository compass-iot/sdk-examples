from client import create_gateway_client
import compassiot.compass.v1.time_pb2 as time
import compassiot.native.v1.native_pb2 as native


def main():
    client = create_gateway_client()

    request = native.HistoricalExportRequest(
        filter_vins=[],
        filter_type=native.HistoricalExportFilterType.TRIP,
        filter_dates=time.DateTimeRange(
            start=time.LocalDate(
                day=1,
                month=10,
                year=2023
            ),
            end=time.LocalDate(
                day=10,
                month=10,
                year=2023
            ),
            day_of_week=[
                time.DayOfWeek.MONDAY,
                time.DayOfWeek.WEDNESDAY,
                time.DayOfWeek.FRIDAY,
                time.DayOfWeek.SUNDAY
            ],
            hour_of_day=[i for i in range(24)]
        )
    )

    response = client.NativeHistoricalExport(request)

    print(response.csv_links)

     
if __name__ == "__main__":
    main()
