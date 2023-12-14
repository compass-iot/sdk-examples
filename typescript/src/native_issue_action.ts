import * as native from "@buf/compassiot_api.bufbuild_es/compassiot/native/v1/native_pb"

import client from "./client"

const request = new native.IssueActionRequest({
  vin: "",
  command: {
    case: "lock",
    value: new native.SetLockCommand({
      locked: true
    })
  }
})

// Returns empty
await client.nativeIssueAction(request)
