import gzip

from falcon import Response

from past_years.api.request import Request


class CompressionMiddleware:
    """Handles compressing the responses."""

    _COMPRESSION = "gzip"

    def process_response(self, req: Request, resp: Response, _, req_success: bool):
        """Compresses the response data.

        If the request is not successful or the `compress` key in
        the `req.context` is explicitly set to `False`, no compression
        is done.
        """

        if not req_success or not req.req_context.compress:
            return

        content_encoding: str | None = req.get_header("accept-encoding")
        if not content_encoding or self._COMPRESSION not in content_encoding:
            return

        data = resp.render_body()
        if not data:
            return

        assert isinstance(data, bytes)
        resp.data = gzip.compress(data)
        resp.set_header("content-encoding", self._COMPRESSION)
