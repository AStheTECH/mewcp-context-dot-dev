"""Configuration for MewCP Context.dev MCP Server."""

import logging
import os

SERVER_VERSION = "v1.0.0"
BREAKING_CHANGES: list[dict] = []

CONTEXT_DEV_API_BASE = "https://api.context.dev/v1"

CONNECT_TIMEOUT = 5    # TCP connection — fixed across all servers
# READ_TIMEOUT matches the server's previous fixed 60s socket timeout, which
# comfortably covers scrape/brand/extract calls under normal conditions. Note:
# tools also accept a `timeout_ms` parameter that is sent to Context.dev as an
# upstream processing budget (up to 300000ms) — it does not change this local
# socket timeout, so a request using a `timeout_ms` above ~55s risks a local
# timeout before Context.dev's own timeout fires. Pre-existing behavior,
# unchanged by this update.
READ_TIMEOUT = 60


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
