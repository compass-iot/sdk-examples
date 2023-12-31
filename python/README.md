# Python Examples

1. Install the foundation modules:
```bash
pip3 install requests grpc_interceptor
```

2. Install Compass IoT modules:
```bash
python3 -m pip install compassiot-api-grpc-python compassiot-api-protocolbuffers-python --extra-index-url https://buf.build/gen/python
```

3. (Optional) Install strong typing for Compass IoT modules:
```bash
python3 -m pip install compassiot-api-community-nipunn1313-mypy-grpc compassiot-api-community-nipunn1313-mypy --extra-index-url https://buf.build/gen/python
```

4. Set your API key in `client.py` on line `15`

5. Run any of the examples, e.g. to run `aggregate_by_path.py`:
```bash
python3 aggregate_by_path.py
```

Note: Pls find our API doc [here](https://beta.api.compassiot.cloud/docs). The proto files for our APIs, can be found [here](https://buf.build/compassiot/api).
