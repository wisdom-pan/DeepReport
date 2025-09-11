"""
Deep Researcher Agent for filtering high-quality data sources using SmolAgents
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from urllib.parse import urlparse
from smolagents import Tool
from smolagents.memory import ConversationMemory
from smolagents.models import OpenAIModel
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .base_agent import BaseAgent, Task, TaskResult

logger = logging.getLogger(__name__)

class SourceDiscoveryTool(Tool):
    """Tool for discovering high-quality data sources"""
    
    def __init__(self):
        super().__init__(
            name="discover_sources",
            description="Search for high-quality financial data sources and research materials",
            parameters={
                "query": {
                    "type": "string",
                    "description": "Search query for financial data sources"
                },
                "source_type": {
                    "type": "string",
                    "description": "Type of sources to find (news, reports, data, analysis)",
                    "default": "all"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                }
            }
        )
    
    async def run(self, query: str, source_type: str = "all", max_results: int = 10) -> Dict[str, Any]:
        """Discover high-quality sources for financial research"""
        try:
            # Use DuckDuckGo for initial search
            search_tool = DuckDuckGoSearchRun()
            search_results = search_tool.run(query)
            
            # Parse and filter results
            sources = []
            high_quality_domains = [
                "bloomberg.com", "reuters.com", "wsj.com", "ft.com", "economist.com",
                "sec.gov", "yahoo.com", "marketwatch.com", "seekingalpha.com",
                "morningstar.com", "investopedia.com", "cnbc.com"
            ]
            
            lines = search_results.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and i < max_results:
                    if 'http' in line:
                        parts = line.split('http', 1)
                        if len(parts) > 1:
                            url = 'http' + parts[1].split()[0]
                            title = parts[0].strip()
                            domain = urlparse(url).netloc.lower()
                            
                            # Quality assessment
                            quality_score = 0.5
                            for quality_domain in high_quality_domains:
                                if quality_domain in domain:
                                    quality_score = 0.9
                                    break
                            
                            sources.append({
                                "url": url,
                                "title": title,
                                "domain": domain,
                                "quality_score": quality_score,
                                "source_type": source_type
                            })
            
            return {
                "sources": sources,
                "total_found": len(sources),
                "query": query,
                "high_quality_count": len([s for s in sources if s["quality_score"] >= 0.8])
            }
            
        except Exception as e:
            logger.error(f"Source discovery failed: {e}")
            return {"error": str(e)}

class ContentExtractionTool(Tool):
    """Tool for extracting content from web sources"""
    
    def __init__(self):
        super().__init__(
            name="extract_content",
            description="Extract and analyze content from web sources",
            parameters={
                "urls": {
                    "type": "array",
                    "description": "List of URLs to extract content from",
                    "items": {"type": "string"}
                },
                "max_content_length": {
                    "type": "integer",
                    "description": "Maximum content length per source",
                    "default": 2000
                }
            }
        )
    
    async def run(self, urls: List[str], max_content_length: int = 2000) -> Dict[str, Any]:
        """Extract content from multiple web sources"""
        try:
            extracted_content = []
            
            for url in urls:
                try:
                    # Use WebBaseLoader for content extraction
                    loader = WebBaseLoader([url])
                    documents = loader.load()
                    
                    if documents:
                        # Split content into manageable chunks
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1000,
                            chunk_overlap=200
                        )
                        chunks = text_splitter.split_documents(documents)
                        
                        # Get main content
                        main_content = chunks[0].page_content if chunks else ""
                        if len(main_content) > max_content_length:
                            main_content = main_content[:max_content_length]
                        
                        extracted_content.append({
                            "url": url,
                            "content": main_content,
                            "chunks_count": len(chunks),
                            "content_length": len(main_content)
                        })
                    
                    # Small delay to avoid overwhelming servers
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.warning(f"Failed to extract content from {url}: {e}")
                    continue
            
            return {
                "extracted_content": extracted_content,
                "total_sources": len(urls),
                "successful_extractions": len(extracted_content),
                "total_content_length": sum(c["content_length"] for c in extracted_content)
            }
            
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            return {"error": str(e)}

class QualityAssessmentTool(Tool):
    """Tool for assessing content quality"""
    
    def __init__(self):
        super().__init__(
            name="assess_quality",
            description="Assess the quality and relevance of extracted content",
            parameters={
                "content_data": {
                    "type": "array",
                    "description": "Array of content objects to assess"
                },
                "research_topic": {
                    "type": "string",
                    "description": "The research topic for relevance assessment"
                }
            }
        )
    
    async def run(self, content_data: List[Dict[str, Any]], research_topic: str) -> Dict[str, Any]:
        """Assess quality and relevance of content"""
        try:
            quality_assessments = []
            
            for content in content_data:
                content_text = content.get("content", "")
                url = content.get("url", "")
                
                # Quality metrics
                quality_metrics = {
                    "content_length": len(content_text),
                    "readability_score": self._calculate_readability(content_text),
                    "relevance_score": self._calculate_relevance(content_text, research_topic),
                    "source_credibility": self._assess_source_credibility(url),
                    "data_richness": self._assess_data_richness(content_text)
                }
                
                # Overall quality score
                overall_score = (
                    quality_metrics["readability_score"] * 0.2 +
                    quality_metrics["relevance_score"] * 0.3 +
                    quality_metrics["source_credibility"] * 0.3 +
                    quality_metrics["data_richness"] * 0.2
                )
                
                quality_metrics["overall_score"] = overall_score
                
                quality_assessments.append({
                    "url": url,
                    "quality_metrics": quality_metrics,
                    "recommendation": "include" if overall_score >= 0.7 else "review"
                })
            
            return {
                "quality_assessments": quality_assessments,
                "average_quality_score": sum(a["quality_metrics"]["overall_score"] for a in quality_assessments) / len(quality_assessments) if quality_assessments else 0,
                "recommended_sources": len([a for a in quality_assessments if a["recommendation"] == "include"])
            }
            
        except Exception as e:
            logger.error(f"Quality assessment failed: {e}")
            return {"error": str(e)}
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score (simplified)"""
        if not text:
            return 0.0
        
        # Simple metrics
        sentences = text.split('.')
        words = text.split()
        
        if len(sentences) == 0 or len(words) == 0:
            return 0.0
        
        avg_words_per_sentence = len(words) / len(sentences)
        
        # Normalize to 0-1 scale
        if avg_words_per_sentence > 25:
            return 0.3
        elif avg_words_per_sentence < 10:
            return 0.5
        else:
            return 0.8
    
    def _calculate_relevance(self, text: str, topic: str) -> float:
        """Calculate relevance score to research topic"""
        if not text or not topic:
            return 0.0
        
        # Simple keyword matching
        topic_lower = topic.lower()
        text_lower = text.lower()
        
        topic_words = topic_lower.split()
        matches = sum(1 for word in topic_words if word in text_lower)
        
        return min(matches / len(topic_words), 1.0)
    
    def _assess_source_credibility(self, url: str) -> float:
        """Assess source credibility based on URL"""
        high_quality_domains = [
            "bloomberg.com", "reuters.com", "wsj.com", "ft.com", "economist.com",
            "sec.gov", "yahoo.com", "marketwatch.com", "seekingalpha.com",
            "morningstar.com", "investopedia.com", "cnbc.com"
        ]
        
        domain = urlparse(url).netloc.lower()
        
        for quality_domain in high_quality_domains:
            if quality_domain in domain:
                return 0.9
        
        # Default credibility
        return 0.5
    
    def _assess_data_richness(self, text: str) -> float:
        """Assess data richness in content"""
        if not text:
            return 0.0
        
        # Look for data indicators
        data_indicators = ["%", "$", "billion", "million", "data", "statistics", "figures", "chart", "table"]
        indicator_count = sum(1 for indicator in data_indicators if indicator in text.lower())
        
        return min(indicator_count / len(data_indicators), 1.0)

