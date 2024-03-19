from client import create_gateway_client, retry_stream, TIMEOUT_SEC
import compassiot.platform.v1.streaming_pb2 as streaming


def main():
    client = create_gateway_client()

    request = streaming.RealtimeRawPointByVinsRequest(
        vins=[],
        stream_env= streaming.StreamEnvironment.DEV
    )
    
    for response in retry_stream(lambda: client.RealtimeRawPointByVins(request, timeout=TIMEOUT_SEC)):
        print(response)


if __name__ == "__main__":
    main()
