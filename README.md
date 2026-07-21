**Scrape, extract, and understand the web — plus identify any company from a domain, email, name, or transaction string.**

A Model Context Protocol (MCP) server that exposes Context.dev's API for web scraping, structured data extraction, and brand intelligence.


## Overview

The mewcp-context-dev MCP Server provides:

- Web scraping in multiple formats — raw HTML, clean Markdown, screenshots, images, sitemaps, and web search
- Schema-driven structured data extraction, plus design-system extraction (styleguides and fonts)
- Brand intelligence lookups by domain, email, company name, or raw bank transaction string

Perfect for:

- Building AI agents that read, summarize, or monitor web content
- Enriching CRM, KYC, or fintech pipelines with company and brand data from a domain, email, or transaction string
- Extracting a competitor's design system (colors, typography, fonts) or structured product/pricing data at scale


## Tools

### Web Scraping

<details>
<summary><code>scrape_html</code> — Scrape a URL and return its raw HTML</summary>

Scrape a URL and return its raw HTML content. Supports web pages, PDFs, XML, JSON, Markdown, CSV, and SVG files.

**Inputs:**
```
- `url` (string, required) — Full URL to scrape, including http:// or https://
- `include_frames` (boolean, optional) — Render iframes inline in the returned HTML
- `use_main_content_only` (boolean, optional) — Extract only the main content area, stripping navigation, ads, and footers
- `include_selectors` (string, optional) — Comma-separated CSS selectors to keep (e.g. 'article,.main-content'). Max 50 selectors.
- `exclude_selectors` (string, optional) — Comma-separated CSS selectors to remove (e.g. 'nav,footer,.ads'). Max 50 selectors.
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds. 0 = always fetch fresh. Default: 86400000 (1 day).
- `wait_for_ms` (integer, optional) — Milliseconds to wait after page load for JavaScript rendering (0–30000)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  success: boolean | null;
  html: string | null;
  url: string | null;
  type: string | null;
  metadata: {
    title: string | null;
    description: string | null;
    language: string | null;
    robots: string | null;
    ogImage: string | null;
  } | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>scrape_markdown</code> — Scrape a URL and return clean, LLM-ready Markdown</summary>

Scrape a URL and return its content converted to clean, LLM-ready Markdown. Strips boilerplate and preserves headings, links, and structure.

**Inputs:**
```
- `url` (string, required) — Full URL to scrape, including http:// or https://
- `include_links` (boolean, optional) — Preserve hyperlinks in the Markdown output (default: true)
- `include_images` (boolean, optional) — Include image references in the Markdown output (default: false)
- `use_main_content_only` (boolean, optional) — Extract only the main content area, stripping navigation, ads, and footers
- `include_frames` (boolean, optional) — Render iframe contents into the Markdown
- `include_selectors` (string, optional) — Comma-separated CSS selectors to keep (e.g. 'article,.main-content'). Max 50 selectors.
- `exclude_selectors` (string, optional) — Comma-separated CSS selectors to remove (e.g. 'nav,footer,.ads'). Max 50 selectors.
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds. 0 = always fetch fresh. Default: 86400000 (1 day).
- `wait_for_ms` (integer, optional) — Milliseconds to wait after page load for JavaScript rendering (0–30000)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  success: boolean | null;
  markdown: string | null;
  url: string | null;
  metadata: {
    title: string | null;
    description: string | null;
    language: string | null;
    robots: string | null;
    ogImage: string | null;
  } | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>scrape_screenshot</code> — Capture a visual screenshot of a website</summary>

Capture a visual screenshot of a website. Provide either 'domain' for the homepage or 'direct_url' for a specific page. Returns a URL to the screenshot image.

**Inputs:**
```
- `domain` (string, optional) — Domain name to screenshot (e.g. 'example.com'). Either domain or direct_url is required.
- `direct_url` (string, optional) — Specific URL to screenshot directly (e.g. 'https://example.com/pricing'). Either domain or direct_url is required.
- `full_screenshot` (boolean, optional) — Capture the full scrollable page instead of just the viewport
- `handle_cookie_popup` (boolean, optional) — Automatically dismiss cookie consent popups before capturing
- `viewport_width` (integer, optional) — Viewport width in pixels (240–7680, default: 1920)
- `viewport_height` (integer, optional) — Viewport height in pixels (240–4320, default: 1080)
- `page` (string, optional) — Named page to capture. One of: login, signup, blog, careers, pricing, terms, privacy, contact
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds (default: 86400000)
- `wait_for_ms` (integer, optional) — Milliseconds to wait after page load (0–30000, default: 3000)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  status: string | null;
  domain: string | null;
  screenshot: string | null;
  screenshotType: string | null;
  width: number | null;
  height: number | null;
  code: number | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>scrape_images</code> — Collect all images referenced on a page</summary>

Collect all images from a URL: img tags, SVGs, CSS backgrounds, video posters, and meta images. Returns each image's src, element type, and optional metadata.

**Inputs:**
```
- `url` (string, required) — Full page URL to inspect, including http:// or https://
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds (default: 86400000)
- `wait_for_ms` (integer, optional) — Milliseconds to wait after page load for JavaScript rendering (0–30000)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  success: boolean | null;
  images: {
    src: string | null;
    element: string | null;
    type: string | null;
    alt: string | null;
  }[] | null;
  url: string | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>crawl_sitemap</code> — Discover all pages on a website via its XML sitemaps</summary>

