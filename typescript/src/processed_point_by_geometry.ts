import * as time from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/time_pb"
import * as streaming from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"

import client from "./client"

const request = new streaming.ProcessedPointByGeometryRequest({
  linestringOrPolygonWkt: "POLYGON ((151.116490002445 -34.136652437446564, 150.76133775468065 -33.970878990313345,150.8238645588653 -33.68832143811975, 150.93391173422782 -33.51542003355166, 151.17151359012706 -33.594622738528074, 151.3165757758332 -33.67583417052261, 151.3115736314981 -33.80478175152794, 151.22903824997502 -34.03515466768564, 151.116490002445 -34.136652437446564))",
  dateTimeRange: new time.DateTimeRange({
    start: new time.LocalDate({
      day: 1,
      month: 10,
      year: 2023
    }),
    end: new time.LocalDate({
      day: 31,
      month: 10,
      year: 2023
    }),
    hourOfDay: Array.from(Array(24).keys())  // 0 to 23
  })
})

for await (const response of client.processedPointByGeometry(request)) {
  console.log(response.toJsonString({ prettySpaces: 2 }))
}
