import * as native from "@buf/compassiot_api.bufbuild_es/compassiot/native/v1/native_pb"

import { createNodeClient } from "./client"

const client = createNodeClient()

const request = new native.GetLatestPointRequest({
  vin: ""
})

const response = await client.nativeGetLatestPoint(request)

console.log(response.toJsonString({ prettySpaces: 2 }))
