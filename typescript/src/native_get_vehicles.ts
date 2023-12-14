import { Empty } from "@bufbuild/protobuf"

import client from "./client"

const request = new Empty()

const response = await client.nativeGetVehicles(request)

console.log(response.toJsonString({ prettySpaces: 2 }))