class DeepResearcherAgent(BaseAgent):
    """Agent for filtering high-quality data sources and research using SmolAgents"""
    
    def __init__(self, model: OpenAIModel, memory: ConversationMemory = None):
        super().__init__(
            name="DeepResearcherAgent",
            model=model,
            memory=memory or ConversationMemory()
        )
        
        # Add research tools
        self.add_custom_tool(SourceDiscoveryTool())
        self.add_custom_tool(ContentExtractionTool())
        self.add_custom_tool(QualityAssessmentTool())
        
        self.high_quality_sources = [
            "bloomberg.com", "reuters.com", "wsj.com", "ft.com", "economist.com",
            "sec.gov", "yahoo.com", "marketwatch.com", "seekingalpha.com",
            "morningstar.com", "investopedia.com", "cnbc.com"
        ]
    
    async def execute_task(self, task: Task) -> TaskResult:
        """Execute deep research tasks using SmolAgents"""
        start_time = datetime.now()
        
        try:
            research_topic = task.parameters.get("research_topic")
            query = task.parameters.get("query")
            source_filter = task.parameters.get("source_filter", True)
            
            if not research_topic and not query:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    error="Research topic or query is required"
                )
            
            # Use SmolAgents to orchestrate the research process
            task_description = f"Research and filter high-quality sources for: {research_topic or query}"
            
            if source_filter:
                task_description += " with strict quality filtering"
            
            result = await self.run_task_with_smolagents(task_description)
            
            if result.get("success"):
                research_result = result.get("result", {})
                
                # Enhance with additional processing
                enhanced_result = await self._enhance_research_result(research_result, research_topic)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=enhanced_result,
                    execution_time=execution_time,
                    metadata={
                        "research_topic": research_topic,
                        "source_filter": source_filter,
                        "method": "smolagents",
                        "total_sources": len(enhanced_result.get("sources", []))
                    }
                )
            else:
                # Fallback to traditional method
                fallback_result = await self._execute_traditional_research(task)
                fallback_result.execution_time = (datetime.now() - start_time).total_seconds()
                return fallback_result
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    async def _enhance_research_result(self, smolagents_result: Dict[str, Any], research_topic: str) -> Dict[str, Any]:
        """Enhance SmolAgents result with additional analysis"""
        try:
            # Extract sources from SmolAgents result
            sources = smolagents_result.get("sources", [])
            
            # Perform additional quality filtering
            if sources:
                quality_analysis = await self._perform_quality_analysis(sources, research_topic)
                smolagents_result["quality_analysis"] = quality_analysis
            
            # Add metadata
            smolagents_result["enhanced_at"] = datetime.now().isoformat()
            smolagents_result["enhanced_by"] = "DeepResearcherAgent"
            
            return smolagents_result
            
        except Exception as e:
            logger.error(f"Failed to enhance research result: {e}")
            return smolagents_result
    
    async def _perform_quality_analysis(self, sources: List[Dict[str, Any]], research_topic: str) -> Dict[str, Any]:
        """Perform quality analysis on discovered sources"""
        try:
            # Use the quality assessment tool
            quality_tool = QualityAssessmentTool()
            
            # Prepare content data for quality assessment
            content_data = []
            for source in sources:
                content_data.append({
                    "url": source.get("url", ""),
                    "content": source.get("content", ""),
                    "title": source.get("title", "")
                })
            
            quality_result = await quality_tool.run(content_data, research_topic)
            return quality_result
            
        except Exception as e:
            logger.error(f"Quality analysis failed: {e}")
            return {"error": str(e)}
    
    async def _execute_traditional_research(self, task: Task) -> TaskResult:
        """Fallback traditional research method"""
        try:
            research_topic = task.parameters.get("research_topic")
            query = task.parameters.get("query")
            source_filter = task.parameters.get("source_filter", True)
            
            # Traditional research logic
            search_query = query or research_topic
            
            # Use source discovery tool
            discovery_tool = SourceDiscoveryTool()
            discovery_result = await discovery_tool.run(search_query)
            
            if "error" in discovery_result:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    error=discovery_result["error"]
                )
            
            sources = discovery_result.get("sources", [])
            
            # Extract content from sources
            if sources:
                urls = [s["url"] for s in sources[:5]]  # Top 5 sources
                extraction_tool = ContentExtractionTool()
                extraction_result = await extraction_tool.run(urls)
                
                if "error" not in extraction_result:
                    discovery_result.update(extraction_result)
            
            return TaskResult(
                task_id=task.id,
                success=True,
                result=discovery_result,
                metadata={
                    "research_topic": research_topic,
                    "source_filter": source_filter,
                    "method": "traditional"
                }
            )
            
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e)
            )
    
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        return [
            "source_discovery",
            "quality_filtering",
            "content_extraction",
            "research_analysis",
            "data_curation",
            "smolagents_integration"
        ]
    
    async def research_with_smolagents(self, research_topic: str, requirements: List[str] = None) -> Dict[str, Any]:
        """Perform research using SmolAgents framework directly"""
        try:
            # Create a comprehensive research task
            task_description = f"""
            Conduct comprehensive financial research on: {research_topic}
            
            Research requirements:
            - Discover high-quality data sources
            - Filter sources by credibility and relevance
            - Extract and analyze content
            - Provide quality assessment
            - Return structured research data
            
            Additional requirements: {', '.join(requirements) if requirements else 'None specified'}
            """
            
            result = await self.run_task_with_smolagents(task_description)
            
            if result.get("success"):
                return result.get("result", {})
            else:
                raise Exception(f"SmolAgents research failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"SmolAgents research failed: {e}")
            raise