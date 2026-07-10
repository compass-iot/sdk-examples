import { Service } from "@buf/compassiot_api.connectrpc_es/compassiot/gateway/v1/gateway_connect"
import { createConnectTransport as createNodeTransport, ConnectTransportOptions as NodeTransportOptions } from "@connectrpc/connect-node"
import { createConnectTransport as createWebTransport, ConnectTransportOptions as WebTransportOptions } from "@connectrpc/connect-web"
import { Code, ConnectError, createPromiseClient, PromiseClient, type Interceptor } from "@connectrpc/connect"

const HOST = "https://api.compassiot.cloud"
const SECRET = "__INSERT_YOUR_COMPASSIOT_API_KEY__"
const TIMEOUT_MS = 1000 * 60 * 25  // used by retryStream

// Detect silently-dropped connections (e.g. NAT/firewall state loss) and
// reconnect automatically. The session manager sends an HTTP/2 PING every 60s
// and closes the session (and its streams) if no ack arrives within 20s, so
// the next request opens a fresh connection. Without these options, a stream
// on a dead TCP connection hangs until its deadline, and every retry on the
// same session hangs the same way, and only a process restart recovers.
const KEEPALIVE_OPTIONS = {
  pingIntervalMs: 60_000,
  pingTimeoutMs: 20_000,
  pingIdleConnection: true,
}

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
  }))
  const transport = createNodeTransport({
    baseUrl: HOST,
    httpVersion: "2",
    ...KEEPALIVE_OPTIONS,
    interceptors: [createAuthInterceptor(SECRET, noauthClient)],
    ...options,
  })
  return createPromiseClient(Service, transport)
}

function createWebClient(options?: Omit<WebTransportOptions, "baseUrl">): PromiseClient<typeof Service> {
  const noauthClient = createPromiseClient(Service, createWebTransport({
    baseUrl: HOST,
  }))
  const transport = createWebTransport({
    baseUrl: HOST,
    interceptors: [createAuthInterceptor(SECRET, noauthClient)],
    ...options,
  })
  return createPromiseClient(Service, transport)
}

/**
 * Keeps a server-streaming RPC alive indefinitely.
 *
 * Streams are opened with a deadline (e.g. TIMEOUT_MS), so DeadlineExceeded is
 * the normal end-of-cycle signal and the stream is simply reopened. Reopening
 * on the same transport is safe after a network failure because
 * KEEPALIVE_OPTIONS make the session detect a dead connection and reconnect
 * on its own.
 */
async function* retryStream<T>(stream: () => AsyncIterable<T>): AsyncIterable<T> {
  let iterable = stream()
  for (; ;) {
    let receivedAny = false
    try {
      for await (const r of iterable) {
        receivedAny = true
        yield r
      }
      // Server ended the stream cleanly — reopen it.
      iterable = stream()
    } catch (err) {
      switch (ConnectError.from(err).code) {
        case Code.DeadlineExceeded:
          if (receivedAny) {
            console.log(`DeadlineExceeded, retrying stream`)
          } else {
            console.log(`DeadlineExceeded with no data received, retrying stream`)
          }
          iterable = stream()
          continue
        default:
          throw err
      }
    }
  }
}

export { createNodeClient, createWebClient, retryStream, TIMEOUT_MS }
