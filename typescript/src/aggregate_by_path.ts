import * as time from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/time_pb"
import * as unary from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/unary_pb"

import client from "./client"

const request = new unary.AggregateByPathRequest({
  linestringWkt: "LINESTRING (151.194525 -33.87363, 151.194109 -33.873076, 151.193736 -33.872564, 151.193507 -33.872265, 151.193347 -33.872052, 151.193259 -33.871925, 151.193228 -33.871889)",
  dateTimeRange: {
    start: {
      day: 1,
      month: 10,
      year: 2023
    },
    end: {
      day: 31,
      month: 10,
      year: 2023
    },
    dayOfWeek: [
      time.DayOfWeek.SATURDAY,
      time.DayOfWeek.SUNDAY
    ],
    hourOfDay: Array.from(Array(24).keys()) // 0 to 23
  }
})

const response = await client.aggregateByPath(request)

console.log(response.toJsonString({ prettySpaces: 2 }))
