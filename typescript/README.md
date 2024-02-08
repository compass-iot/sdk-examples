# Typescript Examples

## Note for Node v19+ users

Due to an ongoing [memory leak issue](https://github.com/nodejs/undici/issues/2143) for <u>Node v19+</u> in [undici](https://github.com/nodejs/undici), it is highly recommended to use <u>Node v18</u> if you are running the examples locally or developing a server-side NodeJS app (even if you're using <strong>connect-web</strong> as it calls <strong>undici</strong> under the hood).

Use:
- [connect-node](https://connectrpc.com/docs/node/using-clients) if you're building a server-side NodeJS app
- [connect-web](https://connectrpc.com/docs/web/using-clients) if the app runs on the browser / mobile

While <strong>connect-web</strong> can be used server-side via <strong>undici</strong>, <strong>connect-node</strong> has access to native gRPC transport and will generally be more efficient.

## Quickstart

All examples will use <strong>connect-node</strong>. For running the examples on the browser / mobile using <strong>connect-web</strong>, see [here](#connect-web).

1. Configure NPM to use Buf registry:
```bash
npm config set @buf:registry https://buf.build/gen/npm/v1/

# or if using pnpm
pnpm config set @buf:registry https://buf.build/gen/npm/v1/

# Yarn versions greater than v1.10.0 and less than v2 are not supported
yarn config set npmScopes.buf.npmRegistryServer https://buf.build/gen/npm/v1/
```

2. Install Node modules:
```bash
npm install && npm update
```

3. Set your API key in `src/client.ts` on line `7`

4. To run any of the examples, we encourage using Typescript server to avoid TS transpilation issues. We recommend using `tsx` as it works for us, so to run, for instance, `src/platform_streaming.ts`, do:
```bash
npx tsx ./src/platform_streaming.ts
```

## FAQ

### Connect Web

Use `connect-web` when you are building an app running in the browser (e.g. React, Vue). The change from `connect-node` to `connect-web` is quite straightforward:
```TS
- import { createNodeClient } from "./client"
+ import { createWebClient } from "./client"

- const client = createNodeClient()
+ const client = createWebClient()
```

### Long-lived Streaming

The HTTP/2 protocol was designed to buffer payload too large to be sent over HTTP/1.1 via streaming. Hence HTTP timeouts still exist in the streaming world. RPCs which may have long periods of inactivity, such as `RealtimeRawPointByVins` suffers from [HTTP 504](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/504) timeout if there is no data sent within 5 minutes. Note that since `RealtimeRawPointByGeometry` aggregates vehicles, it is more frequent in sending data, and hence suffers less from <strong>HTTP 504</strong> timeout.

To support such use case, we expose a utility function from `client.ts`:
```TS
import { createNodeClient, retryStream } from "./client"

const client = createNodeClient()

const stream = () => client.realtimeRawPointByVins(request)

for await (const response of retryStream(stream)) {
    // Do something
}
```

`retryStream` accepts a lambda which returns an `AsyncIterable`. Under the hood, the stream gets wrapped in a `try-catch` statement such that when it gets disconnected due to no data, it will create a new stream and allow clients to continue consuming the stream.
