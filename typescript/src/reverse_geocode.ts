import * as location from "@buf/compassiot_api.bufbuild_es/compassiot/location/v1/location_pb"

import { createNodeClient } from "./client"

const client = createNodeClient()

const request = new location.ReverseGeocodeRequest({
  polygonWkt: "POLYGON ((151.21229795582838 -33.89101682624773, 151.19573365832508 -33.87414013405557, 151.20665103622446 -33.858041660571004, 151.22490940960853 -33.870545592545284, 151.21229795582838 -33.89101682624773))"
})

const response = await client.reverseGeocode(request)

console.log(response.toJsonString({ prettySpaces: 2 }))
