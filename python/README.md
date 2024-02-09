# Python Examples

## Quickstart

1. Install the required modules:
```bash
python3 -m pip install compassiot-api-grpc-python compassiot-api-protocolbuffers-python requests grpc_interceptor --extra-index-url https://buf.build/gen/python
```

2. (Optional) Install strong typing for Compass IoT modules:
```bash
python3 -m pip install compassiot-api-community-nipunn1313-mypy-grpc compassiot-api-community-nipunn1313-mypy --extra-index-url https://buf.build/gen/python
```

3. Set your API key in `client.py` on line `16`

4. Run any of the examples, e.g. to run `aggregate_by_path.py`:
```bash
python3 aggregate_by_path.py
```

Note: Please find our API documentation [here](https://api.compassiot.cloud/docs). The proto files for our APIs, can be found [here](https://buf.build/compassiot/api).

## FAQ

### Long-lived Streaming

The HTTP/2 protocol was designed to buffer payload too large to be sent over HTTP/1.1. Hence HTTP timeouts still exist in the streaming world. RPCs which may have long periods of inactivity, such as `RealtimeRawPointByVins`, suffer from [HTTP 504](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/504) timeout if there are no data sent within 5 minutes. Note that since `RealtimeRawPointByGeometry` aggregates vehicles, it is more frequent in sending data, and hence suffers less from <strong>HTTP 504</strong> timeout.

To support such use case, we expose a utility function from `client.py` to create a new stream whenever it gets disconnected due to no data:
```py
from client import create_gateway_client, retry_stream

client = create_gateway_client()

for response in retry_stream(lambda: client.RealtimeRawPointByVins(request)):
    print(response)
```
