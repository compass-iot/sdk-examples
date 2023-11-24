from grpclib.client import Channel
from sdk.gateway.v1 import ServiceStub


async def get_access_token(host: str, secret: str):
  channel = Channel(host)
  service = ServiceStub(channel)

  auth = await service.authenticate(token=secret)
  channel.close()

  return auth.access_token
