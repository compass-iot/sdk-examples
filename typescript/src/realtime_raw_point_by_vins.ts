import * as streaming from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"

import { createNodeClient, retryStream } from "./client"

const client = createNodeClient()

const request = new streaming.RealtimeRawPointByVinsRequest({
  vins: [],
  streamEnv: streaming.StreamEnvironment.DEV
})

for await (const response of retryStream(() => client.realtimeRawPointByVins(request))) {
  console.log(response.toJsonString({ prettySpaces: 2 }))
}
