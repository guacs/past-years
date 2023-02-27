import time
from typing import Any
from uuid import uuid1

from past_years.api.request import Request
from falcon import Response
from loguru import logger

from past_years.context import ctx

START_TIME = "start-time"
REQUEST_ID_HEADER = "X-Request-Id"


class LogRequestMiddleware:
    """Logs all the requests."""

    def process_request(self, req: Request, resp: Response):
        """Creates a unique ID for each request and sets the start time of the
        request."""

        req.req_context.request_start_time = time.monotonic_ns()

        request_id = str(uuid1())
        ctx.request_id = request_id
        resp.set_header(REQUEST_ID_HEADER, ctx.request_id)

    def process_response(
        self, req: Request, resp: Response, resource: Any, request_success: bool
    ):
        """Logs the request after it's been processed.

        NOTE: Processes the request after it's been processed by the resource."""

        # NOTE: `elapsed_time` becomes -ve if the request was never
        # properly routed i.e. 404 HTTP Status.
        # This is because the start time is set to 0 by default.
        elapsed_time = time.monotonic_ns() - req.req_context.request_start_time
        logger.info(
            f"{req.method} {req.path} {resp.status} {elapsed_time}",
            request_id=ctx.request_id,
        )