Discover all pages on a website by crawling its XML sitemaps. Returns a list of URLs up to maxLinks (default 10,000).

**Inputs:**
```
- `domain` (string, required) — Domain to build a sitemap for (e.g. 'example.com')
- `max_links` (integer, optional) — Maximum number of URLs to return (1–100000, default: 10000)
- `url_regex` (string, optional) — RE2-compatible regex to filter URLs (e.g. '/blog/'). Max 256 characters.
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  success: boolean | null;
  domain: string | null;
  urls: any[] | null;
  meta: {
    sitemapsDiscovered: number | null;
    sitemapsFetched: number | null;
    sitemapsSkipped: number | null;
    errors: number | null;
  } | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>web_search</code> — Search the web with a natural-language query</summary>

Search the web with a natural-language query. Optionally scrapes each result page to Markdown for deeper content. Returns ranked results with url, title, description, and relevance.

**Inputs:**
```
- `query` (string, required) — Natural-language search query (1–500 characters)
- `include_domains` (string, optional) — Comma-separated domains to restrict results to (e.g. 'github.com,stackoverflow.com')
- `exclude_domains` (string, optional) — Comma-separated domains to exclude from results
- `freshness` (string, optional) — Limit results by age. One of: last_24_hours, last_week, last_month, last_year
- `query_fanout` (boolean, optional) — Expand the query into parallel variants for broader coverage
- `scrape_results` (boolean, optional) — Scrape each result page to Markdown and include it in the response
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  results: {
    url: string | null;
    title: string | null;
    description: string | null;
    relevance: string | null;
    markdown: object | null;
  }[] | null;
  query: string | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


### Brand Intelligence

<details>
<summary><code>get_brand_by_domain</code> — Retrieve rich brand data for a company domain</summary>

Retrieve rich brand data for a company domain: logos, colors, backdrops, description, social links, address, stock ticker, and industry classification.

**Inputs:**
```
- `domain` (string, required) — Domain to look up (e.g. 'stripe.com', 'apple.com')
- `force_language` (string, optional) — ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')
- `max_speed` (boolean, optional) — Optimize for speed by skipping comprehensive data enrichment
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds (default: 7776000000 = ~3 months)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  status: string | null;
  brand: object | null;
  code: number | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>get_brand_by_email</code> — Retrieve brand data for the company behind an email address</summary>

Retrieve brand data for the company associated with an email address. Returns an error for free (Gmail, Outlook) or disposable email addresses.

**Inputs:**
```
- `email` (string, required) — Email address to look up (e.g. 'contact@stripe.com')
- `force_language` (string, optional) — ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')
- `max_speed` (boolean, optional) — Optimize for speed by skipping comprehensive data enrichment
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds (default: 86400000)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  status: string | null;
  brand: object | null;
  code: number | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>get_brand_by_name</code> — Retrieve brand data for a company by name</summary>

Retrieve brand data for a company by its name. Useful when only the company name is known. Name must be 3–30 characters.

**Inputs:**
```
- `name` (string, required) — Company name to look up (e.g. 'Stripe', 'Apple Inc')
- `country_gl` (string, optional) — ISO 3166-1 alpha-2 country code to improve matching (e.g. 'US', 'GB')
- `force_language` (string, optional) — ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')
- `max_speed` (boolean, optional) — Optimize for speed by skipping comprehensive data enrichment
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds (default: 86400000)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  status: string | null;
  brand: object | null;
  code: number | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>identify_brand_from_transaction</code> — Identify a company from a bank transaction or merchant string</summary>

Identify a company from a bank transaction description or merchant string (e.g. 'AMZN*123456', 'UBER* EATS', 'SQ *COFFEE SHOP'). Returns full brand data.

**Inputs:**
```
- `transaction_info` (string, required) — Raw transaction or merchant string to identify (e.g. 'AMZN*123456 SEATTLE WA')
- `country_gl` (string, optional) — ISO 3166-1 alpha-2 country code for geographic context (e.g. 'US', 'GB')
- `city` (string, optional) — City name from the transaction to improve matching
- `mcc` (string, optional) — Merchant Category Code (MCC) to narrow the industry search
- `high_confidence_only` (boolean, optional) — Run additional verification to return only high-confidence matches (default: false)
- `force_language` (string, optional) — ISO 639-1 language code to force for brand text (e.g. 'en', 'fr')
- `max_speed` (boolean, optional) — Optimize for speed by skipping comprehensive data enrichment
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  status: string | null;
  brand: object | null;
  code: number | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


### Web Extraction

<details>
<summary><code>extract_structured_data</code> — Crawl a website and extract structured data via JSON Schema</summary>

