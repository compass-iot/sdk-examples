import { Service } from "@buf/compassiot_api.connectrpc_es/gateway/v1/gateway_connect"
import { createConnectTransport, ConnectTransportOptions } from "@connectrpc/connect-web"
import { Code, ConnectError, createPromiseClient, PromiseClient, type Interceptor } from "@connectrpc/connect"

const ENDPOINT = "https://api.compassiot.cloud"

function createGatewayClient(secret: string, options?: ConnectTransportOptions): PromiseClient<typeof Service> {
  // Instantiate at top level for memoisation (optimisation)
  const noauthTransport = createConnectTransport({ baseUrl: ENDPOINT })
  const noauthClient = createPromiseClient(Service, noauthTransport)

  // Need a `let` so we can replace the access token for long-lived usage
  let accessToken = ""

  function createTokenRefreshInterceptor(secret: string): Interceptor {
    return (next) => async req => {
      // Try making request to see if we're still authenticated
      try {
        // Initialise access token if it's empty
        if (accessToken === "") {
          const { accessToken: newAccessToken } = await noauthClient.authenticate({ token: secret })
          accessToken = newAccessToken
        }
        req.header.set("Authorization", `Bearer ${accessToken}`)
        return await next(req)
      }
      catch (err) {
        // Try wrapping as ConnectError to get more context
        if (err instanceof ConnectError) {
          if (err.code === Code.Unauthenticated) {
            // Fetch new access token & update the old one
            const { accessToken: newAccessToken } = await noauthClient.authenticate({ token: secret })
            accessToken = newAccessToken

            // Retry the request
            req.header.set("Authorization", `Bearer ${accessToken}`)
            return await next(req)
          }
          else {
            // Print error, but here we have more context as it's wrapped in ConnectError
            console.error(err.code, err.cause)

            // Or if you prefer stack trace
            console.error(err.stack)
          }
        } else {
          console.error(err)
        }
      }
      return await next(req)
    }
  }

  const transport = createConnectTransport({
    baseUrl: ENDPOINT,
    interceptors: [createTokenRefreshInterceptor(secret)],
    ...options
  })
  return createPromiseClient(Service, transport)
}

export default createGatewayClient
