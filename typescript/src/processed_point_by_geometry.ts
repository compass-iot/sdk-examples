import * as time from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/time_pb"
import * as streaming from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"
import {RawRequestFilter} from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/streaming_pb"
import {Code, ConnectError} from "@connectrpc/connect"

import {createNodeClient} from "./client"
import {VehicleType} from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/vehicle_pb";

const client = createNodeClient()
type Client = typeof client

const request = new streaming.ProcessedPointByGeometryRequest({
    linestringOrPolygonWkt: "LINESTRING(151.18703722810923 -33.8695894847834,151.18361472940623 -33.868689747746664)",
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
        hourOfDay: Array.from(Array(24).keys()), // 0 to 23
        excludeDate: [new time.LocalDate({
            day: 2,
            month: 10,
            year: 2023
        }),
            new time.LocalDate({
                day: 11,
                month: 10,
                year: 2023
            }),
        ]
    }),
    // leave empty for no filters
    filters: [RawRequestFilter.UNSPECIFIED],
    // leave empty to get all vehicles
    vehicleTypeFilter: [VehicleType.VEHICLE_TYPE_UNSPECIFIED, VehicleType.BUS, VehicleType.CAR, VehicleType.LCV, VehicleType.HV,
        VehicleType.VAN, VehicleType.TRUCK, VehicleType.LV, VehicleType.CRANE, VehicleType.TRACTOR, VehicleType.TRAILER,
        VehicleType.LOADER, VehicleType.MOTORCYCLE, VehicleType.GARBAGE_TRUCK, VehicleType.MICROBUS, VehicleType.SUV, VehicleType.LOADER,
        VehicleType.PICKUP_TRUCK]
})

async function* paginateProcessedPoint(client: Client, req: streaming.ProcessedPointByGeometryRequest): AsyncIterable<streaming.ProcessedPoint> {
    let lastReceivedTimestamp = undefined
    let iterable = client.processedPointByGeometry({...req, lastReceivedTimestamp})
    for (; ;) {
        try {
            for await (const r of iterable) {
                lastReceivedTimestamp = r.timestamp
                yield r
            }
        } catch (err) {
            switch (ConnectError.from(err).code) {
                case Code.DeadlineExceeded:
                    console.log(`DeadlineExceeded, retrying stream`, Date.now().toString())
                    iterable = client.processedPointByGeometry({...req, lastReceivedTimestamp})
                    continue
                default:
                    throw err
            }
        }
        break
    }
}

for await (const response of paginateProcessedPoint(client, request)) {
    console.log(response.toJsonString({prettySpaces: 2}))
}
