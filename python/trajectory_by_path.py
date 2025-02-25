from client import RoadIntelligenceClient, SECRET

import compassiot.compass.v1.time_pb2 as time
import compassiot.platform.v1.streaming_pb2 as streaming


def main():
    client = RoadIntelligenceClient(SECRET)

    request = streaming.TrajectoryByPathRequest(
        linestring_wkt="LINESTRING (151.188277 -33.884699, 151.18862 -33.884707, 151.189805 -33.884734, 151.190091 -33.884743, 151.19063 -33.884758, 151.190909 -33.884747, 151.191247 -33.884724, 151.191281 -33.884723, 151.191439 -33.88471, 151.191552 -33.884699, 151.191722 -33.884682, 151.192145 -33.884643, 151.192449 -33.884608)",
        date_time_range=time.DateTimeRange(
            start=time.LocalDate(day=1, month=10, year=2023),
            end=time.LocalDate(day=31, month=10, year=2023),
            day_of_week=[time.DayOfWeek.SATURDAY, time.DayOfWeek.SUNDAY],
            hour_of_day=[i for i in range(24)],  # 0 to 23
            # include the list of dates you would like to exclude from the query, if any
            exclude_date=[
                time.LocalDate(day=10, month=10, year=2023),
                time.LocalDate(day=11, month=10, year=2023),
            ],
        ),
    )

    for response in client.TrajectoryByPath(request):
        print(response)


if __name__ == "__main__":
    main()
