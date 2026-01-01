"""
Web research module: search and scrape functionality.
"""

import logging
import httpx
from typing import Optional, List, Dict
from urllib.parse import urlparse
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

# Try to import trafilatura for better web scraping
try:
    import trafilatura
    HAS_TRAFILATURA = True
except ImportError:
    HAS_TRAFILATURA = False
    logger.warning("trafilatura not available, using basic scraping")

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


class WebResearcher:
    """Handles web research: searching and scraping."""

    def __init__(self):
        self.client = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        )

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Perform web search using DuckDuckGo.

        Returns list of {title, body, href}
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            logger.info(f"Search '{query}' returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def scrape_website(self, url: str) -> Dict:
        """
        Scrape a website and extract structured content.

        Returns {
            url: str,
            title: str,
            content: str,
            meta_description: str,
            links: list,
            success: bool,
            error: str or None
        }
        """
        result = {
            "url": url,
            "title": "",
            "content": "",
            "meta_description": "",
            "links": [],
            "success": False,
            "error": None
        }

        try:
            response = self.client.get(url)
            response.raise_for_status()
            html = response.text

            # Try trafilatura first (best for article extraction)
            if HAS_TRAFILATURA:
                content = trafilatura.extract(
                    html,
                    include_comments=False,
                    include_tables=True,
                    favor_precision=True
                )
                if content:
                    result["content"] = content

            # Fallback to BeautifulSoup
            if not result["content"] and HAS_BS4:
                soup = BeautifulSoup(html, 'html.parser')

                # Get title
                title_tag = soup.find('title')
                if title_tag:
                    result["title"] = title_tag.get_text().strip()

                # Get meta description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    result["meta_description"] = meta_desc.get('content', '')

                # Get main content
                # Remove script, style, nav, footer, header
                for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                    tag.decompose()

                # Try to find main content area
                main = soup.find('main') or soup.find('article') or soup.find('body')
                if main:
                    result["content"] = main.get_text(separator='\n', strip=True)

                # Get important links
                for link in soup.find_all('a', href=True)[:20]:
                    href = link.get('href', '')
                    text = link.get_text().strip()
                    if text and href and not href.startswith('#'):
                        result["links"].append({"text": text, "href": href})

            result["success"] = bool(result["content"])

        except Exception as e:
            logger.error(f"Scrape failed for {url}: {e}")
            result["error"] = str(e)

        return result

    def research_business(self, business_info: Dict) -> Dict:
        """
        Perform comprehensive research on a business.

        Args:
            business_info: Dict with keys like name, website, industry, location, etc.

        Returns:
            Compiled research results
        """
        research = {
            "website_content": None,
            "competitor_info": [],
            "industry_insights": [],
            "trust_signals": [],
            "sources": []
        }

        # 1. Scrape the business website if provided
        website = business_info.get("website")
        if website:
            logger.info(f"Scraping business website: {website}")
            research["website_content"] = self.scrape_website(website)
            if research["website_content"]["success"]:
                research["sources"].append({
                    "type": "primary",
                    "url": website,
                    "description": "Official business website"
                })

        # 2. Search for competitors
        name = business_info.get("name", "")
        industry = business_info.get("industry", "")
        location = business_info.get("location", "")

        if industry:
            query = f"{industry} competitors {location}".strip()
            logger.info(f"Searching competitors: {query}")
            results = self.search(query, max_results=5)
            for r in results:
                research["competitor_info"].append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", "")
                })
                research["sources"].append({
                    "type": "competitor",
                    "url": r.get("href", ""),
                    "description": r.get("title", "")
                })

        # 3. Search for industry best practices
        if industry:
            query = f"{industry} landing page best practices conversion"
            logger.info(f"Searching best practices: {query}")
            results = self.search(query, max_results=5)
            for r in results:
                research["industry_insights"].append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", "")
                })

        # 4. Search for trust signals in this industry
        if industry:
            query = f"{industry} customer concerns objections trust"
            logger.info(f"Searching trust signals: {query}")
            results = self.search(query, max_results=5)
            for r in results:
                research["trust_signals"].append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", "")
                })

        # 5. If business name provided, search for reviews/reputation
        if name:
            query = f'"{name}" reviews reputation'
            logger.info(f"Searching reputation: {query}")
            results = self.search(query, max_results=3)
            for r in results:
                research["sources"].append({
                    "type": "reputation",
                    "url": r.get("href", ""),
                    "description": r.get("title", "")
                })

        return research

    def format_research_for_prompt(self, research: Dict) -> str:
        """Format research results into a string for AI prompt."""
        sections = []

        # Website content
        if research.get("website_content") and research["website_content"].get("success"):
            wc = research["website_content"]
            content = wc.get("content", "")[:5000]  # Limit size
            sections.append(f"""## BUSINESS WEBSITE CONTENT
URL: {wc.get('url', '')}
Title: {wc.get('title', '')}
Meta Description: {wc.get('meta_description', '')}

Content:
{content}
""")

        # Competitor info
        if research.get("competitor_info"):
            comp_text = "\n".join([
                f"- **{c['title']}**: {c['snippet']}"
                for c in research["competitor_info"][:5]
            ])
            sections.append(f"""## COMPETITOR LANDSCAPE
{comp_text}
""")

        # Industry insights
        if research.get("industry_insights"):
            insights_text = "\n".join([
                f"- **{i['title']}**: {i['snippet']}"
                for i in research["industry_insights"][:5]
            ])
            sections.append(f"""## INDUSTRY INSIGHTS
{insights_text}
""")

        # Trust signals
        if research.get("trust_signals"):
            trust_text = "\n".join([
                f"- **{t['title']}**: {t['snippet']}"
                for t in research["trust_signals"][:5]
            ])
            sections.append(f"""## CUSTOMER CONCERNS & TRUST FACTORS
{trust_text}
""")

        # Sources
        if research.get("sources"):
            sources_text = "\n".join([
                f"- [{s['type'].upper()}] {s['description']}: {s['url']}"
                for s in research["sources"][:10]
            ])
            sections.append(f"""## SOURCES CONSULTED
{sources_text}
""")

        return "\n\n".join(sections)

    def close(self):
        """Close the HTTP client."""
        self.client.close()
