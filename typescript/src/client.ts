import { Service } from "@buf/compassiot_api.connectrpc_es/compassiot/gateway/v1/gateway_connect"
import { createConnectTransport as createNodeTransport, ConnectTransportOptions as NodeTransportOptions } from "@connectrpc/connect-node"
import { createConnectTransport as createWebTransport, ConnectTransportOptions as WebTransportOptions } from "@connectrpc/connect-web"
import { Code, ConnectError, createPromiseClient, PromiseClient, type Interceptor } from "@connectrpc/connect"

const HOST = "https://api.compassiot.cloud"
const SECRET = "__INSERT_YOUR_COMPASSIOT_API_KEY__"
const CLIENT_TIMEOUT_MS = 1000 * 60 * 3 // 3 mins, must be lower than server timeout of 5 mins lest we get HTTP 504 from GCP

function createAuthInterceptor(secret: string, client: PromiseClient<typeof Service>): Interceptor {
  // Need a `let` so we can replace the access token for long-lived usage
  let at = ""

  return next => async req => {
    try {
      if (at === "") {
        const { accessToken } = await client.authenticate({ token: secret })
        at = accessToken
      }
      req.header.set("Authorization", `Bearer ${at}`)
      return await next(req)
    }
    catch (err) {
      if (err instanceof ConnectError) {
        if (err.code === Code.Unauthenticated) {
          const { accessToken } = await client.authenticate({ token: secret })
          at = accessToken
          req.header.set("Authorization", `Bearer ${at}`)
          return await next(req)
        }
      }
      throw err
    }
  }
}

function createNodeClient(options?: Omit<NodeTransportOptions, "baseUrl" | "httpVersion">): PromiseClient<typeof Service> {
  const noauthClient = createPromiseClient(Service, createNodeTransport({
    baseUrl: HOST,
    httpVersion: "1.1",
    useHttpGet: true,
    defaultTimeoutMs: CLIENT_TIMEOUT_MS
  }))
  const transport = createNodeTransport({
    baseUrl: HOST,
    httpVersion: "2",
    interceptors: [createAuthInterceptor(SECRET, noauthClient)],
    ...options
  })
  return createPromiseClient(Service, transport)
}

function createWebClient(options?: Omit<WebTransportOptions, "baseUrl">): PromiseClient<typeof Service> {
  const noauthClient = createPromiseClient(Service, createWebTransport({
    baseUrl: HOST,
    useHttpGet: true,
    defaultTimeoutMs: CLIENT_TIMEOUT_MS
  }))
  const transport = createWebTransport({
    baseUrl: HOST,
    interceptors: [createAuthInterceptor(SECRET, noauthClient)],
    ...options
  })
  return createPromiseClient(Service, transport)
}

async function* retryStream<T>(stream: () => AsyncIterable<T>): AsyncIterable<T> {
  let iterable = stream()
  for (; ;) {
    try {
      for await (const r of iterable) {
        yield r
      }
    } catch (err) {
      switch (ConnectError.from(err).code) {
        case Code.DeadlineExceeded:
          console.log(`DeadlineExceeded, retrying stream`)
          iterable = stream()
          continue
        default:
          throw err
      }
    }
  }
}

export { createNodeClient, createWebClient, retryStream }
