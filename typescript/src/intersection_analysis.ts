import * as geo from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/geo_pb"
import * as time from "@buf/compassiot_model.bufbuild_es/compassiot/compass/v1/time_pb"
import * as unary from "@buf/compassiot_api.bufbuild_es/compassiot/platform/v1/unary_pb"

import { createNodeClient } from "./client"

const client = createNodeClient()

const request = new unary.IntersectionRequest({
	intersectionCenter: new geo.LatLng({
		lat: -33.87973611766243,
		lng: 151.2091378332539
	}),
	intersectionRadius: 26,
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

const response = await client.intersectionAnalysis(request)

console.log(response.toJsonString({ prettySpaces: 2 }))
