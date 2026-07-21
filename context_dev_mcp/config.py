"""Configuration for MewCP Context.dev MCP Server."""

import logging

SERVER_VERSION = "v1.0.0"
BREAKING_CHANGES: list[dict] = []

CONTEXT_DEV_API_BASE = "https://api.context.dev"
CONTEXT_DEV_API_VERSION = "v1"
API_TIMEOUT = 60


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
