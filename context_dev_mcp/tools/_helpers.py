"""Shared error helpers for all tool modules.

Adapted for context_dev_mcp's raw `requests`-based service layer
(`service.make_get_request` / `service.make_post_request`), which calls
`resp.raise_for_status()` and therefore raises `requests.HTTPError` /
`requests.RequestException` (including `requests.Timeout`) instead of
returning `(data, status, retry_after)` tuples. `service._api_key()` raises
`ValueError("Missing api_key credential")` when no credential is configured.
"""

from __future__ import annotations

import requests

from ..logging_utils import ToolLogger
from ..schemas import ToolError


def _err(
    result_class,
    tlog: ToolLogger,
    code: str,
    message: str,
    status: int,
    retriable: bool = False,
    retry_after: int | None = None,
):
    """Build a failure result and log it. Use for VALIDATION_ERROR guards etc."""
    tlog.failure(code, message)
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code=code, message=message),
    )


def _upstream_err(result_class, tlog: ToolLogger, exc: requests.exceptions.HTTPError):
    """Map a `requests.HTTPError` (raised by `resp.raise_for_status()`) to a failure result."""
    resp = exc.response
    status = resp.status_code if resp is not None else 502

    retry_after: int | None = None
    upstream_message = None
    if resp is not None:
        retry_after_header = resp.headers.get("Retry-After")
        if retry_after_header is not None:
            try:
                retry_after = int(retry_after_header)
            except ValueError:
                retry_after = None
        try:
            data = resp.json()
        except ValueError:
            data = None
        if isinstance(data, dict):
            upstream_message = data.get("error") or data.get("message")

    if status in (401, 403):
        code, retriable = "AUTH_ERROR", False
    elif status == 429:
        code, retriable = "RATE_LIMIT", True
    elif status >= 500:
        code, retriable = "UPSTREAM_ERROR", True
    else:
        code, retriable = "UPSTREAM_ERROR", False

    log_message = f"HTTP {status}"
    tlog.failure(code, log_message)  # log the status, not str(exc)
    message = str(upstream_message) if upstream_message else log_message
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code=code, message=message),
    )


def _handle_request_exc(result_class, tlog: ToolLogger, exc: Exception):
    """Map any exception raised while calling `service.make_get_request` /
    `service.make_post_request` (or `service._api_key()`) to a failure result."""
    if isinstance(exc, requests.exceptions.Timeout):
        return _err(result_class, tlog, "REQUEST_TIMEOUT", "Request to upstream API timed out",
                    408, retriable=True)
    if isinstance(exc, requests.exceptions.HTTPError):
        return _upstream_err(result_class, tlog, exc)
    if isinstance(exc, requests.exceptions.RequestException):
        tlog.failure("UPSTREAM_ERROR", "Network error")
        return result_class(success=False, statusCode=503, retriable=True,
            error=ToolError(code="UPSTREAM_ERROR", message=str(exc)))
    if isinstance(exc, ValueError):
        # e.g. service._api_key() -> ValueError("Missing api_key credential")
        tlog.failure("AUTH_ERROR", str(exc))
        return result_class(success=False, statusCode=401, retriable=False,
            error=ToolError(code="AUTH_ERROR", message=str(exc)))
    tlog.failure("SERVER_ERROR", str(exc))  # log full detail internally
    return result_class(success=False, statusCode=500, retriable=False,
        error=ToolError(code="SERVER_ERROR", message="Unexpected server error"))
