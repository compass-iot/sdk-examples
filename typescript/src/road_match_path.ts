import * as geo from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/geo_pb"
import * as gateway from "@buf/compassiot_api.bufbuild_es/compassiot/gateway/v1/gateway_pb"


import {createNodeClient} from "./client"

const client = createNodeClient()

const request = new gateway.RoadMatchPathRequest({
    rawPoints: [
        new geo.LatLng({
        lat: -33.85715882779781,
        lng: 151.20751220989666
    }),
        new geo.LatLng({
        lat: -33.84842568559147,
        lng: 151.212589825605
    })
    ]
})

const response = await client.roadMatchPath(request)

console.log(response.toJsonString({prettySpaces: 2}))
