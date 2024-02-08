import { Empty } from "@bufbuild/protobuf"

import { createNodeClient } from "./client"

const client = createNodeClient()

const request = new Empty()

const response = await client.nativeGetVehicles(request)

console.log(response.toJsonString({ prettySpaces: 2 }))
