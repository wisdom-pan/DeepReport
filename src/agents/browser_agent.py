"""
Browser Agent for web interaction and PDF analysis using SmolAgents
"""

import asyncio
import json
import logging
import os
import tempfile
from typing import Dict, Any, List, Optional
from datetime import datetime
from urllib.parse import urlparse
import aiohttp
import fitz  # PyMuPDF for PDF processing
from browser_use import BrowserUse
from smolagents import Tool
from smolagents.memory import ConversationMemory
from smolagents.models import OpenAIModel

from .base_agent import BaseAgent, Task, TaskResult

logger = logging.getLogger(__name__)

class WebNavigationTool(Tool):
    """Tool for web navigation and interaction"""
    
    def __init__(self, browser: BrowserUse):
        super().__init__(
            name="navigate_web",
            description="Navigate and interact with web pages",
            parameters={
                "url": {
                    "type": "string",
                    "description": "URL to navigate to"
                },
                "actions": {
                    "type": "array",
                    "description": "List of actions to perform on the page",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["click", "fill", "scroll", "extract"]},
                            "target": {"type": "string"},
                            "value": {"type": "string"}
                        }
                    }
                }
            }
        )
        self.browser = browser
    
    async def run(self, url: str, actions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Navigate to URL and perform actions"""
        try:
            # Navigate to URL
            await self.browser.goto(url)
            
            # Extract basic page information
            title = await self.browser.get_title()
            content = await self.browser.get_text_content()
            
            # Perform actions
            action_results = []
            if actions:
                for action in actions:
                    result = await self._perform_action(action)
                    action_results.append(result)
            
            return {
                "url": url,
                "title": title,
                "content": content,
                "action_results": action_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Web navigation failed: {e}")
            return {"error": str(e)}
    
    async def _perform_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a single action on the page"""
        try:
            action_type = action.get("type")
            target = action.get("target")
            value = action.get("value")
            
            if action_type == "click":
                await self.browser.click_element(target)
                return {"action": "click", "target": target, "success": True}
            elif action_type == "fill":
                await self.browser.fill_input(target, value)
                return {"action": "fill", "target": target, "value": value, "success": True}
            elif action_type == "scroll":
                await self.browser.scroll_to_element(target)
                return {"action": "scroll", "target": target, "success": True}
            elif action_type == "extract":
                content = await self.browser.extract_element_text(target)
                return {"action": "extract", "target": target, "content": content, "success": True}
            else:
                return {"action": action_type, "target": target, "success": False, "error": "Unknown action type"}
                
        except Exception as e:
            return {"action": action.get("type", "unknown"), "target": action.get("target", "unknown"), "success": False, "error": str(e)}

class PDFAnalysisTool(Tool):
    """Tool for analyzing PDF documents"""
    
    def __init__(self):
        super().__init__(
            name="analyze_pdf",
            description="Analyze PDF documents for financial data and content",
            parameters={
                "pdf_path": {
                    "type": "string",
                    "description": "Path or URL to PDF document"
                },
                "extract_tables": {
                    "type": "boolean",
                    "description": "Whether to extract tables from PDF",
                    "default": True
                },
                "extract_charts": {
                    "type": "boolean",
                    "description": "Whether to extract chart information",
                    "default": True
                }
            }
        )
    
    async def run(self, pdf_path: str, extract_tables: bool = True, extract_charts: bool = True) -> Dict[str, Any]:
        """Analyze PDF document content"""
        try:
            # Check if it's a URL or local path
            if pdf_path.startswith("http"):
                # Download PDF from URL
                async with aiohttp.ClientSession() as session:
                    async with session.get(pdf_path) as response:
                        if response.status == 200:
                            pdf_data = await response.read()
                            # Save to temporary file
                            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                                temp_file.write(pdf_data)
                                pdf_path = temp_file.name
                        else:
                            return {"error": f"Failed to download PDF: {response.status}"}
            
            # Analyze PDF using PyMuPDF
            doc = fitz.open(pdf_path)
            
            analysis = {
                "metadata": doc.metadata,
                "page_count": len(doc),
                "word_count": 0,
                "sections": [],
                "tables": [],
                "charts": [],
                "financial_data": [],
                "full_text": ""
            }
            
            # Extract text and analyze structure
            full_text = ""
            for page_num, page in enumerate(doc):
                text = page.get_text()
                full_text += text
                
                # Basic section detection
                if text.strip():
                    analysis["sections"].append({
                        "page": page_num + 1,
                        "content": text[:500] + "..." if len(text) > 500 else text,
                        "word_count": len(text.split())
                    })
                
                # Extract tables
                if extract_tables:
                    tables = page.find_tables()
                    for table in tables:
                        analysis["tables"].append({
                            "page": page_num + 1,
                            "rows": len(table.rows()),
                            "cols": len(table.cols()),
                            "data": table.extract()
                        })
                
                # Look for financial data patterns
                financial_indicators = ["$", "%", "revenue", "profit", "loss", "EBITDA", "EPS", "P/E"]
                found_indicators = [indicator for indicator in financial_indicators if indicator.lower() in text.lower()]
                if found_indicators:
                    analysis["financial_data"].append({
                        "page": page_num + 1,
                        "indicators": found_indicators,
                        "context": text[:200]
                    })
            
            analysis["full_text"] = full_text
            analysis["word_count"] = len(full_text.split())
            
            # Clean up temporary file if created
            if pdf_path.startswith("/tmp/"):
                os.unlink(pdf_path)
            
            doc.close()
            
            return analysis
            
        except Exception as e:
            logger.error(f"PDF analysis failed: {e}")
            return {"error": str(e)}

class StructuredDataExtractionTool(Tool):
    """Tool for extracting structured data from web pages"""
    
    def __init__(self, browser: BrowserUse):
        super().__init__(
            name="extract_structured_data",
            description="Extract structured data (tables, forms, lists) from web pages",
            parameters={
                "url": {
                    "type": "string",
                    "description": "URL to extract data from"
                },
                "data_types": {
                    "type": "array",
                    "description": "Types of data to extract",
                    "items": {"type": "string", "enum": ["tables", "forms", "lists", "links", "images"]},
                    "default": ["tables", "forms", "lists"]
                }
            }
        )
        self.browser = browser
    
    async def run(self, url: str, data_types: List[str] = None) -> Dict[str, Any]:
        """Extract structured data from web page"""
        try:
            if data_types is None:
                data_types = ["tables", "forms", "lists"]
            
            await self.browser.goto(url)
            
            structured_data = {
                "url": url,
                "title": await self.browser.get_title(),
                "extracted_data": {}
            }
            
            # Extract different types of structured data
            if "tables" in data_types:
                tables = await self.browser.get_tables()
                structured_data["extracted_data"]["tables"] = tables
            
            if "forms" in data_types:
                forms = await self.browser.get_forms()
                structured_data["extracted_data"]["forms"] = forms
            
            if "lists" in data_types:
                lists = await self.browser.get_lists()
                structured_data["extracted_data"]["lists"] = lists
            
            if "links" in data_types:
                links = await self.browser.get_links()
                structured_data["extracted_data"]["links"] = links
            
            if "images" in data_types:
                images = await self.browser.get_images()
                structured_data["extracted_data"]["images"] = images
            
            return structured_data
            
        except Exception as e:
            logger.error(f"Structured data extraction failed: {e}")
            return {"error": str(e)}

class FormInteractionTool(Tool):
    """Tool for interacting with web forms"""
    
    def __init__(self, browser: BrowserUse):
        super().__init__(
            name="interact_with_form",
            description="Fill and submit web forms",
            parameters={
                "url": {
                    "type": "string",
                    "description": "URL containing the form"
                },
                "form_data": {
                    "type": "object",
                    "description": "Form field names and values to fill"
                },
                "submit_button": {
                    "type": "string",
                    "description": "Selector for the submit button"
                }
            }
        )
        self.browser = browser
    
    async def run(self, url: str, form_data: Dict[str, Any], submit_button: str = None) -> Dict[str, Any]:
        """Interact with web forms"""
        try:
            await self.browser.goto(url)
            
            # Fill form fields
            for field_name, field_value in form_data.items():
                await self.browser.fill_input(field_name, field_value)
            
            # Submit form if button specified
            if submit_button:
                await self.browser.click_button(submit_button)
            
            # Extract results after form submission
            result_content = await self.browser.get_text_content()
            
            return {
                "url": url,
                "form_data": form_data,
                "submitted": submit_button is not None,
                "result_content": result_content,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Form interaction failed: {e}")
            return {"error": str(e)}

class BrowserAgent(BaseAgent):
    """Agent for fine-grained web interaction using browser-use library and SmolAgents"""
    
    def __init__(self, model: OpenAIModel, memory: ConversationMemory = None):
        super().__init__(
            name="BrowserAgent",
            model=model,
            memory=memory or ConversationMemory()
        )
        
        self.browser = None
        self.browser_initialized = False
        
    async def start(self):
        """Start the browser agent"""
        await super().start()
        await self._initialize_browser()
        await self._setup_tools()
        
    async def _initialize_browser(self):
        """Initialize browser-use instance"""
        try:
            self.browser = BrowserUse()
            self.browser_initialized = True
            logger.info("Browser-use initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize browser-use: {e}")
            raise
    
    async def _setup_tools(self):
        """Setup browser tools"""
        if self.browser_initialized:
            self.add_custom_tool(WebNavigationTool(self.browser))
            self.add_custom_tool(StructuredDataExtractionTool(self.browser))
            self.add_custom_tool(FormInteractionTool(self.browser))
        
        self.add_custom_tool(PDFAnalysisTool())
    
    async def execute_task(self, task: Task) -> TaskResult:
        """Execute browser-related tasks using SmolAgents"""
        start_time = datetime.now()
        
        try:
            task_type = task.parameters.get("browser_task_type")
            url = task.parameters.get("url")
            query = task.parameters.get("query")
            action = task.parameters.get("action")
            pdf_path = task.parameters.get("pdf_path")
            
            # Create task description for SmolAgents
            task_description = f"Perform browser task: {task_type or 'web interaction'}"
            
            if url:
                task_description += f" on {url}"
            if query:
                task_description += f" with query: {query}"
            
            # Use SmolAgents to orchestrate the task
            result = await self.run_task_with_smolagents(task_description)
            
            if result.get("success"):
                browser_result = result.get("result", {})
                
                # Enhance with specific browser operations
                enhanced_result = await self._enhance_browser_result(browser_result, task)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=enhanced_result,
                    execution_time=execution_time,
                    metadata={
                        "url": url,
                        "query": query,
                        "task_type": task_type,
                        "action": action,
                        "method": "smolagents"
                    }
                )
            else:
                # Fallback to traditional method
                fallback_result = await self._execute_traditional_browser_task(task)
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
    
    async def _enhance_browser_result(self, smolagents_result: Dict[str, Any], task: Task) -> Dict[str, Any]:
        """Enhance SmolAgents result with browser-specific operations"""
        try:
            task_type = task.parameters.get("browser_task_type")
            url = task.parameters.get("url")
            
            if task_type == "web_navigation" and url:
                # Perform actual web navigation
                navigation_tool = WebNavigationTool(self.browser)
                navigation_result = await navigation_tool.run(url)
                smolagents_result.update(navigation_result)
            
            elif task_type == "pdf_analysis":
                pdf_path = task.parameters.get("pdf_path") or url
                if pdf_path:
                    pdf_tool = PDFAnalysisTool()
                    pdf_result = await pdf_tool.run(pdf_path)
                    smolagents_result.update(pdf_result)
            
            elif task_type == "structured_data_extraction" and url:
                extraction_tool = StructuredDataExtractionTool(self.browser)
                extraction_result = await extraction_tool.run(url)
                smolagents_result.update(extraction_result)
            
            # Add metadata
            smolagents_result["enhanced_at"] = datetime.now().isoformat()
            smolagents_result["enhanced_by"] = "BrowserAgent"
            
            return smolagents_result
            
        except Exception as e:
            logger.error(f"Failed to enhance browser result: {e}")
            return smolagents_result
    
    async def _execute_traditional_browser_task(self, task: Task) -> TaskResult:
        """Fallback traditional browser task execution"""
        try:
            task_type = task.parameters.get("browser_task_type")
            url = task.parameters.get("url")
            action = task.parameters.get("action")
            pdf_path = task.parameters.get("pdf_path")
            
            if task_type == "web_navigation":
                result = await self._perform_web_navigation(url, action)
            elif task_type == "pdf_analysis":
                result = await self._analyze_pdf_document(pdf_path or url)
            elif task_type == "form_interaction":
                result = await self._interact_with_form(url, action)
            elif task_type == "structured_data_extraction":
                result = await self._extract_structured_data(url)
            else:
                result = {"error": f"Unknown browser task type: {task_type}"}
            
            return TaskResult(
                task_id=task.id,
                success="error" not in result,
                result=result if "error" not in result else None,
                error=result.get("error") if "error" in result else None,
                metadata={
                    "url": url,
                    "task_type": task_type,
                    "method": "traditional"
                }
            )
            
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e)
            )
    
    async def _perform_web_navigation(self, url: str, action: str) -> Dict[str, Any]:
        """Perform web navigation and interaction"""
        try:
            await self.browser.goto(url)
            
            title = await self.browser.get_title()
            content = await self.browser.get_text_content()
            
            action_results = {}
            if action:
                action_results = await self._execute_browser_action(action)
            
            return {
                "url": url,
                "title": title,
                "content": content,
                "action_results": action_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to perform web navigation: {str(e)}"}
    
    async def _analyze_pdf_document(self, pdf_path: str) -> Dict[str, Any]:
        """Analyze PDF document content"""
        try:
            pdf_tool = PDFAnalysisTool()
            return await pdf_tool.run(pdf_path)
            
        except Exception as e:
            return {"error": f"Failed to analyze PDF: {str(e)}"}
    
    async def _interact_with_form(self, url: str, action: Dict[str, Any]) -> Dict[str, Any]:
        """Interact with web forms"""
        try:
            form_tool = FormInteractionTool(self.browser)
            form_data = action.get("fields", {})
            submit_button = action.get("submit")
            
            return await form_tool.run(url, form_data, submit_button)
            
        except Exception as e:
            return {"error": f"Failed to interact with form: {str(e)}"}
    
    async def _extract_structured_data(self, url: str) -> Dict[str, Any]:
        """Extract structured data from web pages"""
        try:
            extraction_tool = StructuredDataExtractionTool(self.browser)
            return await extraction_tool.run(url)
            
        except Exception as e:
            return {"error": f"Failed to extract structured data: {str(e)}"}
    
    async def _execute_browser_action(self, action_description: str) -> Dict[str, Any]:
        """Execute browser action based on natural language description"""
        try:
            # Use AI to interpret the action
            prompt = f"""
            Interpret this browser action: "{action_description}"
            
            Return a JSON object with:
            {{
                "action_type": "click" | "fill" | "scroll" | "extract" | "navigate",
                "target": "element description or selector",
                "value": "value to fill (if applicable)",
                "confidence": 0.0 to 1.0
            }}
            """
            
            response = await self.model.generate_structured_response(
                prompt,
                {
                    "action_type": "",
                    "target": "",
                    "value": "",
                    "confidence": 0.0
                }
            )
            
            if response.get("success") and response["content"]["confidence"] > 0.7:
                action = response["content"]
                
                if action["action_type"] == "click":
                    await self.browser.click_element(action["target"])
                elif action["action_type"] == "fill":
                    await self.browser.fill_input(action["target"], action["value"])
                elif action["action_type"] == "scroll":
                    await self.browser.scroll_to_element(action["target"])
                elif action["action_type"] == "extract":
                    content = await self.browser.extract_element_text(action["target"])
                    return {"content": content, "interpreted_action": action}
                
                return {"interpreted_action": action, "executed": True}
            else:
                return {"error": "Could not interpret action with sufficient confidence"}
                
        except Exception as e:
            return {"error": f"Failed to execute browser action: {str(e)}"}
    
    async def stop(self):
        """Stop the browser agent"""
        if self.browser:
            await self.browser.close()
        await super().stop()
    
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        return [
            "web_navigation",
            "pdf_analysis",
            "form_interaction",
            "structured_data_extraction",
            "content_interaction",
            "ai_guided_browsing",
            "smolagents_integration"
        ]
    
    async def browse_with_smolagents(self, url: str, task: str) -> Dict[str, Any]:
        """Browse website using SmolAgents framework directly"""
        try:
            # Create comprehensive browsing task
            task_description = f"""
            Browse and interact with website: {url}
            
            Task: {task}
            
            Please:
            1. Navigate to the URL
            2. Understand the page structure
            3. Perform necessary interactions
            4. Extract relevant information
            5. Provide structured results
            """
            
            result = await self.run_task_with_smolagents(task_description)
            
            if result.get("success"):
                return result.get("result", {})
            else:
                raise Exception(f"SmolAgents browsing failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"SmolAgents browsing failed: {e}")
            raise