Crawl a website and extract structured data conforming to a JSON Schema. Ideal for scraping product info, pricing tables, contact details, team pages, or any structured content. Up to 50 pages per call.

**Inputs:**
```
- `url` (string, required) — Starting URL to crawl, including http:// or https://
- `schema_json` (string, required) — JSON Schema (as a JSON string) defining the structure of data to extract. Example: '{"type":"object","properties":{"title":{"type":"string"},"price":{"type":"number"}}}'
- `instructions` (string, optional) — Natural-language extraction instructions to guide the model (max 2000 characters)
- `fact_check` (boolean, optional) — When true, values must be grounded in page content — reduces hallucination (default: false)
- `follow_subdomains` (boolean, optional) — Follow links on subdomains of the starting URL (default: false)
- `max_pages` (integer, optional) — Maximum number of pages to analyze (1–50, default: 5)
- `max_depth` (integer, optional) — Maximum link depth from the starting URL
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds (default: 604800000 = 7 days)
- `wait_for_ms` (integer, optional) — Milliseconds to wait after page load for JavaScript rendering (0–30000)
- `stop_after_ms` (integer, optional) — Crawl time budget in milliseconds (10000–110000, default: 80000)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  status: string | null;
  url: string | null;
  urls_analyzed: any[] | null;
  data: object | null;
  metadata: object | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>scrape_styleguide</code> — Extract a website's design system</summary>

Extract a website's design system: brand colors, typography (font families, sizes, weights), element spacing, shadows, button styles, and font CDN links.

**Inputs:**
```
- `domain` (string, optional) — Domain name to extract styleguide from (e.g. 'stripe.com'). Either domain or direct_url is required.
- `direct_url` (string, optional) — Specific URL to extract styleguide from. Either domain or direct_url is required.
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds (default: 7776000000 = ~3 months)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  status: string | null;
  domain: string | null;
  styleguide: object | null;
  code: number | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


<details>
<summary><code>scrape_fonts</code> — Extract all font families used on a website</summary>

Extract all font families used on a website along with usage statistics, CSS selectors, fallback fonts, and CDN asset links (Google Fonts or custom).

**Inputs:**
```
- `domain` (string, optional) — Domain name to extract fonts from (e.g. 'stripe.com'). Either domain or direct_url is required.
- `direct_url` (string, optional) — Specific URL to extract fonts from. Either domain or direct_url is required.
- `max_age_ms` (integer, optional) — Maximum cache age in milliseconds (default: 7776000000 = ~3 months)
- `timeout_ms` (integer, optional) — Request timeout in milliseconds (1000–300000)
```

**Output `data` schema:**

```typescript
{
  status: string | null;
  domain: string | null;
  fonts: any[] | null;
  fontLinks: object | null;
  code: number | null;
  key_metadata: {
    credits_consumed: number;
    credits_remaining: number;
  } | null;
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "VALIDATION_ERROR", "message": "...", "details": null },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `REQUEST_TIMEOUT`, `RATE_LIMIT`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Common Parameters</strong></summary>

- `domain` / `direct_url` — Site targeting used by `scrape_screenshot`, `scrape_styleguide`, and `scrape_fonts`. Exactly one of the two is required on each of those tools.
- `max_age_ms` — Maximum cache age in milliseconds for the underlying scrape. `0` forces a fresh fetch; otherwise cached results younger than this may be returned. Default varies per tool (1 day for scraping tools, ~3 months for brand/styleguide/fonts/screenshot, 7 days for extraction).
- `wait_for_ms` — Milliseconds to wait after page load before capturing content, to allow JavaScript-rendered content to settle (0–30000).
- `timeout_ms` — Overall request timeout in milliseconds, shared across all 13 tools (1000–300000).
- `key_metadata` — Present on every successful `data` payload; reports `credits_consumed` and `credits_remaining` for the API key used.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**CSS Selectors (`include_selectors` / `exclude_selectors`):**

```
Comma-separated list of CSS selectors, max 50 entries.
Example: article,.main-content
Example: nav,footer,.ads
```

**Freshness (`web_search`):**

```
One of: last_24_hours, last_week, last_month, last_year
```

**Named Pages (`scrape_screenshot`):**

```
One of: login, signup, blog, careers, pricing, terms, privacy, contact
```

**JSON Schema (`extract_structured_data`):**

```
A JSON Schema object, passed as a JSON string.
Example: {"type":"object","properties":{"title":{"type":"string"},"price":{"type":"number"}}}
```

</details>


## Getting Your Context.dev API Key

<details>
<summary><strong>Steps</strong></summary>

1. Go to the [Context.dev Developer Dashboard](https://context.dev)
2. Sign in and navigate to the API keys section of your account
3. Click **Create API Key** (or equivalent)
4. Copy the generated key — you will only see it once

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Context.dev credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Add your Context.dev API key (static)
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Context.dev API Error</strong></summary>

- **Cause:** Upstream Context.dev API returned an error
- **Solution:**
  1. Check Context.dev service status
  2. Verify your credential has the required permissions
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Context.dev API Documentation](https://context.dev)** — Official API reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
