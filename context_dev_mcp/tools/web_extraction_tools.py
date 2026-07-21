"""Web Extraction group: extract_structured_data, scrape_styleguide, scrape_fonts."""

import json
import logging
from typing import Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas import ExtractData, ExtractResult, FontsData, FontsResult, StyleguideData, StyleguideResult
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("context-dev-mcp.tools.web_extraction")


def register_web_extraction_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="extract_structured_data",
        description=(
            "Crawl a website and extract structured data conforming to a JSON Schema. "
            "Ideal for scraping product info, pricing tables, contact details, team pages, "
            "or any structured content. Up to 50 pages per call."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def extract_structured_data(
        url: str = Field(..., description="Starting URL to crawl, including http:// or https://"),
        schema_json: str = Field(..., description='JSON Schema (as a JSON string) defining the structure of data to extract. Example: \'{"type":"object","properties":{"title":{"type":"string"},"price":{"type":"number"}}}\''),
        instructions: Optional[str] = Field(None, max_length=2000, description="Natural-language extraction instructions to guide the model (max 2000 characters)"),
        fact_check: Optional[bool] = Field(None, description="When true, values must be grounded in page content — reduces hallucination (default: false)"),
        follow_subdomains: Optional[bool] = Field(None, description="Follow links on subdomains of the starting URL (default: false)"),
        max_pages: Optional[int] = Field(None, ge=1, le=50, description="Maximum number of pages to analyze (1–50, default: 5)"),
        max_depth: Optional[int] = Field(None, description="Maximum link depth from the starting URL"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 604800000 = 7 days)"),
        wait_for_ms: Optional[int] = Field(None, ge=0, le=30000, description="Milliseconds to wait after page load for JavaScript rendering (0–30000)"),
        stop_after_ms: Optional[int] = Field(None, ge=10000, le=110000, description="Crawl time budget in milliseconds (10000–110000, default: 80000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> ExtractResult:
        tlog = ToolLogger(logger, "extract_structured_data")

        try:
            schema_dict = json.loads(schema_json)
        except json.JSONDecodeError as e:
            return _err(ExtractResult, tlog, "VALIDATION_ERROR", f"Invalid JSON schema: {e}", 400)

        body: dict = {"url": url, "schema": schema_dict}
        if instructions:
            body["instructions"] = instructions
        if fact_check is not None:
            body["factCheck"] = fact_check
        if follow_subdomains is not None:
            body["followSubdomains"] = follow_subdomains
        if max_pages is not None:
            body["maxPages"] = max_pages
        if max_depth is not None:
            body["maxDepth"] = max_depth
        if max_age_ms is not None:
            body["maxAgeMs"] = max_age_ms
        if wait_for_ms is not None:
            body["waitForMs"] = wait_for_ms
        if stop_after_ms is not None:
            body["stopAfterMs"] = stop_after_ms
        if timeout_ms is not None:
            body["timeoutMS"] = timeout_ms

        try:
            data, status, retry_after = service.api_request(
                "POST", "/web/extract", body=body, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )
        except Exception as exc:
            return _handle_request_exc(ExtractResult, tlog, exc)

        if 200 <= status < 300:
            tlog.success()
            return ExtractResult(success=True, statusCode=status, data=ExtractData(**data))
        return _upstream_err(ExtractResult, tlog, status, data, retry_after)

    @mcp.tool(
        name="scrape_styleguide",
        description=(
            "Extract a website's design system: brand colors, typography (font families, "
            "sizes, weights), element spacing, shadows, button styles, and font CDN links."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def scrape_styleguide(
        domain: Optional[str] = Field(None, description="Domain name to extract styleguide from (e.g. 'stripe.com'). Either domain or direct_url is required."),
        direct_url: Optional[str] = Field(None, description="Specific URL to extract styleguide from. Either domain or direct_url is required."),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 7776000000 = ~3 months)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> StyleguideResult:
        tlog = ToolLogger(logger, "scrape_styleguide")

        if not domain and not direct_url:
            return _err(StyleguideResult, tlog, "VALIDATION_ERROR", "Provide either 'domain' or 'direct_url'", 400)

        params: dict = {}
        if domain:
            params["domain"] = domain
        if direct_url:
            params["directUrl"] = direct_url
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms

        try:
            data, status, retry_after = service.api_request(
                "GET", "/web/styleguide", params=params, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )
        except Exception as exc:
            return _handle_request_exc(StyleguideResult, tlog, exc)

        if 200 <= status < 300:
            tlog.success()
            return StyleguideResult(success=True, statusCode=status, data=StyleguideData(**data))
        return _upstream_err(StyleguideResult, tlog, status, data, retry_after)

    @mcp.tool(
        name="scrape_fonts",
        description=(
            "Extract all font families used on a website along with usage statistics, "
            "CSS selectors, fallback fonts, and CDN asset links (Google Fonts or custom)."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def scrape_fonts(
        domain: Optional[str] = Field(None, description="Domain name to extract fonts from (e.g. 'stripe.com'). Either domain or direct_url is required."),
        direct_url: Optional[str] = Field(None, description="Specific URL to extract fonts from. Either domain or direct_url is required."),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 7776000000 = ~3 months)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> FontsResult:
        tlog = ToolLogger(logger, "scrape_fonts")

        if not domain and not direct_url:
            return _err(FontsResult, tlog, "VALIDATION_ERROR", "Provide either 'domain' or 'direct_url'", 400)

        params: dict = {}
        if domain:
            params["domain"] = domain
        if direct_url:
            params["directUrl"] = direct_url
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms

        try:
            data, status, retry_after = service.api_request(
                "GET", "/web/fonts", params=params, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )
        except Exception as exc:
            return _handle_request_exc(FontsResult, tlog, exc)

        if 200 <= status < 300:
            tlog.success()
            return FontsResult(success=True, statusCode=status, data=FontsData(**data))
        return _upstream_err(FontsResult, tlog, status, data, retry_after)
