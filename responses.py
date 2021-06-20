from starlette.responses import Response
import msgpack

class MsgpackResponse(Response):
  media_type = 'application/x-msgpack'

  def render(self, content: dict) -> bytes:
    return msgpack.packb(content)
