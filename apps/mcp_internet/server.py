#!/usr/bin/env python3
"""
MCP Server for Internet Search with Serper, VoyageAI, and Trafilatura
"""

import asyncio
import base64
import json
import os
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import httpx
import trafilatura
import voyageai
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Image

# Load environment variables
load_dotenv()

# Initialize clients
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

if not SERPER_API_KEY or not VOYAGE_API_KEY:
    raise ValueError("Missing required API keys in .env file")

# Initialize VoyageAI client
voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)

# HTTP client configuration
HTTP_TIMEOUT = 10.0
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Domains to exclude
EXCLUDED_DOMAINS = {
    "youtube.com", "www.youtube.com", "youtu.be",
    "facebook.com", "www.facebook.com", "fb.com",
    "instagram.com", "www.instagram.com"
}

def is_excluded_url(url: str) -> bool:
    """Check if URL should be excluded based on domain"""
    try:
        domain = urlparse(url).netloc.lower()
        return any(excluded in domain for excluded in EXCLUDED_DOMAINS)
    except Exception:
        return True

async def search_serper(query: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """Search using Serper API"""
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "q": query,
        "num": num_results
    }
    
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if "organic" in data:
                for item in data["organic"]:
                    if not is_excluded_url(item.get("link", "")):
                        results.append({
                            "title": item.get("title", ""),
                            "url": item.get("link", ""),
                            "snippet": item.get("snippet", "")
                        })
            
            return results
        except Exception as e:
            raise Exception(f"Serper search failed: {str(e)}")

def rerank_with_voyage(query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    """Rerank search results using VoyageAI"""
    if not documents:
        return []
    
    try:
        # Prepare documents for reranking
        doc_texts = []
        for doc in documents:
            text = f"{doc['title']} {doc['snippet']}"
            doc_texts.append(text)
        
        # Use VoyageAI rerank
        reranked = voyage_client.rerank(
            query=query,
            documents=doc_texts,
            model="rerank-2.5",
            top_k=min(top_k, len(documents))
        )
        
        # Return reranked documents
        result = []
        for item in reranked.results:
            original_doc = documents[item.index]
            original_doc["relevance_score"] = item.relevance_score
            result.append(original_doc)
        
        return result
    except Exception as e:
        # If reranking fails, return original documents
        print(f"Reranking failed: {str(e)}, returning original results")
        return documents[:top_k]

async def crawl_and_extract(url: str) -> Optional[str]:
    """Crawl URL and extract clean text using Trafilatura"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers=headers) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            
            # Extract text using Trafilatura
            extracted = trafilatura.extract(
                response.text,
                include_comments=False,
                include_tables=True,
                include_formatting=False,
                favor_precision=True
            )
            
            return extracted
        except Exception as e:
            print(f"Failed to crawl {url}: {str(e)}")
            return None

async def internet_search(query: str, max_results: int = 5) -> str:
    """Complete internet search pipeline"""
    try:
        # Step 1: Search with Serper
        print(f"Searching for: {query}")
        search_results = await search_serper(query, num_results=10)
        
        if not search_results:
            return "No search results found."
        
        # Step 2: Rerank with VoyageAI
        print(f"Reranking {len(search_results)} results...")
        reranked_results = rerank_with_voyage(query, search_results, top_k=max_results)
        
        # Step 3: Crawl and extract content
        final_results = []
        for i, result in enumerate(reranked_results, 1):
            print(f"Crawling result {i}/{len(reranked_results)}: {result['url']}")
            content = await crawl_and_extract(result['url'])
            
            if content and len(content.strip()) > 100:  # Only include substantial content
                final_results.append({
                    "title": result['title'],
                    "url": result['url'],
                    "snippet": result['snippet'],
                    "content": content[:2000],  # Limit content length
                    "relevance_score": result.get('relevance_score', 0)
                })
        
        # Format results
        if not final_results:
            return "No content could be extracted from the search results."
        
        formatted_output = f"Search Results for: {query}\n\n"
        for i, result in enumerate(final_results, 1):
            formatted_output += f"## Result {i}: {result['title']}\n"
            formatted_output += f"**URL:** {result['url']}\n"
            formatted_output += f"**Relevance Score:** {result['relevance_score']:.3f}\n"
            formatted_output += f"**Snippet:** {result['snippet']}\n\n"
            formatted_output += f"**Content:**\n{result['content']}\n\n"
            formatted_output += "---\n\n"
        
        return formatted_output
        
    except Exception as e:
        return f"Search failed: {str(e)}"

# Initialize MCP Server
mcp = FastMCP("Internet Search")

@mcp.tool()
async def internet_search_tool(query: str, max_results: int = 5) -> str:
    """
    Search the internet for information using Serper API, rerank results with VoyageAI, and extract clean content.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return (default: 5, max: 10)
    
    Returns:
        Formatted search results with extracted content
    """
    if max_results > 10:
        max_results = 10
    elif max_results < 1:
        max_results = 1
        
    return await internet_search(query, max_results)

@mcp.tool()
async def take_screenshot(
    url: str,
    width: int = 1280,
    full_page: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Image:
    """
    Take a screenshot of a website.
    
    Args:
        url: The URL to capture
        width: Viewport width (default: 1280)
        full_page: Whether to take a screenshot of the entire page (default: False)
        username: Basic authentication username (optional)
        password: Basic authentication password (optional)
    
    Returns:
        A screenshot of the website.
    """
    async with async_playwright() as p:
        # Use system's chrome if available
        executable_path = "/usr/bin/google-chrome"
        if not os.path.exists(executable_path):
            executable_path = None
            
        browser = await p.chromium.launch(executable_path=executable_path, headless=True)
        
        # Setup context with viewport and auth if provided
        context_options = {
            "viewport": {"width": width, "height": 1080}
        }
        
        if username and password:
            context_options["http_credentials"] = {
                "username": username,
                "password": password
            }
            
        context = await browser.new_context(**context_options)
        page = await context.new_page()
        
        try:
            # Set timeout to 30s
            await page.goto(url, wait_until="networkidle", timeout=30000)
            # Give it an extra second to settle
            await asyncio.sleep(1)
            
            screenshot_bytes = await page.screenshot(full_page=full_page)
            await browser.close()
            
            return Image(data=screenshot_bytes, format="png")
        except Exception as e:
            await browser.close()
            raise Exception(f"Failed to take screenshot: {str(e)}")


if __name__ == "__main__":
    mcp.run()