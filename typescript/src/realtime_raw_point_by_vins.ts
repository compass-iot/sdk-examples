import * as streaming from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"

import { TIMEOUT_MS, createNodeClient, retryStream } from "./client"

const client = createNodeClient()

const request = new streaming.RealtimeRawPointByVinsRequest({
  vins: [],
  streamEnv: streaming.StreamEnvironment.DEV
})

for await (const response of retryStream(() => client.realtimeRawPointByVins(request, { timeoutMs: TIMEOUT_MS }))) {
  console.log(response.toJsonString({ prettySpaces: 2 }))
}
