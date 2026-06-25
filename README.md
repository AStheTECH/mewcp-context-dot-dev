# mewcp-context-dev

MewCP MCP server for the [Context.dev](https://context.dev) API — web scraping, brand intelligence, and structured data extraction as MCP tools.

## Tools

### Web Scraping

| Tool | Description |
|------|-------------|
| `scrape_html` | Scrape a URL and return raw HTML content |
| `scrape_markdown` | Scrape a URL and return clean LLM-ready Markdown |
| `scrape_screenshot` | Capture a visual screenshot of a webpage |
| `scrape_images` | Collect all images from a page with metadata |
| `crawl_sitemap` | Discover all pages via XML sitemaps |
| `web_search` | Search the web; optionally scrape results to Markdown |

### Brand Intelligence

| Tool | Description |
|------|-------------|
| `get_brand_by_domain` | Logos, colors, description, socials, address for a domain |
| `get_brand_by_email` | Brand data for the company behind an email address |
| `get_brand_by_name` | Brand data by company name (3–30 characters) |
| `identify_brand_from_transaction` | Identify a company from a bank transaction string |

### Web Extraction

| Tool | Description |
|------|-------------|
| `extract_structured_data` | Crawl a site and extract data matching a JSON Schema |
| `scrape_styleguide` | Extract design system: colors, typography, spacing, shadows |
| `scrape_fonts` | Extract font families, weights, usage stats, and CDN links |

## Authentication

This server uses a **static API key** credential. The MewCP Gateway injects the key as:

```
X-Mcp-Cred-Fields: {"api_key": "<your-context.dev-api-key>"}
```

When calling through the MewCP platform, pass:

```http
Authorization: Bearer <MEWCP_API_KEY>
X-Mewcp-Credential-Id: <credential-id>
```

The gateway resolves the stored credential and forwards it to this server automatically.

## Local Development

Run directly without the gateway by injecting the header yourself:

```bash
# Start the server
python server.py --transport streamable-http --port 8080

# Call a tool (replace with your real API key)
curl -X POST http://localhost:8080/mcp \
  -H 'Content-Type: application/json' \
  -H 'X-Mcp-Cred-Fields: {"api_key": "<your-context.dev-key>"}' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "scrape_markdown",
      "arguments": {"url": "https://example.com"}
    }
  }'
```

For local MCP client debugging:

```bash
python server.py --transport stdio
```

## Docker

```bash
docker build -t mewcp-context-dev .
docker run -p 8080:8080 mewcp-context-dev
```

Override transport or port at runtime:

```bash
docker run -e MCP_TRANSPORT=streamable-http -e PORT=9000 -p 9000:9000 mewcp-context-dev
```

## MCP Endpoint

```
https://<host>/mcp
```

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `UNAUTHORIZED` | Missing or invalid API key | Verify `X-Mcp-Cred-Fields` contains the correct `api_key` |
| `USAGE_EXCEEDED` | Credits exhausted | Check usage in the Context.dev dashboard |
| `REQUEST_TIMEOUT` | Slow target site or low `timeout_ms` | Increase `timeout_ms` or use `max_age_ms=0` to skip cache |
| `WEBSITE_ACCESS_ERROR` | Target site blocks scrapers | Try `wait_for_ms` for JS-heavy sites; some sites cannot be scraped |
| Missing credential error on startup | No `X-Mcp-Cred-Fields` header | Send the header with every request — the server is stateless |
