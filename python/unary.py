import asyncio
from grpclib.client import Channel

from auth import get_access_token
from sdk.gateway.v1 import ServiceStub
from sdk.platform.v1 import AggregateByPathRequest
from sdk.compass.v1 import DateTimeRange, LocalDate, DayOfWeek


HOST = "api.compassiot.cloud"
SECRET = "...INSERT SECRET HERE..."


async def main():
  # Setup, notice that we attach the access token inside metadata
  access_token = await get_access_token()
  metadata = [('authorization', 'Bearer %s' % (access_token))]
  channel = Channel(host=HOST)
  service = ServiceStub(channel, metadata=metadata)

  # Try October:
  # - Dates: 2023-10-01 to 2023-10-31
  # - All hours (0 - 23)
  # - Only weekends (Saturday & Sunday)
  request = AggregateByPathRequest(
    linestring_wkt="LINESTRING (151.194525 -33.87363, 151.194109 -33.873076, 151.193736 -33.872564, 151.193507 -33.872265, 151.193347 -33.872052, 151.193259 -33.871925, 151.193228 -33.871889)",
    date_time_range=DateTimeRange(
      start=LocalDate(
        day=1,
        month=10,
        year=2023
      ),
      end=LocalDate(
        day=31,
        month=10,
        year=2023
      ),
      hour_of_day=[],
      day_of_week=[
        DayOfWeek.SATURDAY,
        DayOfWeek.SUNDAY
      ]
    )
  )

  response = await service.aggregate_by_path(request)
  print(response)

  # Remember to close channel to avoid hanging
  channel.close()


if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
