from fastmcp import FastMCP

from .web_scraping_tools import register_web_scraping_tools
from .brand_intelligence_tools import register_brand_intelligence_tools
from .web_extraction_tools import register_web_extraction_tools


def register_tools(mcp: FastMCP) -> None:
    register_web_scraping_tools(mcp)
    register_brand_intelligence_tools(mcp)
    register_web_extraction_tools(mcp)
