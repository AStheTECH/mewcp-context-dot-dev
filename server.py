import json
import os

from dotenv import load_dotenv
load_dotenv()

from fastmcp import FastMCP
from fastmcp_credentials import CredentialMiddleware, HeaderCredentialBackend
from context_dev_mcp.cli import parse_args
from context_dev_mcp.tools import register_tools

backend = HeaderCredentialBackend()
mcp = FastMCP(
    "MewCP Context.dev MCP Server",
    middleware=[CredentialMiddleware(backend, "static")],
)
register_tools(mcp)

_base_app = mcp.http_app(path="/mcp", transport="streamable-http", stateless_http=True)
_dev_key = os.getenv("CONTEXT_DEV_API_KEY")


class _DevCredentialInjector:
    """Auto-injects X-Mcp-Cred-Fields from CONTEXT_DEV_API_KEY env var when the
    header is absent. Only active in dev (when the env var is set). In production
    the gateway injects the header and this wrapper is not used."""

    def __init__(self, inner):
        self._inner = inner

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = list(scope.get("headers", []))
            if not any(k.lower() == b"x-mcp-cred-fields" for k, _ in headers):
                value = json.dumps({"api_key": _dev_key}).encode()
                headers.append((b"x-mcp-cred-fields", value))
                scope = {**scope, "headers": headers}
        await self._inner(scope, receive, send)


# Production: plain ASGI app (gateway injects headers).
# Dev: wrapped app (env var injects headers automatically).
app = _DevCredentialInjector(_base_app) if _dev_key else _base_app


if __name__ == "__main__":
    import uvicorn

    args = parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        uvicorn.run(
            app,
            host=args.host or "0.0.0.0",
            port=args.port or 8000,
        )
