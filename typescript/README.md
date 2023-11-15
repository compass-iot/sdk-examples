# Typescript Example

Connect RPC supports two types of protocol:
- Unary: traditional request-response model similar to REST APIs
- Streaming: maintains persistent connection similar to [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API), but much more performant, comparable to [grpc-web](https://grpc.io/docs/platforms/web/basics/). See comparison between Connect & gRPC Web [here](https://stackoverflow.com/questions/50956757/http-2-or-websockets-for-low-latency-client-to-server-messages/59690386#59690386).

## Prerequisites

You'll firstly need the `client_secret` provisioned by Compass IoT to run the examples. Then, the next steps are:
1. Clone this repository
```bash
% git clone https://github.com/compass-iot/sdk-examples.git
```
2. Install dependencies
```bash
% npm install  # similar command in yarn & pnpm
```
or to install them manually (in another project):
```bash
% npm install --save \
    @buf/compassiot_model.bufbuild_es \
    @buf/compassiot_api.bufbuild_es \
    @buf/compassiot_api.connectrpc_es \
    @bufbuild/protobuf \
    @connectrpc/connect \
    @connectrpc/connect-web
```

3. Run example
```bash
% npm run unary  # src/unary.ts
% npm run streaming  # src/streaming.ts
% npm run streaming-throttled  # src/streaming-throttled.ts
```
