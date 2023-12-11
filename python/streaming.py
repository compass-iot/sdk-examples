from compassiot.platform.v1.streaming_pb2 import RealtimeRawPointByGeometryRequest, StreamEnvironment
from client import create_gateway_client


def main():
  client = create_gateway_client()

  request = RealtimeRawPointByGeometryRequest(
    bounds_wkt="POLYGON ((151.116490002445 -34.136652437446564, 150.76133775468065 -33.970878990313345, 150.8238645588653 -33.68832143811975, 150.93391173422782 -33.51542003355166, 151.17151359012706 -33.594622738528074, 151.3165757758332 -33.67583417052261, 151.3115736314981 -33.80478175152794, 151.22903824997502 -34.03515466768564, 151.116490002445 -34.136652437446564))",
    stream_env=StreamEnvironment.DEV
  )

  for response in client.RealtimeRawPointByGeometry(request):
    print(response)


if __name__ == "__main__":
  main()
