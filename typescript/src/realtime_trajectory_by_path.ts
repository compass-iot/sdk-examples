import * as streaming from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"

import {createNodeClient} from "./client"

const client = createNodeClient()
const request = new streaming.RealtimeTrajectoryByPathRequest({
    linestringWkt: "LINESTRING (151.188277 -33.884699, 151.18862 -33.884707, 151.189805 -33.884734, 151.190091 -33.884743, 151.19063 -33.884758, 151.190909 -33.884747, 151.191247 -33.884724, 151.191281 -33.884723, 151.191439 -33.88471, 151.191552 -33.884699, 151.191722 -33.884682, 151.192145 -33.884643, 151.192449 -33.884608)",
})

for await (const response of client.realtimeTrajectoryByPath(request)) {
    console.log(response.toJsonString({prettySpaces: 2}))
}
