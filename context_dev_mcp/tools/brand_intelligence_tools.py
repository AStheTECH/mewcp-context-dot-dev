"""Brand Intelligence group: get_brand_by_domain, get_brand_by_email, get_brand_by_name, identify_brand_from_transaction."""

import logging
from typing import Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from ..service import make_get_request
from ..schemas import BrandData, BrandResult
from ..logging_utils import ToolLogger
from ._helpers import _handle_request_exc

logger = logging.getLogger(__name__)


def register_brand_intelligence_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_brand_by_domain",
        description=(
            "Retrieve rich brand data for a company domain: logos, colors, backdrops, "
            "description, social links, address, stock ticker, and industry classification."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_brand_by_domain(
        domain: str = Field(..., description="Domain to look up (e.g. 'stripe.com', 'apple.com')"),
        force_language: Optional[str] = Field(None, description="ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')"),
        max_speed: Optional[bool] = Field(None, description="Optimize for speed by skipping comprehensive data enrichment"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 7776000000 = ~3 months)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> BrandResult:
        tlog = ToolLogger(logger, "get_brand_by_domain")
        params: dict = {"domain": domain}
        if force_language:
            params["force_language"] = force_language
        if max_speed is not None:
            params["maxSpeed"] = max_speed
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        try:
            raw = make_get_request("/brand/retrieve", params)
        except Exception as exc:
            return _handle_request_exc(BrandResult, tlog, exc)
        tlog.success()
        return BrandResult(success=True, statusCode=200, data=BrandData(**raw))

    @mcp.tool(
        name="get_brand_by_email",
        description=(
            "Retrieve brand data for the company associated with an email address. "
            "Returns an error for free (Gmail, Outlook) or disposable email addresses."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_brand_by_email(
        email: str = Field(..., description="Email address to look up (e.g. 'contact@stripe.com')"),
        force_language: Optional[str] = Field(None, description="ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')"),
        max_speed: Optional[bool] = Field(None, description="Optimize for speed by skipping comprehensive data enrichment"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 86400000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> BrandResult:
        tlog = ToolLogger(logger, "get_brand_by_email")
        params: dict = {"email": email}
        if force_language:
            params["force_language"] = force_language
        if max_speed is not None:
            params["maxSpeed"] = max_speed
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        try:
            raw = make_get_request("/brand/retrieve-by-email", params)
        except Exception as exc:
            return _handle_request_exc(BrandResult, tlog, exc)
        tlog.success()
        return BrandResult(success=True, statusCode=200, data=BrandData(**raw))

    @mcp.tool(
        name="get_brand_by_name",
        description=(
            "Retrieve brand data for a company by its name. Useful when only the company name "
            "is known. Name must be 3–30 characters."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_brand_by_name(
        name: str = Field(..., min_length=3, max_length=30, description="Company name to look up (e.g. 'Stripe', 'Apple Inc')"),
        country_gl: Optional[str] = Field(None, description="ISO 3166-1 alpha-2 country code to improve matching (e.g. 'US', 'GB')"),
        force_language: Optional[str] = Field(None, description="ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')"),
        max_speed: Optional[bool] = Field(None, description="Optimize for speed by skipping comprehensive data enrichment"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 86400000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> BrandResult:
        tlog = ToolLogger(logger, "get_brand_by_name")
        params: dict = {"name": name}
        if country_gl:
            params["country_gl"] = country_gl
        if force_language:
            params["force_language"] = force_language
        if max_speed is not None:
            params["maxSpeed"] = max_speed
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        try:
            raw = make_get_request("/brand/retrieve-by-name", params)
        except Exception as exc:
            return _handle_request_exc(BrandResult, tlog, exc)
        tlog.success()
        return BrandResult(success=True, statusCode=200, data=BrandData(**raw))

    @mcp.tool(
        name="identify_brand_from_transaction",
        description=(
            "Identify a company from a bank transaction description or merchant string "
            "(e.g. 'AMZN*123456', 'UBER* EATS', 'SQ *COFFEE SHOP'). Returns full brand data."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def identify_brand_from_transaction(
        transaction_info: str = Field(..., description="Raw transaction or merchant string to identify (e.g. 'AMZN*123456 SEATTLE WA')"),
        country_gl: Optional[str] = Field(None, description="ISO 3166-1 alpha-2 country code for geographic context (e.g. 'US', 'GB')"),
        city: Optional[str] = Field(None, description="City name from the transaction to improve matching"),
        mcc: Optional[str] = Field(None, description="Merchant Category Code (MCC) to narrow the industry search"),
        high_confidence_only: Optional[bool] = Field(None, description="Run additional verification to return only high-confidence matches (default: false)"),
        force_language: Optional[str] = Field(None, description="ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')"),
        max_speed: Optional[bool] = Field(None, description="Optimize for speed by skipping comprehensive data enrichment"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> BrandResult:
        tlog = ToolLogger(logger, "identify_brand_from_transaction")
        params: dict = {"transaction_info": transaction_info}
        if country_gl:
            params["country_gl"] = country_gl
        if city:
            params["city"] = city
        if mcc:
            params["mcc"] = mcc
        if high_confidence_only is not None:
            params["high_confidence_only"] = high_confidence_only
        if force_language:
            params["force_language"] = force_language
        if max_speed is not None:
            params["maxSpeed"] = max_speed
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        try:
            raw = make_get_request("/brand/transaction_identifier", params)
        except Exception as exc:
            return _handle_request_exc(BrandResult, tlog, exc)
        tlog.success()
        return BrandResult(success=True, statusCode=200, data=BrandData(**raw))
