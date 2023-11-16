# Typescript Example

Connect RPC supports two types of protocol:
- Unary: traditional request-response model similar to REST APIs
- Streaming: maintains persistent connection similar to [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API), but much more performant, comparable to [grpc-web](https://grpc.io/docs/platforms/web/basics/).

## Prerequisites

You'll firstly need the `client_secret` provisioned by Compass IoT to run the examples. Then, the next steps are:
1. Clone this repository
```sh
git clone https://github.com/compass-iot/sdk-examples.git

cd sdk-examples/typescript
```
2. Install dependencies
```sh
npm install  # similar command in yarn & pnpm
```
or to install them manually (in another project):
```sh
npm install --save \
  @buf/compassiot_model.bufbuild_es \
  @buf/compassiot_api.bufbuild_es \
  @buf/compassiot_api.connectrpc_es \
  @bufbuild/protobuf \
  @connectrpc/connect \
  @connectrpc/connect-web
```

3. Modify client secret
In each of the files `src/unary.ts`, `src/streaming.ts` & `src/streaming-throttled.ts`, and update the `SECRET` variable:
```ts
import { AggregateByPathRequest } from "@buf/compassiot_model.bufbuild_es/platform/v1/unary_pb"
import { DayOfWeek } from "@buf/compassiot_model.bufbuild_es/compass/v1/time_pb"

import createGatewayClient from "./client"

const ENDPOINT = "https://api.compassiot.cloud"

// Set the following to client secret
const SECRET = "...insert client secret here..."
```

4. Run examples
```sh
npm run unary  # src/unary.ts
npm run streaming  # src/streaming.ts
npm run streaming-throttled  # src/streaming-throttled.ts
```
