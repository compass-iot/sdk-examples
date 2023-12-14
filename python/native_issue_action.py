from client import create_gateway_client
import compassiot.native.v1.native_pb2 as native


def main():
    client = create_gateway_client()

    request = native.IssueActionRequest(
        vin="",
        lock=native.SetLockCommand(
            locked=True
        )
    )

    client.NativeIssueAction(request)

     
if __name__ == "__main__":
    main()
