"""Upstream API client for MewCP Context.dev MCP Server."""

import requests
from fastmcp_credentials import get_credentials

from context_dev_mcp.config import CONTEXT_DEV_API_BASE, CONTEXT_DEV_API_VERSION, API_TIMEOUT


def _api_key() -> str:
    cred = get_credentials()
    value = cred.fields.get("api_key") if cred.fields else None
    if not value:
        raise ValueError("Missing api_key credential")
    return value


def _auth_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json",
    }


def _clean(params: dict) -> dict:
    """Remove None values and empty collections so they are not sent to the API."""
    result = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, (list, dict)) and not v:
            continue
        result[k] = v
    return result


def make_get_request(endpoint: str, params: dict | None = None) -> dict:
    url = f"{CONTEXT_DEV_API_BASE}/{CONTEXT_DEV_API_VERSION}{endpoint}"
    resp = requests.get(
        url,
        headers=_auth_headers(),
        params=_clean(params or {}),
        timeout=API_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def make_post_request(endpoint: str, body: dict) -> dict:
    url = f"{CONTEXT_DEV_API_BASE}/{CONTEXT_DEV_API_VERSION}{endpoint}"
    resp = requests.post(
        url,
        headers=_auth_headers(),
        json=_clean(body),
        timeout=API_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()
