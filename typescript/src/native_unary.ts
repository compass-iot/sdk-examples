import client from "./client"

const response = await client.nativeGetVehicles({})

console.log(response.toJsonString({ prettySpaces: 2 }))
