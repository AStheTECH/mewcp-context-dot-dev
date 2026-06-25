import json
from typing import Optional

from fastmcp import FastMCP
from pydantic import Field

from context_dev_mcp.service import make_get_request, make_post_request


def register_tools(mcp: FastMCP) -> None:

    # -------------------------------------------------------------------------
    # Web Scraping
    # -------------------------------------------------------------------------

    @mcp.tool(
        name="scrape_html",
        description=(
            "Scrape a URL and return its raw HTML content. Supports web pages, PDFs, "
            "XML, JSON, Markdown, CSV, and SVG files."
        ),
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
    ) -> dict:
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
        return make_get_request("/web/scrape/html", params)

    @mcp.tool(
        name="scrape_markdown",
        description=(
            "Scrape a URL and return its content converted to clean, LLM-ready Markdown. "
            "Strips boilerplate and preserves headings, links, and structure."
        ),
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
    ) -> dict:
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
        return make_get_request("/web/scrape/markdown", params)

    @mcp.tool(
        name="scrape_screenshot",
        description=(
            "Capture a visual screenshot of a website. Provide either 'domain' for the "
            "homepage or 'direct_url' for a specific page. Returns a URL to the screenshot image."
        ),
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
    ) -> dict:
        if not domain and not direct_url:
            return {"error": True, "error_code": "INPUT_VALIDATION_ERROR", "message": "Provide either 'domain' or 'direct_url'"}
        valid_pages = {"login", "signup", "blog", "careers", "pricing", "terms", "privacy", "contact"}
        if page and page not in valid_pages:
            return {"error": True, "error_code": "INPUT_VALIDATION_ERROR", "message": f"'page' must be one of: {', '.join(sorted(valid_pages))}"}
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
        return make_get_request("/web/screenshot", params)

    @mcp.tool(
        name="scrape_images",
        description=(
            "Collect all images from a URL: img tags, SVGs, CSS backgrounds, video posters, "
            "and meta images. Returns each image's src, element type, and optional metadata."
        ),
    )
    def scrape_images(
        url: str = Field(..., description="Full page URL to inspect, including http:// or https://"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 86400000)"),
        wait_for_ms: Optional[int] = Field(None, ge=0, le=30000, description="Milliseconds to wait after page load for JavaScript rendering (0–30000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> dict:
        params: dict = {"url": url}
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if wait_for_ms is not None:
            params["waitForMs"] = wait_for_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        return make_get_request("/web/scrape/images", params)

    @mcp.tool(
        name="crawl_sitemap",
        description=(
            "Discover all pages on a website by crawling its XML sitemaps. "
            "Returns a list of URLs up to maxLinks (default 10,000)."
        ),
    )
    def crawl_sitemap(
        domain: str = Field(..., description="Domain to build a sitemap for (e.g. 'example.com')"),
        max_links: Optional[int] = Field(None, ge=1, le=100000, description="Maximum number of URLs to return (1–100000, default: 10000)"),
        url_regex: Optional[str] = Field(None, max_length=256, description="RE2-compatible regex to filter URLs (e.g. '/blog/'). Max 256 characters."),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> dict:
        params: dict = {"domain": domain}
        if max_links is not None:
            params["maxLinks"] = max_links
        if url_regex:
            params["urlRegex"] = url_regex
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        return make_get_request("/web/scrape/sitemap", params)

    @mcp.tool(
        name="web_search",
        description=(
            "Search the web with a natural-language query. Optionally scrapes each result "
            "page to Markdown for deeper content. Returns ranked results with url, title, "
            "description, and relevance."
        ),
    )
    def web_search(
        query: str = Field(..., min_length=1, max_length=500, description="Natural-language search query (1–500 characters)"),
        include_domains: Optional[str] = Field(None, description="Comma-separated domains to restrict results to (e.g. 'github.com,stackoverflow.com')"),
        exclude_domains: Optional[str] = Field(None, description="Comma-separated domains to exclude from results"),
        freshness: Optional[str] = Field(None, description="Limit results by age. One of: last_24_hours, last_week, last_month, last_year"),
        query_fanout: Optional[bool] = Field(None, description="Expand the query into parallel variants for broader coverage"),
        scrape_results: Optional[bool] = Field(None, description="Scrape each result page to Markdown and include it in the response"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> dict:
        valid_freshness = {"last_24_hours", "last_week", "last_month", "last_year"}
        if freshness and freshness not in valid_freshness:
            return {"error": True, "error_code": "INPUT_VALIDATION_ERROR", "message": f"'freshness' must be one of: {', '.join(sorted(valid_freshness))}"}
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
        return make_post_request("/web/search", body)

    # -------------------------------------------------------------------------
    # Brand Intelligence
    # -------------------------------------------------------------------------

    @mcp.tool(
        name="get_brand_by_domain",
        description=(
            "Retrieve rich brand data for a company domain: logos, colors, backdrops, "
            "description, social links, address, stock ticker, and industry classification."
        ),
    )
    def get_brand_by_domain(
        domain: str = Field(..., description="Domain to look up (e.g. 'stripe.com', 'apple.com')"),
        force_language: Optional[str] = Field(None, description="ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')"),
        max_speed: Optional[bool] = Field(None, description="Optimize for speed by skipping comprehensive data enrichment"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 7776000000 = ~3 months)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> dict:
        params: dict = {"domain": domain}
        if force_language:
            params["force_language"] = force_language
        if max_speed is not None:
            params["maxSpeed"] = max_speed
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        return make_get_request("/brand/retrieve", params)

    @mcp.tool(
        name="get_brand_by_email",
        description=(
            "Retrieve brand data for the company associated with an email address. "
            "Returns an error for free (Gmail, Outlook) or disposable email addresses."
        ),
    )
    def get_brand_by_email(
        email: str = Field(..., description="Email address to look up (e.g. 'contact@stripe.com')"),
        force_language: Optional[str] = Field(None, description="ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')"),
        max_speed: Optional[bool] = Field(None, description="Optimize for speed by skipping comprehensive data enrichment"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 86400000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> dict:
        params: dict = {"email": email}
        if force_language:
            params["force_language"] = force_language
        if max_speed is not None:
            params["maxSpeed"] = max_speed
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        return make_get_request("/brand/retrieve-by-email", params)

    @mcp.tool(
        name="get_brand_by_name",
        description=(
            "Retrieve brand data for a company by its name. Useful when only the company name "
            "is known. Name must be 3–30 characters."
        ),
    )
    def get_brand_by_name(
        name: str = Field(..., min_length=3, max_length=30, description="Company name to look up (e.g. 'Stripe', 'Apple Inc')"),
        country_gl: Optional[str] = Field(None, description="ISO 3166-1 alpha-2 country code to improve matching (e.g. 'US', 'GB')"),
        force_language: Optional[str] = Field(None, description="ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')"),
        max_speed: Optional[bool] = Field(None, description="Optimize for speed by skipping comprehensive data enrichment"),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 86400000)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> dict:
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
        return make_get_request("/brand/retrieve-by-name", params)

    @mcp.tool(
        name="identify_brand_from_transaction",
        description=(
            "Identify a company from a bank transaction description or merchant string "
            "(e.g. 'AMZN*123456', 'UBER* EATS', 'SQ *COFFEE SHOP'). Returns full brand data."
        ),
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
    ) -> dict:
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
        return make_get_request("/brand/transaction_identifier", params)

    # -------------------------------------------------------------------------
    # Web Extraction
    # -------------------------------------------------------------------------

    @mcp.tool(
        name="extract_structured_data",
        description=(
            "Crawl a website and extract structured data conforming to a JSON Schema. "
            "Ideal for scraping product info, pricing tables, contact details, team pages, "
            "or any structured content. Up to 50 pages per call."
        ),
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
    ) -> dict:
        try:
            schema_dict = json.loads(schema_json)
        except json.JSONDecodeError as e:
            return {"error": True, "error_code": "INPUT_VALIDATION_ERROR", "message": f"Invalid JSON schema: {e}"}
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
        return make_post_request("/web/extract", body)

    @mcp.tool(
        name="scrape_styleguide",
        description=(
            "Extract a website's design system: brand colors, typography (font families, "
            "sizes, weights), element spacing, shadows, button styles, and font CDN links."
        ),
    )
    def scrape_styleguide(
        domain: Optional[str] = Field(None, description="Domain name to extract styleguide from (e.g. 'stripe.com'). Either domain or direct_url is required."),
        direct_url: Optional[str] = Field(None, description="Specific URL to extract styleguide from. Either domain or direct_url is required."),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 7776000000 = ~3 months)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> dict:
        if not domain and not direct_url:
            return {"error": True, "error_code": "INPUT_VALIDATION_ERROR", "message": "Provide either 'domain' or 'direct_url'"}
        params: dict = {}
        if domain:
            params["domain"] = domain
        if direct_url:
            params["directUrl"] = direct_url
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        return make_get_request("/web/styleguide", params)

    @mcp.tool(
        name="scrape_fonts",
        description=(
            "Extract all font families used on a website along with usage statistics, "
            "CSS selectors, fallback fonts, and CDN asset links (Google Fonts or custom)."
        ),
    )
    def scrape_fonts(
        domain: Optional[str] = Field(None, description="Domain name to extract fonts from (e.g. 'stripe.com'). Either domain or direct_url is required."),
        direct_url: Optional[str] = Field(None, description="Specific URL to extract fonts from. Either domain or direct_url is required."),
        max_age_ms: Optional[int] = Field(None, description="Maximum cache age in milliseconds (default: 7776000000 = ~3 months)"),
        timeout_ms: Optional[int] = Field(None, ge=1000, le=300000, description="Request timeout in milliseconds (1000–300000)"),
    ) -> dict:
        if not domain and not direct_url:
            return {"error": True, "error_code": "INPUT_VALIDATION_ERROR", "message": "Provide either 'domain' or 'direct_url'"}
        params: dict = {}
        if domain:
            params["domain"] = domain
        if direct_url:
            params["directUrl"] = direct_url
        if max_age_ms is not None:
            params["maxAgeMs"] = max_age_ms
        if timeout_ms is not None:
            params["timeoutMS"] = timeout_ms
        return make_get_request("/web/fonts", params)
