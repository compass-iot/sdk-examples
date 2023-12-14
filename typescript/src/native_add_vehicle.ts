import * as native from "@buf/compassiot_api.bufbuild_es/compassiot/native/v1/native_pb"

import client from "./client"

const request = new native.AddVehicleRequest({
  providerAuth: new native.AuthRequest({
    provider: {
      case: "tesla",
      value: new native.TeslaAuth({
        vin: ""
      })
    }
  })
})

const response = await client.nativeAddVehicle(request)

console.log(response.toJsonString({ prettySpaces: 2 }))
