# Python Examples

### Requirements

You'll need:

1. `pip` or `uv`

Checkout the `uv` installation guide [here](https://docs.astral.sh/uv/#installation).
Or, alternatively use the `pip` installation guide [here](https://pip.pypa.io/en/stable/installation/) if not already bundled.

2. Python 3.12 or newer (Check using `python3 --version`)

You can install or update python from the following guide [here](https://www.datacamp.com/tutorial/pip-upgrade-python).
Please note, this will occur automatically if you use `uv`.

3. To install the depdencies

If you're using `uv`, run the following command:

```bash
uv pip install --requirements requirements.txt
```

However, if you're using `pip`, run the following command:

```bash
pip install -r requirements.txt --extra-index-url https://buf.build/gen/python
```

### Example Script

#### Assigning your API Key

To begin, you must first assign your API key to the `SECRET` variable in `client.py`, line `26`.
Once you have met all the requirements below, go to the "Example Script" section to see the SDK in action.

You may begin by running any of the caller functions.

#### Making an API call

Let's call the [`AggregateByPath`](https://api.compassiot.cloud/docs/gateway/AggregateByPath) RPC. We can do so using the example provided in `aggregate_by_path.py`, and running it using the following command based on the package manager we selected earlier.

```bash
# Using UV
uv run aggregate_by_path.py

# Using PIP
python3 aggregate_by_path.py
```

> Please find our API documentation [here](https://api.compassiot.cloud/docs).
> The protobuf files for our APIs, can be found [here](https://buf.build/compassiot/api).

## FAQs

### What is Unary, what is Streaming?

There are two forms of APIs, there are unary APIs and streaming APIs.

Unary APIs are simple request-response APIs, meaning you will have a request structure and a response structure, there will be only one request for each singular response.
As an example, the [`AggregateByPath`](https://api.compassiot.cloud/docs/gateway/AggregateByPath) RPC accepts an [`AggregateByPathRequest`](https://buf.build/compassiot/api/docs/fe4a263c804c4ffa9b0861a9caa5effe:compassiot.platform.v1#compassiot.platform.v1.AggregateByPathRequest) and returns an [`AggregateByPathResponse`](https://buf.build/compassiot/api/docs/fe4a263c804c4ffa9b0861a9caa5effe:compassiot.platform.v1#compassiot.platform.v1.AggregateByPathResponse).

Streaming APIs meanwhile, are APIs that allow for a continuous stream of data.
This means the response structure is sent asynchronously. As an example, the [`ProcessedPointByGeometry`](https://api.compassiot.cloud/docs/gateway/ProcessedPointByGeometry) API accepts a [`ProcessedPointByGeometryRequest`](https://buf.build/compassiot/api/docs/fe4a263c804c4ffa9b0861a9caa5effe:compassiot.platform.v1#compassiot.platform.v1.ProcessedPointByGeometryRequest) and returns a stream of [`ProcessedPoint`](https://buf.build/compassiot/api/docs/fe4a263c804c4ffa9b0861a9caa5effe:compassiot.platform.v1#compassiot.platform.v1.ProcessedPoint) responses, which can be consumed in a loop.

```python
# Create our request structure
request = streaming.ProcessedPointByGeometryRequest(...)

# Consume our response as a Generator-type.
for response in client.ProcessedPointByGeometry(request):
    print(response)
```

These streams are short-lived, and so may restart during the lifetime of downloading your data,
so keep this in mind if you are monitoring the rate of data returned from your stream.
