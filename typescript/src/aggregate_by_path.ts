import * as time from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/time_pb"
import * as unary from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/unary_pb"

import { createNodeClient } from "./client"

// Speeds in requests and responses are always km/h
const KMH_PER_MPH = 1.609344

const client = createNodeClient()

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
  },
  speedDistribution: {
    rangeStart: 0,
    rangeEnd: 75 * KMH_PER_MPH,
    stepSize: 5 * KMH_PER_MPH
  }
})

const response = await client.aggregateByPath(request)

console.log(response.toJsonString({ prettySpaces: 2 }))

// // To view speed distribution bins
// response.aggregate.forEach((aggregate, i) => {
//   console.log(`Aggregate ${i} speed distribution:`)
//   for (const bin of aggregate.total?.speedDistribution ?? []) {
//     const from = (bin.rangeStart / KMH_PER_MPH).toFixed(0)
//     const to = (bin.rangeEnd / KMH_PER_MPH).toFixed(0)
//     console.log(`  ${from}-${to} mph: ${bin.tripCountTotalPercentile.toFixed(1)}% of trips`)
//   }
// })
