import * as streaming from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"

import client from "./client"

const request = new streaming.RealtimeRawPointByVinsRequest({
  vins: [],
  streamEnv: streaming.StreamEnvironment.DEV
})

for await (const response of client.realtimeRawPointByVins(request)) {
  console.log(response.toJsonString({ prettySpaces: 2 }))
}
