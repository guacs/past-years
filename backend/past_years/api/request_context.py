from dataclasses import dataclass


@dataclass
class RequestContext:
    """A tuple to hold the various context per request."""

    compress: bool = True
    """Indicates whether to compress the response or not."""

    request_start_time: int = 0
    """The time the request was started to be processed."""
