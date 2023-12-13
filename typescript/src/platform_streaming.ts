import { RealtimeRawPointByGeometryRequest, StreamEnvironment } from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"

import client from "./client"

const request = new RealtimeRawPointByGeometryRequest({
    boundsWkt: "POLYGON ((151.116490002445 -34.136652437446564, 150.76133775468065 -33.970878990313345, 150.8238645588653 -33.68832143811975, 150.93391173422782 -33.51542003355166, 151.17151359012706 -33.594622738528074, 151.3165757758332 -33.67583417052261, 151.3115736314981 -33.80478175152794, 151.22903824997502 -34.03515466768564, 151.116490002445 -34.136652437446564))",
    streamEnv: StreamEnvironment.DEV,
})

for await (const response of client.realtimeRawPointByGeometry(request)) {
    console.log(response.toJsonString({ prettySpaces: 2 }))
}
