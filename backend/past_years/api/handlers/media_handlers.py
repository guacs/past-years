from typing import Any
from falcon.media import BaseHandler
import falcon

import msgspec


class MsgPackHandler(BaseHandler):
    """A custom MsgPack handler using `msgspec`."""

    _encoder = msgspec.msgpack.Encoder()

    def serialize(self, media: Any, content_type: str) -> bytes:
        """Serializes the media into `msgpack` if the content-type
        is `application/msgpack`."""

        assert content_type == falcon.MEDIA_MSGPACK
        return self._encoder.encode(media)


class JSONHandler(BaseHandler):
    """A custom JSON handler using `msgspec`."""

    _encoder = msgspec.json.Encoder()
    _decoder = msgspec.json.Decoder()

    def serialize(self, media: Any, content_type: str) -> bytes:
        assert content_type == falcon.MEDIA_JSON
        return self._encoder.encode(media)

    def deserialize(self, stream, content_type, content_length) -> object:
        return self._decoder.decode(stream.read())
