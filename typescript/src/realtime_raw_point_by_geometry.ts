import * as streaming from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"

import { createNodeClient, retryStream } from "./client"

const client = createNodeClient()

const request = new streaming.RealtimeRawPointByGeometryRequest({
  boundsWkt: "POLYGON ((151.24515599751396 -33.99690664408569, 151.1312304506755 -33.922084606957064, 151.16130001880038 -33.84614157217645, 151.25574387361428 -33.86302364348595, 151.2887780470458 -33.850010674904205, 151.24515599751396 -33.99690664408569))",
  streamEnv: streaming.StreamEnvironment.DEV
})

for await (const response of retryStream(() => client.realtimeRawPointByGeometry(request))) {
  console.log(response.toJsonString({ prettySpaces: 2 }))
}
