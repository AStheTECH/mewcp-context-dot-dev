from typing import TypedDict, Optional


class KeyMetadata(TypedDict):
    credits_consumed: int
    credits_remaining: int


class PageMetadata(TypedDict, total=False):
    title: str
    description: str
    language: str
    robots: str
    ogImage: str


class ScrapeHtmlResponse(TypedDict, total=False):
    success: bool
    html: str
    url: str
    type: str
    metadata: PageMetadata
    key_metadata: KeyMetadata


class ScrapeMarkdownResponse(TypedDict, total=False):
    success: bool
    markdown: str
    url: str
    metadata: PageMetadata
    key_metadata: KeyMetadata


class ScreenshotResponse(TypedDict, total=False):
    status: str
    domain: str
    screenshot: str
    screenshotType: str
    width: int
    height: int
    code: int
    key_metadata: KeyMetadata


class ImageItem(TypedDict, total=False):
    src: str
    element: str
    type: str
    alt: Optional[str]


class ScrapeImagesResponse(TypedDict, total=False):
    success: bool
    images: list
    url: str
    key_metadata: KeyMetadata


class SitemapMeta(TypedDict, total=False):
    sitemapsDiscovered: int
    sitemapsFetched: int
    sitemapsSkipped: int
    errors: int


class CrawlSitemapResponse(TypedDict, total=False):
    success: bool
    domain: str
    urls: list
    meta: SitemapMeta
    key_metadata: KeyMetadata


class SearchResult(TypedDict, total=False):
    url: str
    title: str
    description: str
    relevance: str
    markdown: dict


class WebSearchResponse(TypedDict, total=False):
    results: list
    query: str
    key_metadata: KeyMetadata


class BrandResponse(TypedDict, total=False):
    status: str
    brand: dict
    code: int
    key_metadata: KeyMetadata


class ExtractResponse(TypedDict, total=False):
    status: str
    url: str
    urls_analyzed: list
    data: dict
    metadata: dict
    key_metadata: KeyMetadata


class StyleguideResponse(TypedDict, total=False):
    status: str
    domain: str
    styleguide: dict
    code: int
    key_metadata: KeyMetadata


class FontsResponse(TypedDict, total=False):
    status: str
    domain: str
    fonts: list
    fontLinks: dict
    code: int
    key_metadata: KeyMetadata


class ErrorResponse(TypedDict):
    error: bool
    error_code: str
    message: str
