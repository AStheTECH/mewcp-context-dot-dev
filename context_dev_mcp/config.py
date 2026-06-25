import logging

CONTEXT_DEV_API_BASE = "https://api.context.dev"
CONTEXT_DEV_API_VERSION = "v1"
API_TIMEOUT = 60


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
