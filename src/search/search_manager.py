import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .engines import SerperEngine, MetasoEngine, SogouEngine

logger = logging.getLogger(__name__)

class SearchManager:
    """Manages multiple search engines and coordinates search operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.engines = {}
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize search engines based on configuration"""
        # Initialize Serper engine
        if self.config.get("serper_api_key"):
            self.engines["serper"] = SerperEngine({
                "api_key": self.config["serper_api_key"]
            })
            logger.info("Serper search engine initialized")
        
        # Initialize Metaso engine
        if self.config.get("metaso_api_key"):
            self.engines["metaso"] = MetasoEngine({
                "api_key": self.config["metaso_api_key"]
            })
            logger.info("Metaso search engine initialized")
        
        # Initialize Sogou engine
        if self.config.get("sogou_api_key"):
            self.engines["sogou"] = SogouEngine({
                "api_key": self.config["sogou_api_key"]
            })
            logger.info("Sogou search engine initialized")
    
    async def search(self, query: str, engines: List[str] = None, max_results: int = 10) -> Dict[str, Any]:
        """Perform search across multiple engines"""
        if not self.engines:
            return {
                "success": False,
                "error": "No search engines configured",
                "results": []
            }
        
        if not engines:
            engines = list(self.engines.keys())
        
        # Validate engines
        valid_engines = [engine for engine in engines if engine in self.engines]
        if not valid_engines:
            return {
                "success": False,
                "error": "No valid search engines available",
                "results": []
            }
        
        # Perform concurrent searches
        search_tasks = []
        for engine_name in valid_engines:
            engine = self.engines[engine_name]
            search_tasks.append(self._search_with_engine(engine, engine_name, query, max_results))
        
        # Wait for all searches to complete
        search_results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Aggregate results
        all_results = []
        successful_engines = []
        
        for i, result in enumerate(search_results):
            engine_name = valid_engines[i]
            if isinstance(result, Exception):
                logger.error(f"Search with {engine_name} failed: {result}")
            elif result.get("success"):
                all_results.extend(result.get("results", []))
                successful_engines.append(engine_name)
        
        # Remove duplicates and rank results
        unique_results = self._deduplicate_results(all_results)
        ranked_results = await self._rank_results(query, unique_results)
        
        return {
            "success": True,
            "query": query,
            "engines_used": successful_engines,
            "results": ranked_results[:max_results],
            "total_results": len(ranked_results),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _search_with_engine(self, engine, engine_name: str, query: str, max_results: int) -> Dict[str, Any]:
        """Search with a specific engine"""
        try:
            return await engine.search(query, max_results)
        except Exception as e:
            logger.error(f"Error searching with {engine_name}: {e}")
            return {"success": False, "error": str(e), "engine": engine_name}
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results based on URL"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    async def _rank_results(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank search results by relevance"""
        # Simple ranking based on position and source
        # You can enhance this with more sophisticated ranking algorithms
        
        # Assign scores based on position
        for result in results:
            position = result.get("position", 100)
            source = result.get("source", "")
            
            # Base score from position (lower position = higher score)
            score = max(0, 100 - position)
            
            # Bonus for certain sources
            if source == "serper":
                score += 10
            elif source == "metaso":
                score += 5
            elif source == "sogou":
                score += 3
            
            # Check if query terms are in title or snippet
            query_terms = query.lower().split()
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            
            for term in query_terms:
                if term in title:
                    score += 5
                if term in snippet:
                    score += 2
            
            result["relevance_score"] = score
        
        # Sort by relevance score
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return results
    
    def get_available_engines(self) -> List[str]:
        """Get list of available search engines"""
        return list(self.engines.keys())
    
    def get_engine_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all search engines"""
        status = {}
        for engine_name, engine in self.engines.items():
            status[engine_name] = {
                "available": True,
                "type": type(engine).__name__,
                "config": engine.get_config() if hasattr(engine, 'get_config') else {}
            }
        return status