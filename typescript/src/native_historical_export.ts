import * as time from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/time_pb"
import * as native from "@buf/compassiot_api.bufbuild_es/compassiot/native/v1/native_pb"

import client from "./client"

const request = new native.HistoricalExportRequest({
  filterVins: [],
  filterDates: new time.DateTimeRange({
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
    dayOfWeek: [
      time.DayOfWeek.SATURDAY,
      time.DayOfWeek.SUNDAY
    ],
    hourOfDay: Array.from(Array(24).keys())  // 0 to 23
  })
})

const response = await client.nativeHistoricalExport(request)

console.log(response.toJsonString({ prettySpaces: 2 }))
