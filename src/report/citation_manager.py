import re
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from urllib.parse import urlparse
import hashlib

logger = logging.getLogger(__name__)

class CitationManager:
    """Manage citations and references for reports"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.citation_styles = {
            "apa": self._format_apa_citation,
            "mla": self._format_mla_citation,
            "chicago": self._format_chicago_citation,
            "harvard": self._format_harvard_citation
        }
    
    async def process_citations(self, citations: List[Dict[str, Any]], style: str = "apa") -> List[Dict[str, Any]]:
        """Process and format citations"""
        try:
            processed_citations = []
            formatter = self.citation_styles.get(style, self._format_apa_citation)
            
            for i, citation in enumerate(citations):
                processed_citation = await formatter(citation, i + 1)
                processed_citations.append(processed_citation)
            
            return processed_citations
            
        except Exception as e:
            logger.error(f"Failed to process citations: {e}")
            return []
    
    async def _format_apa_citation(self, citation: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Format citation in APA style"""
        try:
            citation_text = ""
            
            if citation.get("type") == "website":
                citation_text = self._format_apa_website(citation)
            elif citation.get("type") == "article":
                citation_text = self._format_apa_article(citation)
            elif citation.get("type") == "book":
                citation_text = self._format_apa_book(citation)
            elif citation.get("type") == "report":
                citation_text = self._format_apa_report(citation)
            else:
                citation_text = self._format_apa_general(citation)
            
            return {
                "id": str(index),
                "text": citation_text,
                "url": citation.get("url", ""),
                "date": citation.get("access_date", datetime.now().strftime("%Y-%m-%d")),
                "type": citation.get("type", "general"),
                "doi": citation.get("doi", ""),
                "authors": citation.get("authors", []),
                "title": citation.get("title", ""),
                "source": citation.get("source", ""),
                "year": citation.get("year", "")
            }
            
        except Exception as e:
            logger.error(f"Failed to format APA citation: {e}")
            return {
                "id": str(index),
                "text": f"[Citation {index}] - Error formatting citation",
                "url": citation.get("url", ""),
                "date": citation.get("access_date", datetime.now().strftime("%Y-%m-%d")),
                "type": "error"
            }
    
    def _format_apa_website(self, citation: Dict[str, Any]) -> str:
        """Format website citation in APA style"""
        authors = self._format_authors_apa(citation.get("authors", []))
        year = citation.get("year", "n.d.")
        title = citation.get("title", "")
        url = citation.get("url", "")
        retrieval_date = citation.get("access_date", datetime.now().strftime("%Y-%m-%d"))
        
        citation_parts = []
        if authors:
            citation_parts.append(authors)
        
        citation_parts.append(f"({year}).")
        citation_parts.append(f"{title}.")
        
        if citation.get("site_name"):
            citation_parts.append(f"{citation['site_name']}.")
        
        citation_parts.append(f"Retrieved {retrieval_date}, from {url}")
        
        return " ".join(citation_parts)
    
    def _format_apa_article(self, citation: Dict[str, Any]) -> str:
        """Format article citation in APA style"""
        authors = self._format_authors_apa(citation.get("authors", []))
        year = citation.get("year", "")
        title = citation.get("title", "")
        journal = citation.get("journal", "")
        volume = citation.get("volume", "")
        issue = citation.get("issue", "")
        pages = citation.get("pages", "")
        doi = citation.get("doi", "")
        
        citation_parts = []
        if authors:
            citation_parts.append(authors)
        
        citation_parts.append(f"({year}).")
        citation_parts.append(f"{title}.")
        citation_parts.append(f"<em>{journal}</em>,")
        
        if volume and issue:
            citation_parts.append(f"{volume}({issue}),")
        elif volume:
            citation_parts.append(f"{volume},")
        
        if pages:
            citation_parts.append(f"{pages}.")
        
        if doi:
            citation_parts.append(f"https://doi.org/{doi}")
        
        return " ".join(citation_parts)
    
    def _format_apa_book(self, citation: Dict[str, Any]) -> str:
        """Format book citation in APA style"""
        authors = self._format_authors_apa(citation.get("authors", []))
        year = citation.get("year", "")
        title = citation.get("title", "")
        publisher = citation.get("publisher", "")
        doi = citation.get("doi", "")
        url = citation.get("url", "")
        
        citation_parts = []
        if authors:
            citation_parts.append(authors)
        
        citation_parts.append(f"({year}).")
        citation_parts.append(f"<em>{title}</em>.")
        
        if publisher:
            citation_parts.append(f"{publisher}.")
        
        if doi:
            citation_parts.append(f"https://doi.org/{doi}")
        elif url:
            citation_parts.append(url)
        
        return " ".join(citation_parts)
    
    def _format_apa_report(self, citation: Dict[str, Any]) -> str:
        """Format report citation in APA style"""
        authors = self._format_authors_apa(citation.get("authors", []))
        year = citation.get("year", "")
        title = citation.get("title", "")
        report_number = citation.get("report_number", "")
        institution = citation.get("institution", "")
        url = citation.get("url", "")
        
        citation_parts = []
        if authors:
            citation_parts.append(authors)
        
        citation_parts.append(f"({year}).")
        citation_parts.append(f"<em>{title}</em>")
        
        if report_number:
            citation_parts.append(f"(Report No. {report_number}).")
        
        if institution:
            citation_parts.append(f"{institution}.")
        
        if url:
            citation_parts.append(url)
        
        return " ".join(citation_parts)
    
    def _format_apa_general(self, citation: Dict[str, Any]) -> str:
        """Format general citation in APA style"""
        title = citation.get("title", "")
        url = citation.get("url", "")
        retrieval_date = citation.get("access_date", datetime.now().strftime("%Y-%m-%d"))
        
        if title and url:
            return f"{title}. Retrieved {retrieval_date}, from {url}"
        elif title:
            return title
        else:
            return f"Untitled source. Retrieved {retrieval_date}"
    
    def _format_authors_apa(self, authors: List[str]) -> str:
        """Format authors list in APA style"""
        if not authors:
            return ""
        
        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return f"{authors[0]} & {authors[1]}"
        elif len(authors) <= 7:
            return f"{', '.join(authors[:-1])}, & {authors[-1]}"
        else:
            return f"{', '.join(authors[:6])}, ... {authors[-1]}"
    
    async def _format_mla_citation(self, citation: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Format citation in MLA style"""
        # Simplified MLA formatting
        authors = ", ".join(citation.get("authors", []))
        title = citation.get("title", "")
        source = citation.get("source", "")
        year = citation.get("year", "")
        url = citation.get("url", "")
        
        citation_text = f'{authors}. "{title}." {source}, {year}, {url}.'
        
        return {
            "id": str(index),
            "text": citation_text,
            "url": url,
            "date": citation.get("access_date", datetime.now().strftime("%Y-%m-%d")),
            "type": citation.get("type", "general")
        }
    
    async def _format_chicago_citation(self, citation: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Format citation in Chicago style"""
        # Simplified Chicago formatting
        authors = ", ".join(citation.get("authors", []))
        title = citation.get("title", "")
        source = citation.get("source", "")
        year = citation.get("year", "")
        url = citation.get("url", "")
        
        citation_text = f'{authors}. {title}. {source}, {year}. {url}.'
        
        return {
            "id": str(index),
            "text": citation_text,
            "url": url,
            "date": citation.get("access_date", datetime.now().strftime("%Y-%m-%d")),
            "type": citation.get("type", "general")
        }
    
    async def _format_harvard_citation(self, citation: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Format citation in Harvard style"""
        # Simplified Harvard formatting
        authors = ", ".join(citation.get("authors", []))
        year = citation.get("year", "")
        title = citation.get("title", "")
        source = citation.get("source", "")
        url = citation.get("url", "")
        
        citation_text = f'{authors} ({year}) {title}. {source}. Available at: {url}.'
        
        return {
            "id": str(index),
            "text": citation_text,
            "url": url,
            "date": citation.get("access_date", datetime.now().strftime("%Y-%m-%d")),
            "type": citation.get("type", "general")
        }
    
    async def extract_citations_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract citations from text using pattern matching"""
        citations = []
        
        # Pattern for URLs
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)
        
        for url in urls:
            try:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                
                citation = {
                    "type": "website",
                    "url": url,
                    "title": f"Source from {domain}",
                    "source": domain,
                    "access_date": datetime.now().strftime("%Y-%m-%d")
                }
                
                citations.append(citation)
            except Exception as e:
                logger.warning(f"Failed to parse URL: {url}")
        
        # Pattern for DOIs
        doi_pattern = r'doi:\s*([^\s]+)|https://doi\.org/([^\s]+)'
        doi_matches = re.findall(doi_pattern, text)
        
        for match in doi_matches:
            doi = match[0] or match[1]
            if doi:
                citation = {
                    "type": "article",
                    "doi": doi,
                    "url": f"https://doi.org/{doi}",
                    "title": f"DOI: {doi}",
                    "access_date": datetime.now().strftime("%Y-%m-%d")
                }
                citations.append(citation)
        
        return citations
    
    async def validate_citation(self, citation: Dict[str, Any]) -> bool:
        """Validate citation data"""
        required_fields = ["title", "type"]
        
        for field in required_fields:
            if not citation.get(field):
                logger.warning(f"Citation missing required field: {field}")
                return False
        
        # Validate URL if present
        if citation.get("url"):
            try:
                parsed_url = urlparse(citation["url"])
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    logger.warning(f"Invalid URL: {citation['url']}")
                    return False
            except Exception:
                logger.warning(f"Invalid URL format: {citation['url']}")
                return False
        
        return True
    
    async def generate_citation_id(self, citation: Dict[str, Any]) -> str:
        """Generate unique ID for citation"""
        # Create hash based on key citation fields
        citation_str = f"{citation.get('title', '')}{citation.get('url', '')}{citation.get('year', '')}"
        hash_object = hashlib.md5(citation_str.encode())
        return hash_object.hexdigest()[:8]
    
    async def deduplicate_citations(self, citations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate citations"""
        seen = set()
        unique_citations = []
        
        for citation in citations:
            # Create unique key based on URL and title
            url = citation.get("url", "")
            title = citation.get("title", "")
            key = f"{url}|{title}"
            
            if key not in seen:
                seen.add(key)
                unique_citations.append(citation)
        
        return unique_citations
    
    async def sort_citations(self, citations: List[Dict[str, Any]], sort_by: str = "author") -> List[Dict[str, Any]]:
        """Sort citations by specified criteria"""
        if sort_by == "author":
            return sorted(citations, key=lambda x: x.get("authors", [""])[0].lower() if x.get("authors") else "")
        elif sort_by == "title":
            return sorted(citations, key=lambda x: x.get("title", "").lower())
        elif sort_by == "year":
            return sorted(citations, key=lambda x: x.get("year", ""), reverse=True)
        elif sort_by == "type":
            return sorted(citations, key=lambda x: x.get("type", ""))
        else:
            return citations
    
    async def get_citation_statistics(self, citations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about citations"""
        if not citations:
            return {"total": 0}
        
        type_counts = {}
        source_counts = {}
        year_counts = {}
        
        for citation in citations:
            # Count by type
            citation_type = citation.get("type", "unknown")
            type_counts[citation_type] = type_counts.get(citation_type, 0) + 1
            
            # Count by source
            source = citation.get("source", "unknown")
            source_counts[source] = source_counts.get(source, 0) + 1
            
            # Count by year
            year = citation.get("year", "unknown")
            year_counts[year] = year_counts.get(year, 0) + 1
        
        return {
            "total": len(citations),
            "by_type": type_counts,
            "by_source": source_counts,
            "by_year": year_counts
        }