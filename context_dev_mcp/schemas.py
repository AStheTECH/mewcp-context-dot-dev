"""Typed result models for MewCP Context.dev MCP Server."""

from pydantic import BaseModel, ConfigDict
from typing import Any


# -----------------------------------------------------------------------------
# Base classes
# -----------------------------------------------------------------------------

class ToolError(BaseModel):
    code: str
    message: str
    details: Any = None


class ToolResult(BaseModel):
    success: bool
    statusCode: int
    retriable: bool = False
    retry_after_seconds: int | None = None
    error: ToolError | None = None


# -----------------------------------------------------------------------------
# Shared nested types
# -----------------------------------------------------------------------------

class KeyMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    credits_consumed: int
    credits_remaining: int


class PageMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str | None = None
    description: str | None = None
    language: str | None = None
    robots: str | None = None
    ogImage: str | None = None


# -----------------------------------------------------------------------------
# Web Scraping — scrape_html
# -----------------------------------------------------------------------------

class ScrapeHtmlData(BaseModel):
    model_config = ConfigDict(extra="allow")

    success: bool | None = None
    html: str | None = None
    url: str | None = None
    type: str | None = None
    metadata: PageMetadata | None = None
    key_metadata: KeyMetadata | None = None


class ScrapeHtmlResult(ToolResult):
    data: ScrapeHtmlData | None = None


# -----------------------------------------------------------------------------
# Web Scraping — scrape_markdown
# -----------------------------------------------------------------------------

class ScrapeMarkdownData(BaseModel):
    model_config = ConfigDict(extra="allow")

    success: bool | None = None
    markdown: str | None = None
    url: str | None = None
    metadata: PageMetadata | None = None
    key_metadata: KeyMetadata | None = None


class ScrapeMarkdownResult(ToolResult):
    data: ScrapeMarkdownData | None = None


# -----------------------------------------------------------------------------
# Web Scraping — scrape_screenshot
# -----------------------------------------------------------------------------

class ScrapeScreenshotData(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str | None = None
    domain: str | None = None
    screenshot: str | None = None
    screenshotType: str | None = None
    width: int | None = None
    height: int | None = None
    code: int | None = None
    key_metadata: KeyMetadata | None = None


class ScrapeScreenshotResult(ToolResult):
    data: ScrapeScreenshotData | None = None


# -----------------------------------------------------------------------------
# Web Scraping — scrape_images
# -----------------------------------------------------------------------------

class ImageItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    src: str | None = None
    element: str | None = None
    type: str | None = None
    alt: str | None = None


class ScrapeImagesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    success: bool | None = None
    images: list[ImageItem] | None = None
    url: str | None = None
    key_metadata: KeyMetadata | None = None


class ScrapeImagesResult(ToolResult):
    data: ScrapeImagesData | None = None


# -----------------------------------------------------------------------------
# Web Scraping — crawl_sitemap
# -----------------------------------------------------------------------------

class SitemapMeta(BaseModel):
    model_config = ConfigDict(extra="allow")

    sitemapsDiscovered: int | None = None
    sitemapsFetched: int | None = None
    sitemapsSkipped: int | None = None
    errors: int | None = None


class CrawlSitemapData(BaseModel):
    model_config = ConfigDict(extra="allow")

    success: bool | None = None
    domain: str | None = None
    urls: list | None = None
    meta: SitemapMeta | None = None
    key_metadata: KeyMetadata | None = None


class CrawlSitemapResult(ToolResult):
    data: CrawlSitemapData | None = None


# -----------------------------------------------------------------------------
# Web Scraping — web_search
# -----------------------------------------------------------------------------

class SearchResultItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str | None = None
    title: str | None = None
    description: str | None = None
    relevance: str | None = None
    markdown: dict | None = None


class WebSearchData(BaseModel):
    model_config = ConfigDict(extra="allow")

    results: list[SearchResultItem] | None = None
    query: str | None = None
    key_metadata: KeyMetadata | None = None


class WebSearchResult(ToolResult):
    data: WebSearchData | None = None


# -----------------------------------------------------------------------------
# Brand Intelligence — get_brand_by_domain, get_brand_by_email,
# get_brand_by_name, identify_brand_from_transaction (shared shape)
# -----------------------------------------------------------------------------

class BrandData(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str | None = None
    brand: dict | None = None
    code: int | None = None
    key_metadata: KeyMetadata | None = None


class BrandResult(ToolResult):
    data: BrandData | None = None


# -----------------------------------------------------------------------------
# Web Extraction — extract_structured_data
# -----------------------------------------------------------------------------

class ExtractData(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str | None = None
    url: str | None = None
    urls_analyzed: list | None = None
    data: dict | None = None
    metadata: dict | None = None
    key_metadata: KeyMetadata | None = None


class ExtractResult(ToolResult):
    data: ExtractData | None = None


# -----------------------------------------------------------------------------
# Web Extraction — scrape_styleguide
# -----------------------------------------------------------------------------

class StyleguideData(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str | None = None
    domain: str | None = None
    styleguide: dict | None = None
    code: int | None = None
    key_metadata: KeyMetadata | None = None


class StyleguideResult(ToolResult):
    data: StyleguideData | None = None


# -----------------------------------------------------------------------------
# Web Extraction — scrape_fonts
# -----------------------------------------------------------------------------

class FontsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str | None = None
    domain: str | None = None
    fonts: list | None = None
    fontLinks: dict | None = None
    code: int | None = None
    key_metadata: KeyMetadata | None = None


class FontsResult(ToolResult):
    data: FontsData | None = None
