import asyncio
from grpclib.client import Channel

from auth import get_access_token
from sdk.gateway.v1 import ServiceStub
from sdk.platform.v1 import RealtimeRawPointByGeometryRequest, StreamEnvironment


HOST = "beta.api.compassiot.cloud"
SECRET = "...INSERT SECRET HERE..."


async def main():
  # Setup, notice that we attach the access token inside metadata
  access_token = await get_access_token()
  metadata = [('authorization', 'Bearer %s' % (access_token))]
  channel = Channel(host=HOST)
  service = ServiceStub(channel, metadata=metadata)

  request = RealtimeRawPointByGeometryRequest(
    bounds_wkt="POLYGON ((151.116490002445 -34.136652437446564, 150.76133775468065 -33.970878990313345, 150.8238645588653 -33.68832143811975, 150.93391173422782 -33.51542003355166, 151.17151359012706 -33.594622738528074, 151.3165757758332 -33.67583417052261, 151.3115736314981 -33.80478175152794, 151.22903824997502 -34.03515466768564, 151.116490002445 -34.136652437446564))",
    stream_env=StreamEnvironment.DEV
  )

  async for response in service.realtime_raw_point_by_geometry(request):
    print(response)

  # Remember to close channel to avoid hanging
  channel.close()


if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
