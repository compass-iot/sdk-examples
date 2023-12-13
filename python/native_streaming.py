from compassiot.platform.v1.streaming_pb2 import RealtimeRawPointByVinsRequest, StreamEnvironment
from client import create_gateway_client


def main():
    client = create_gateway_client()

    # Insert your VINs here but ensure that they've been added to Compass
    vins = []
    request = RealtimeRawPointByVinsRequest(
	    vins=vins,
	    stream_env=StreamEnvironment.DEV
    )

    for response in client.RealtimeRawPointByVins(request):
	    print(response)


if __name__ == "__main__":
    main()
