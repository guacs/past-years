from typing import NamedTuple


class RequestContext(NamedTuple):
    """A tuple to hold the various context per request."""

    compress: bool = False
    """Indicates whether to compress the response or not."""

    request_start_time: int = 0
    """The time the request was started to be processed."""
