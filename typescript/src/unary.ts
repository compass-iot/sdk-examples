import { AggregateByPathRequest } from "@buf/compassiot_model.bufbuild_es/platform/v1/unary_pb"
import { DayOfWeek } from "@buf/compassiot_model.bufbuild_es/compass/v1/time_pb"

import createGatewayClient from "./client"

const ENDPOINT = "https://api.compassiot.cloud"
const SECRET = "...insert client secret here..."

const request = new AggregateByPathRequest({
  linestringWkt: "LINESTRING (151.194525 -33.87363, 151.194109 -33.873076, 151.193736 -33.872564, 151.193507 -33.872265, 151.193347 -33.872052, 151.193259 -33.871925, 151.193228 -33.871889)",

  // Try October:
  // - Dates: 2023-10-01 to 2023-10-31
  // - All hours (0 - 23)
  // - Only weekends (Saturday & Sunday)
  dateTimeRange: {
    start: {
      day: 1,
      // beware JS & TS users, Date.getMonth() returns integer between 0-11, so should add +1
      month: 10,
      year: 2023
    },
    end: {
      day: 31,
      month: 10,
      year: 2023
    },
    dayOfWeek: [
      DayOfWeek.SATURDAY,
      DayOfWeek.SUNDAY
    ],
    hourOfDay: []
  }
})

const client = createGatewayClient(ENDPOINT, SECRET)

console.log("Querying AggregateByPath")

const response = await client.aggregateByPath(request)

console.log(response.toJsonString({ prettySpaces: 2 }))
