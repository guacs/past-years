class _Context:
    """A class to hold the global context."""

    def __init__(self):

        self.request_id: str | None = None


ctx = _Context()
