import requests
from fastmcp_credentials import get_credentials
from context_dev_mcp.config import CONTEXT_DEV_API_BASE, CONTEXT_DEV_API_VERSION, API_TIMEOUT


def _api_key() -> str:
    return get_credentials().fields["api_key"]


def _auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {_api_key()}"}


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
    try:
        resp = requests.get(
            url,
            headers=_auth_headers(),
            params=_clean(params or {}),
            timeout=API_TIMEOUT,
        )
        if resp.ok:
            return resp.json()
        try:
            err = resp.json()
        except Exception:
            err = {}
        return {
            "error": True,
            "status_code": resp.status_code,
            "message": err.get("message", resp.text),
            "error_code": err.get("error_code", "UNKNOWN"),
        }
    except requests.Timeout:
        return {"error": True, "error_code": "REQUEST_TIMEOUT", "message": "Request timed out"}
    except Exception as e:
        return {"error": True, "error_code": "INTERNAL_ERROR", "message": str(e)}


def make_post_request(endpoint: str, body: dict) -> dict:
    url = f"{CONTEXT_DEV_API_BASE}/{CONTEXT_DEV_API_VERSION}{endpoint}"
    try:
        resp = requests.post(
            url,
            headers=_auth_headers(),
            json=_clean(body),
            timeout=API_TIMEOUT,
        )
        if resp.ok:
            return resp.json()
        try:
            err = resp.json()
        except Exception:
            err = {}
        return {
            "error": True,
            "status_code": resp.status_code,
            "message": err.get("message", resp.text),
            "error_code": err.get("error_code", "UNKNOWN"),
        }
    except requests.Timeout:
        return {"error": True, "error_code": "REQUEST_TIMEOUT", "message": "Request timed out"}
    except Exception as e:
        return {"error": True, "error_code": "INTERNAL_ERROR", "message": str(e)}
