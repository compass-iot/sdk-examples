import { RealtimeRawPointByGeometryRequest, StreamEnvironment } from "@buf/compassiot_model.bufbuild_es/platform/v1/streaming_pb"
import createGatewayClient from "./client"
import throttle from "./throttle"

const req = new RealtimeRawPointByGeometryRequest({
  boundsWkt: "POLYGON ((151.116490002445 -34.136652437446564, 150.76133775468065 -33.970878990313345, 150.8238645588653 -33.68832143811975, 150.93391173422782 -33.51542003355166, 151.17151359012706 -33.594622738528074, 151.3165757758332 -33.67583417052261, 151.3115736314981 -33.80478175152794, 151.22903824997502 -34.03515466768564, 151.116490002445 -34.136652437446564))",
  streamEnv: StreamEnvironment.DEV,
})

const client = createGatewayClient("https://api.compassiot.cloud", "...insert client secret here...")
console.log("Connecting to Gateway...")

// The only difference between this example & streaming.ts
// is the usage of `throttle(client..., duration)` to limit
// the rate of message consumption (e.g. rendering on front-end).
// Below, we're capping the rate to 1 per second, but you can adjust
// to say, `100 milliseconds` by passing `{ value: 100, unit: "ms" }`
for await (const res of throttle(client.realtimeRawPointByGeometry(req), { value: 1, unit: "s" })) {
  console.log(res.toJsonString({ prettySpaces: 2 }))
}
