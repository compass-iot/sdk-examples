import * as time from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/time_pb"
import * as streaming from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"

import {createNodeClient} from "./client"

const client = createNodeClient()
const request = new streaming.TrajectoryByPathRequest({
    linestringWkt: "LINESTRING (151.188277 -33.884699, 151.18862 -33.884707, 151.189805 -33.884734, 151.190091 -33.884743, 151.19063 -33.884758, 151.190909 -33.884747, 151.191247 -33.884724, 151.191281 -33.884723, 151.191439 -33.88471, 151.191552 -33.884699, 151.191722 -33.884682, 151.192145 -33.884643, 151.192449 -33.884608)",
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
        hourOfDay: Array.from(Array(24).keys()),  // 0 to 23
        excludeDate: Array(
            new time.LocalDate({
                    day: 10,
                    month: 10,
                    year: 2023
                }
            ),
            new time.LocalDate({
                    day: 11,
                    month: 10,
                    year: 2023
                }
            ),
        )
    })
})

for await (const response of client.trajectoryByPath(request)) {
    console.log(response.toJsonString({prettySpaces: 2}))
}
