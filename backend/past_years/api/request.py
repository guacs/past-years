from typing import Literal
from falcon import Request as FalconRequest
from falcon import MEDIA_JSON, MEDIA_MSGPACK

from .request_context import RequestContext

MEDIA_TYPES = Literal["application/json", "application/msgpack"]


class Request(FalconRequest):
    def __init__(self, env, options=None):

        super().__init__(env, options)

        self.req_context = RequestContext()

    def get_accepted_content_type(self) -> MEDIA_TYPES:
        """Returns the content-type to use on the response data.

        By default, all clients are assumed to accept JSON.
        """

        if self.client_accepts_msgpack:
            return MEDIA_MSGPACK

        return MEDIA_JSON
