import json
import logging
from typing import Dict, Any, List
import requests
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class SearchEngine(ABC):
    """Abstract base class for search engines"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__
    
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Perform search with the engine"""
        pass
    
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Get engine configuration"""
        pass


class SerperEngine(SearchEngine):
    """Serper search engine implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = "https://google.serper.dev/search"
        
        if not self.api_key:
            raise ValueError("Serper API key is required")
    
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search using Serper API"""
        try:
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "q": query,
                "num": max_results,
                "type": "search"
            }
            
            # Add search parameters for better results
            data.update({
                "gl": "us",  # Geographic location
                "hl": "en",  # Language
                "autocorrect": True,
                "page": 1
            })
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            results = response.json()
            formatted_results = []
            
            # Process organic results
            for result in results.get("organic", [])[:max_results]:
                formatted_result = {
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "source": "serper",
                    "position": result.get("position", 0),
                    "date": result.get("date", ""),
                    "sitelinks": result.get("sitelinks", [])
                }
                
                # Add additional metadata if available
                if result.get("imageUrl"):
                    formatted_result["image_url"] = result["imageUrl"]
                
                formatted_results.append(formatted_result)
            
            # Process knowledge graph if available
            knowledge_graph = results.get("knowledgeGraph", {})
            if knowledge_graph:
                formatted_results.append({
                    "title": knowledge_graph.get("title", ""),
                    "url": knowledge_graph.get("descriptionLink", ""),
                    "snippet": knowledge_graph.get("description", ""),
                    "source": "serper_knowledge_graph",
                    "position": 0,
                    "type": "knowledge_graph",
                    "attributes": knowledge_graph.get("attributes", {})
                })
            
            return {
                "success": True,
                "engine": "serper",
                "query": query,
                "results": formatted_results,
                "total_results": len(formatted_results),
                "search_parameters": data
            }
            
        except requests.RequestException as e:
            logger.error(f"Serper API request failed: {e}")
            return {
                "success": False,
                "engine": "serper",
                "error": f"API request failed: {str(e)}",
                "query": query
            }
        except Exception as e:
            logger.error(f"Serper search error: {e}")
            return {
                "success": False,
                "engine": "serper",
                "error": f"Search failed: {str(e)}",
                "query": query
            }
    
    def get_config(self) -> Dict[str, Any]:
        """Get Serper engine configuration"""
        return {
            "engine": "serper",
            "api_key_configured": bool(self.api_key),
            "base_url": self.base_url
        }


class MetasoEngine(SearchEngine):
    """Metaso search engine implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = "https://api.metaso.com/v1/search"
        
        if not self.api_key:
            raise ValueError("Metaso API key is required")
    
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search using Metaso API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "query": query,
                "limit": max_results,
                "offset": 0,
                "language": "en",
                "region": "us"
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            results = response.json()
            formatted_results = []
            
            # Process results
            for result in results.get("results", [])[:max_results]:
                formatted_result = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("description", ""),
                    "source": "metaso",
                    "position": result.get("rank", 0),
                    "score": result.get("score", 0),
                    "published_date": result.get("publishedDate", ""),
                    "author": result.get("author", "")
                }
                
                # Add additional metadata
                if result.get("thumbnail"):
                    formatted_result["thumbnail"] = result["thumbnail"]
                
                if result.get("categories"):
                    formatted_result["categories"] = result["categories"]
                
                formatted_results.append(formatted_result)
            
            return {
                "success": True,
                "engine": "metaso",
                "query": query,
                "results": formatted_results,
                "total_results": len(formatted_results),
                "search_parameters": data
            }
            
        except requests.RequestException as e:
            logger.error(f"Metaso API request failed: {e}")
            return {
                "success": False,
                "engine": "metaso",
                "error": f"API request failed: {str(e)}",
                "query": query
            }
        except Exception as e:
            logger.error(f"Metaso search error: {e}")
            return {
                "success": False,
                "engine": "metaso",
                "error": f"Search failed: {str(e)}",
                "query": query
            }
    
    def get_config(self) -> Dict[str, Any]:
        """Get Metaso engine configuration"""
        return {
            "engine": "metaso",
            "api_key_configured": bool(self.api_key),
            "base_url": self.base_url
        }


class SogouEngine(SearchEngine):
    """Sogou search engine implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = "https://api.sogou.com/v1/search"
        
        if not self.api_key:
            raise ValueError("Sogou API key is required")
    
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search using Sogou API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "query": query,
                "count": max_results,
                "start": 0,
                "language": "zh-cn"  # Chinese language for Sogou
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            results = response.json()
            formatted_results = []
            
            # Process results
            for result in results.get("items", [])[:max_results]:
                formatted_result = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("abstract", ""),
                    "source": "sogou",
                    "position": result.get("rank", 0),
                    "display_url": result.get("displayUrl", ""),
                    "file_format": result.get("fileFormat", ""),
                    "size": result.get("size", "")
                }
                
                # Add additional metadata
                if result.get("cacheUrl"):
                    formatted_result["cache_url"] = result["cacheUrl"]
                
                if result.get("relatedSearches"):
                    formatted_result["related_searches"] = result["relatedSearches"]
                
                formatted_results.append(formatted_result)
            
            return {
                "success": True,
                "engine": "sogou",
                "query": query,
                "results": formatted_results,
                "total_results": len(formatted_results),
                "search_parameters": data
            }
            
        except requests.RequestException as e:
            logger.error(f"Sogou API request failed: {e}")
            return {
                "success": False,
                "engine": "sogou",
                "error": f"API request failed: {str(e)}",
                "query": query
            }
        except Exception as e:
            logger.error(f"Sogou search error: {e}")
            return {
                "success": False,
                "engine": "sogou",
                "error": f"Search failed: {str(e)}",
                "query": query
            }
    
    def get_config(self) -> Dict[str, Any]:
        """Get Sogou engine configuration"""
        return {
            "engine": "sogou",
            "api_key_configured": bool(self.api_key),
            "base_url": self.base_url
        }