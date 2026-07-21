"""Web Scraping group: scrape_html, scrape_markdown, scrape_screenshot, scrape_images, crawl_sitemap, web_search."""

import logging
from typing import Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from ..service import make_get_request, make_post_request
from ..logging_utils import ToolLogger
from ..schemas import (
    ScrapeHtmlData,
    ScrapeHtmlResult,
    ScrapeMarkdownData,
    ScrapeMarkdownResult,
    ScrapeScreenshotData,
    ScrapeScreenshotResult,
    ScrapeImagesData,
    ScrapeImagesResult,
    CrawlSitemapData,
    CrawlSitemapResult,
    WebSearchData,
    WebSearchResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger(__name__)


def register_web_scraping_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="scrape_html",
        description=(
            "Scrape a URL and return its raw HTML content. Supports web pages, PDFs, "
            "XML, JSON, Markdown, CSV, and SVG files."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def scrape_html(
        url: str = Field(..., description="Full URL to scrape, including http:// or https://"),
        include_frames: Optional[bool] = Field(None, description="Render iframes inline in the returned HTML"),
        use_main_content_only: Optional[bool] = Field(None, description="Extract only the main content area, stripping navigation, ads, and footers"),
        include_selectors: Optional[str] = Field(None, description="Comma-separated CSS selectors to keep (e.g. 'article,.main-content'). Max 50 selectors."),
        exclude_selectors: Optional[str] = Field(None, description="Comma-separated CSS selectors to remove (e.g. 'nav,footer,.ads'). Max 50 selectors."),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds. 0 = always fetch fresh. Default: 86400000 (1 day)."),
        wait_for_ms: Optional[int] = Field(None, ge=0, le=30000, description="Milliseconds to wait after page load for JavaScript rendering (0–30000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> ScrapeHtmlResult:
        tlog = ToolLogger(logger, "scrape_html")

        params: dict = {"url": url}
        if include_frames is not None:
            params["includeFrames"] = include_frames
        if use_main_content_only is not None:
            params["useMainContentOnly"] = use_main_content_only
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if wait_for_ms is not None:
            params["waitForMs"] = wait_for_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        if include_selectors:
            params["includeSelectors"] = [s.strip() for s in include_selectors.split(",") if s.strip()]
        if exclude_selectors:
            params["excludeSelectors"] = [s.strip() for s in exclude_selectors.split(",") if s.strip()]

        try:
            raw = make_get_request("/web/scrape/html", params)
            tlog.success()
            return ScrapeHtmlResult(success=True, statusCode=200, data=ScrapeHtmlData(**raw))
        except Exception as exc:
            return _handle_request_exc(ScrapeHtmlResult, tlog, exc)

    @mcp.tool(
        name="scrape_markdown",
        description=(
            "Scrape a URL and return its content converted to clean, LLM-ready Markdown. "
            "Strips boilerplate and preserves headings, links, and structure."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def scrape_markdown(
        url: str = Field(..., description="Full URL to scrape, including http:// or https://"),
        include_links: Optional[bool] = Field(None, description="Preserve hyperlinks in the Markdown output (default: true)"),
        include_images: Optional[bool] = Field(None, description="Include image references in the Markdown output (default: false)"),
        use_main_content_only: Optional[bool] = Field(None, description="Extract only the main content area, stripping navigation, ads, and footers"),
        include_frames: Optional[bool] = Field(None, description="Render iframe contents into the Markdown"),
        include_selectors: Optional[str] = Field(None, description="Comma-separated CSS selectors to keep (e.g. 'article,.main-content'). Max 50 selectors."),
        exclude_selectors: Optional[str] = Field(None, description="Comma-separated CSS selectors to remove (e.g. 'nav,footer,.ads'). Max 50 selectors."),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds. 0 = always fetch fresh. Default: 86400000 (1 day)."),
        wait_for_ms: Optional[int] = Field(None, ge=0, le=30000, description="Milliseconds to wait after page load for JavaScript rendering (0–30000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> ScrapeMarkdownResult:
        tlog = ToolLogger(logger, "scrape_markdown")

        params: dict = {"url": url}
        if include_links is not None:
            params["includeLinks"] = include_links
        if include_images is not None:
            params["includeImages"] = include_images
        if use_main_content_only is not None:
            params["useMainContentOnly"] = use_main_content_only
        if include_frames is not None:
            params["includeFrames"] = include_frames
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if wait_for_ms is not None:
            params["waitForMs"] = wait_for_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        if include_selectors:
            params["includeSelectors"] = [s.strip() for s in include_selectors.split(",") if s.strip()]
        if exclude_selectors:
            params["excludeSelectors"] = [s.strip() for s in exclude_selectors.split(",") if s.strip()]

        try:
            raw = make_get_request("/web/scrape/markdown", params)
            tlog.success()
            return ScrapeMarkdownResult(success=True, statusCode=200, data=ScrapeMarkdownData(**raw))
        except Exception as exc:
            return _handle_request_exc(ScrapeMarkdownResult, tlog, exc)

    @mcp.tool(
        name="scrape_screenshot",
        description=(
            "Capture a visual screenshot of a website. Provide either 'domain' for the "
            "homepage or 'direct_url' for a specific page. Returns a URL to the screenshot image."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def scrape_screenshot(
        domain: Optional[str] = Field(None, description="Domain name to screenshot (e.g. 'example.com'). Either domain or direct_url is required."),
        direct_url: Optional[str] = Field(None, description="Specific URL to screenshot directly (e.g. 'https://example.com/pricing'). Either domain or direct_url is required."),
        full_screenshot: Optional[bool] = Field(None, description="Capture the full scrollable page instead of just the viewport"),
        handle_cookie_popup: Optional[bool] = Field(None, description="Automatically dismiss cookie consent popups before capturing"),
        viewport_width: Optional[int] = Field(None, ge=240, le=7680, description="Viewport width in pixels (240–7680, default: 1920)"),
        viewport_height: Optional[int] = Field(None, ge=240, le=4320, description="Viewport height in pixels (240–4320, default: 1080)"),
        page: Optional[str] = Field(None, description="Named page to capture. One of: login, signup, blog, careers, pricing, terms, privacy, contact"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 86400000)"),
        wait_for_ms: Optional[int] = Field(None, ge=0, le=30000, description="Milliseconds to wait after page load (0–30000, default: 3000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> ScrapeScreenshotResult:
        tlog = ToolLogger(logger, "scrape_screenshot")

        if not domain and not direct_url:
            return _err(ScrapeScreenshotResult, tlog, "VALIDATION_ERROR", "Provide either 'domain' or 'direct_url'", 400)
        valid_pages = {"login", "signup", "blog", "careers", "pricing", "terms", "privacy", "contact"}
        if page and page not in valid_pages:
            return _err(
                ScrapeScreenshotResult, tlog, "VALIDATION_ERROR",
                f"'page' must be one of: {', '.join(sorted(valid_pages))}", 400,
            )

        params: dict = {}
        if domain:
            params["domain"] = domain
        if direct_url:
            params["directUrl"] = direct_url
        if full_screenshot is not None:
            params["fullScreenshot"] = str(full_screenshot).lower()
        if handle_cookie_popup is not None:
            params["handleCookiePopup"] = str(handle_cookie_popup).lower()
        if viewport_width is not None or viewport_height is not None:
            viewport: dict = {}
            if viewport_width is not None:
                viewport["width"] = viewport_width
            if viewport_height is not None:
                viewport["height"] = viewport_height
            params["viewport"] = viewport
        if page:
            params["page"] = page
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if wait_for_ms is not None:
            params["waitForMs"] = wait_for_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms

        try:
            raw = make_get_request("/web/screenshot", params)
            tlog.success()
            return ScrapeScreenshotResult(success=True, statusCode=200, data=ScrapeScreenshotData(**raw))
        except Exception as exc:
            return _handle_request_exc(ScrapeScreenshotResult, tlog, exc)

    @mcp.tool(
        name="scrape_images",
        description=(
            "Collect all images from a URL: img tags, SVGs, CSS backgrounds, video posters, "
            "and meta images. Returns each image's src, element type, and optional metadata."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def scrape_images(
        url: str = Field(..., description="Full page URL to inspect, including http:// or https://"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 86400000)"),
        wait_for_ms: Optional[int] = Field(None, ge=0, le=30000, description="Milliseconds to wait after page load for JavaScript rendering (0–30000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> ScrapeImagesResult:
        tlog = ToolLogger(logger, "scrape_images")

        params: dict = {"url": url}
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if wait_for_ms is not None:
            params["waitForMs"] = wait_for_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms

        try:
            raw = make_get_request("/web/scrape/images", params)
            tlog.success()
            return ScrapeImagesResult(success=True, statusCode=200, data=ScrapeImagesData(**raw))
        except Exception as exc:
            return _handle_request_exc(ScrapeImagesResult, tlog, exc)

    @mcp.tool(
        name="crawl_sitemap",
        description=(
            "Discover all pages on a website by crawling its XML sitemaps. "
            "Returns a list of URLs up to maxLinks (default 10,000)."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def crawl_sitemap(
        domain: str = Field(..., description="Domain to build a sitemap for (e.g. 'example.com')"),
        max_links: Optional[int] = Field(None, ge=1, le=100000, description="Maximum number of URLs to return (1–100000, default: 10000)"),
        url_regex: Optional[str] = Field(None, max_length=256, description="RE2-compatible regex to filter URLs (e.g. '/blog/'). Max 256 characters."),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> CrawlSitemapResult:
        tlog = ToolLogger(logger, "crawl_sitemap")

        params: dict = {"domain": domain}
        if max_links is not None:
            params["maxLinks"] = max_links
        if url_regex:
            params["urlRegex"] = url_regex
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms

        try:
            raw = make_get_request("/web/scrape/sitemap", params)
            tlog.success()
            return CrawlSitemapResult(success=True, statusCode=200, data=CrawlSitemapData(**raw))
        except Exception as exc:
            return _handle_request_exc(CrawlSitemapResult, tlog, exc)

    @mcp.tool(
        name="web_search",
        description=(
            "Search the web with a natural-language query. Optionally scrapes each result "
            "page to Markdown for deeper content. Returns ranked results with url, title, "
            "description, and relevance."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def web_search(
        query: str = Field(..., min_length=1, max_length=500, description="Natural-language search query (1–500 characters)"),
        include_domains: Optional[str] = Field(None, description="Comma-separated domains to restrict results to (e.g. 'github.com,stackoverflow.com')"),
        exclude_domains: Optional[str] = Field(None, description="Comma-separated domains to exclude from results"),
        freshness: Optional[str] = Field(None, description="Limit results by age. One of: last_24_hours, last_week, last_month, last_year"),
        query_fanout: Optional[bool] = Field(None, description="Expand the query into parallel variants for broader coverage"),
        scrape_results: Optional[bool] = Field(None, description="Scrape each result page to Markdown and include it in the response"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> WebSearchResult:
        tlog = ToolLogger(logger, "web_search")

        valid_freshness = {"last_24_hours", "last_week", "last_month", "last_year"}
        if freshness and freshness not in valid_freshness:
            return _err(
                WebSearchResult, tlog, "VALIDATION_ERROR",
                f"'freshness' must be one of: {', '.join(sorted(valid_freshness))}", 400,
            )

        body: dict = {"query": query}
        if include_domains:
            body["includeDomains"] = [d.strip() for d in include_domains.split(",") if d.strip()]
        if exclude_domains:
            body["excludeDomains"] = [d.strip() for d in exclude_domains.split(",") if d.strip()]
        if freshness:
            body["freshness"] = freshness
        if query_fanout is not None:
            body["queryFanout"] = query_fanout
        if scrape_results is not None:
            body["markdownOptions"] = {"enabled": scrape_results}
        if timeout_ms is not None:
            body["timeoutMS"] = timeout_ms

        try:
            raw = make_post_request("/web/search", body)
            tlog.success()
            return WebSearchResult(success=True, statusCode=200, data=WebSearchData(**raw))
        except Exception as exc:
            return _handle_request_exc(WebSearchResult, tlog, exc)
