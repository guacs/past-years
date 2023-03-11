from typing import Any
from wsgiref.simple_server import WSGIRequestHandler

import dotenv
from api import make_app
from falcon import App
from loguru import logger
from utils import configure_logger


def initialize_application() -> App:
    dotenv.load_dotenv()
    configure_logger()
    return make_app()


application = initialize_application()

if __name__ == "__main__":
    # THIS IS ONLY MEANT FOR DEVELOPMENT PURPOSES!!
    from wsgiref import simple_server

    class SilentServerHandler(WSGIRequestHandler):
        """A silent server that does not log any messages of its own."""

        def log_message(self, format: str, *args: Any) -> None:
            pass

    PORT = 8080

    logger.info(f"Listening on port {PORT}")
    with simple_server.make_server(
        "", PORT, application, handler_class=SilentServerHandler
    ) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.critical("Shutting down...")
            httpd.server_close()
