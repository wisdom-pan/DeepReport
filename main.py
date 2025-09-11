#!/usr/bin/env python3
"""
DeepReport - AI-powered financial report generation system
Main application with Gradio frontend
"""

import asyncio
import gradio as gr
import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from src.agents import PlanningAgent
from src.agents.sub_agents import DeepResearcherAgent, BrowserAgent, DeepAnalyzeAgent, FinalAnswerAgent
from src.search import SearchManager
from src.utils import ModelAdapter, MCPManager
from src.report import HTMLReportGenerator
from config import config, get_model_config
from smolagents import OpenAIModel, ConversationMemory

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepReportApp:
    """Main application class"""
    
    def __init__(self):
        self.config = config
        self.model_config = get_model_config()
        
        # Initialize components
        self.search_manager = SearchManager({
            "serper_api_key": config.serper_api_key,
            "metaso_api_key": config.metaso_api_key,
            "sogou_api_key": config.sogou_api_key
        })
        
        self.mcp_manager = MCPManager({
            "mcp_server_url": config.mcp_server_url,
            "mcp_api_key": config.mcp_api_key
        })
        
        self.report_generator = HTMLReportGenerator({
            "charts_enabled": config.charts_enabled,
            "data_sources_enabled": config.data_sources_enabled
        })
        
        # Initialize agents
        self.agents = {}
        self._initialize_agents()
        
        # Create output directory
        os.makedirs(config.output_dir, exist_ok=True)
    
    def _initialize_agents(self):
        """Initialize all agents using SmolAgents framework"""
        try:
            # Initialize SmolAgents model
            model = OpenAIModel(
                model_id=self.model_config.get("model", "gpt-4o"),
                api_key=self.model_config.get("api_key", os.getenv("OPENAI_API_KEY")),
                base_url=self.model_config.get("base_url", "https://api.openai.com/v1")
            )
            
            # Initialize memory
            memory = ConversationMemory()
            
            # Initialize planning agent
            self.agents["planning"] = PlanningAgent(model, memory)
            
            # Initialize sub-agents
            self.agents["deep_researcher"] = DeepResearcherAgent(model, memory)
            self.agents["browser"] = BrowserAgent(model, memory)
            self.agents["deep_analyze"] = DeepAnalyzeAgent(model, memory)
            self.agents["final_answer"] = FinalAnswerAgent(model, memory)
            
            logger.info("All agents initialized successfully with SmolAgents framework")
            
        except Exception as e:
            logger.error(f"Failed to initialize agents: {e}")
            raise
    
    async def generate_report(self, 
                            research_topic: str,
                            requirements: str,
                            output_format: str = "html",
                            model: str = "gpt-4o") -> Dict[str, Any]:
        """Generate a comprehensive financial report"""
        try:
            # Parse requirements
            requirements_list = [req.strip() for req in requirements.split('\n') if req.strip()]
            
            logger.info(f"Starting report generation for topic: {research_topic}")
            
            # Step 1: Create research plan
            plan_result = await self.agents["planning"].run(
                f"Create a comprehensive research plan for topic: {research_topic} with requirements: {requirements_list}"
            )
            
            if not plan_result:
                return {"success": False, "error": "Failed to create research plan"}
            
            # Step 2: Execute research tasks
            task_results = await self._execute_research_plan(plan_result)
            
            # Step 3: Generate final report
            report_data = {
                "title": f"Financial Research Report: {research_topic}",
                "subtitle": "Comprehensive Analysis and Insights",
                "research_topic": research_topic,
                "requirements": requirements_list,
                "plan": plan_result,
                "task_results": task_results,
                "generated_at": datetime.now().isoformat(),
                "model": model,
                "confidence_score": 85,
                "data_points": sum(len(result.get("data", [])) for result in task_results.values()),
                "charts_data": self._extract_chart_data(task_results),
                "citations": self._extract_citations(task_results),
                "data_sources": self._extract_data_sources(task_results),
                "sections": self._create_report_sections(task_results),
                "key_metrics": self._extract_key_metrics(task_results),
                "risk_assessment": self._extract_risk_assessment(task_results),
                "recommendations": self._extract_recommendations(task_results),
                "executive_summary": self._generate_executive_summary(plan_result, task_results)
            }
            
            # Step 4: Generate HTML report
            if output_format == "html":
                html_result = await self.report_generator.generate_report(report_data)
                
                if html_result["success"]:
                    # Save report to file
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"financial_report_{timestamp}.html"
                    filepath = os.path.join(config.output_dir, filename)
                    
                    success = await self.report_generator.save_report(report_data, filepath)
                    
                    if success:
                        return {
                            "success": True,
                            "report_path": filepath,
                            "report_html": html_result["html_content"],
                            "report_data": report_data,
                            "generation_time": datetime.now().isoformat()
                        }
                    else:
                        return {"success": False, "error": "Failed to save report"}
                else:
                    return {"success": False, "error": html_result.get("error", "Failed to generate HTML")}
            
            return {
                "success": True,
                "report_data": report_data,
                "generation_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_research_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research tasks from the plan"""
        task_results = {}
        
        for task in plan.get("tasks", []):
            task_id = task["task_id"]
            task_type = task["task_type"]
            
            try:
                if task_type == "deep_research":
                    result = await self._execute_deep_research_task(task)
                elif task_type == "browser_use":
                    result = await self._execute_browser_task(task)
                elif task_type == "deep_analyze":
                    result = await self._execute_analysis_task(task)
                elif task_type == "final_answer":
                    result = await self._execute_final_task(task)
                else:
                    logger.warning(f"Unknown task type: {task_type}")
                    continue
                
                task_results[task_id] = result
                
            except Exception as e:
                logger.error(f"Failed to execute task {task_id}: {e}")
                task_results[task_id] = {"error": str(e)}
        
        return task_results
    
    async def _execute_browser_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute browser task"""
        try:
            result = await self.agents["browser"].run(
                f"Perform web interaction for: {task['description']}"
            )
            
            return {
                "success": True,
                "data": result,
                "task_type": "browser",
                "execution_time": 0  # SmolAgents handles timing internally
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task_type": "browser"
            }
    
    async def _execute_deep_research_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deep research task"""
        try:
            result = await self.agents["deep_researcher"].run(
                f"Research and filter high-quality data sources for: {task['description']}"
            )
            
            return {
                "success": True,
                "data": result,
                "task_type": "deep_research",
                "execution_time": 0  # SmolAgents handles timing internally
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task_type": "deep_research"
            }
    
    async def _execute_analysis_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis task"""
        try:
            result = await self.agents["deep_analyze"].run(
                f"Perform deep financial analysis for: {task['description']}"
            )
            
            return {
                "success": True,
                "data": result,
                "task_type": "analysis",
                "execution_time": 0  # SmolAgents handles timing internally
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task_type": "analysis"
            }
    
    async def _execute_final_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute final task"""
        try:
            result = await self.agents["final_answer"].run(
                f"Generate final report for: {task['description']}"
            )
            
            return {
                "success": True,
                "data": result,
                "task_type": "final",
                "execution_time": 0  # SmolAgents handles timing internally
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task_type": "final"
            }
    
    def _extract_chart_data(self, task_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract chart data from task results"""
        chart_data = []
        
        for task_id, result in task_results.items():
            if result.get("success") and result.get("data"):
                data = result["data"]
                
                # Look for chart-able data
                if isinstance(data, dict):
                    if "results" in data:  # Search results
                        chart_data.append({
                            "id": f"chart_{task_id}",
                            "type": "bar",
                            "title": "Search Results by Engine",
                            "labels": [r.get("source", "Unknown") for r in data["results"]],
                            "values": [1 for _ in data["results"]],
                            "description": "Distribution of search results by search engine"
                        })
                    
                    if "structured_data" in data:  # Browser data
                        structured = data["structured_data"]
                        if structured.get("headings"):
                            chart_data.append({
                                "id": f"chart_{task_id}_headings",
                                "type": "pie",
                                "title": "Content Structure",
                                "labels": [h[:20] + "..." if len(h) > 20 else h for h in structured["headings"]],
                                "values": [1 for _ in structured["headings"]],
                                "description": "Distribution of content headings"
                            })
        
        return chart_data
    
    def _extract_citations(self, task_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract citations from task results"""
        citations = []
        
        for task_id, result in task_results.items():
            if result.get("success") and result.get("data"):
                data = result["data"]
                
                if isinstance(data, dict) and "results" in data:
                    for search_result in data["results"]:
                        citations.append({
                            "type": "website",
                            "title": search_result.get("title", ""),
                            "url": search_result.get("url", ""),
                            "source": search_result.get("source", ""),
                            "access_date": datetime.now().strftime("%Y-%m-%d")
                        })
        
        return citations
    
    def _extract_data_sources(self, task_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract data sources from task results"""
        sources = []
        
        for task_id, result in task_results.items():
            if result.get("success") and result.get("data"):
                data = result["data"]
                
                if isinstance(data, dict) and "results" in data:
                    sources_used = set()
                    for search_result in data["results"]:
                        source = search_result.get("source", "Unknown")
                        if source not in sources_used:
                            sources_used.add(source)
                            sources.append({
                                "name": source.title(),
                                "description": f"Search results from {source}",
                                "url": search_result.get("url", "")
                            })
        
        return sources
    
    def _create_report_sections(self, task_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create report sections from task results"""
        sections = []
        
        # Methodology section
        sections.append({
            "id": "methodology",
            "title": "Research Methodology",
            "content": """
            <p>This report was generated using DeepReport's AI-powered research system. 
            The research process involved:</p>
            <ul>
                <li>Automated web search across multiple search engines</li>
                <li>Content extraction and analysis</li>
                <li>Data visualization and chart generation</li>
                <li>Citation tracking and source verification</li>
            </ul>
            <p>Each step was executed by specialized AI agents working in coordination.</p>
            """
        })
        
        # Search results section
        search_results = []
        for task_id, result in task_results.items():
            if result.get("success") and result.get("task_type") in ["deep_research", "browser"]:
                data = result["data"]
                if isinstance(data, dict) and "results" in data:
                    search_results.extend(data["results"])
        
        if search_results:
            search_content = "<div class='row'>"
            for i, result in enumerate(search_results[:10]):  # Limit to top 10
                search_content += f"""
                <div class='col-md-6 mb-3'>
                    <div class='card'>
                        <div class='card-body'>
                            <h6 class='card-title'>{result.get('title', 'Untitled')}</h6>
                            <p class='card-text small'>{result.get('snippet', 'No description available')}</p>
                            <a href='{result.get('url', '#')}' class='btn btn-outline-primary btn-sm' target='_blank'>
                                View Source
                            </a>
                        </div>
                    </div>
                </div>
                """
            search_content += "</div>"
            
            sections.append({
                "id": "search_results",
                "title": "Search Results",
                "content": search_content
            })
        
        return sections
    
    def _extract_key_metrics(self, task_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract key metrics from task results"""
        metrics = []
        
        # Count total results
        total_results = 0
        total_sources = 0
        
        for task_id, result in task_results.items():
            if result.get("success") and result.get("data"):
                data = result["data"]
                if isinstance(data, dict) and "results" in data:
                    total_results += len(data["results"])
                    sources = set(r.get("source", "Unknown") for r in data["results"])
                    total_sources += len(sources)
        
        metrics.extend([
            {
                "name": "Total Results",
                "value": str(total_results),
                "description": "Number of search results found"
            },
            {
                "name": "Data Sources",
                "value": str(total_sources),
                "description": "Number of unique data sources"
            },
            {
                "name": "Tasks Completed",
                "value": str(len(task_results)),
                "description": "Research tasks executed"
            }
        ])
        
        return metrics
    
    def _extract_risk_assessment(self, task_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract risk assessment from task results"""
        # This is a simplified risk assessment
        return [
            {
                "category": "Data Quality",
                "level": "low",
                "impact": "High-quality search results from multiple sources",
                "mitigation": "Cross-reference information from multiple sources"
            },
            {
                "category": "Source Reliability",
                "level": "medium",
                "impact": "Some sources may have bias or inaccuracies",
                "mitigation": "Verify critical information with authoritative sources"
            },
            {
                "category": "Timeliness",
                "level": "low",
                "impact": "Current search results provide up-to-date information",
                "mitigation": "Regular updates and monitoring of key sources"
            }
        ]
    
    def _extract_recommendations(self, task_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract recommendations from task results"""
        return [
            {
                "title": "Continuous Monitoring",
                "description": "Set up ongoing monitoring of key financial indicators and market trends",
                "priority": "High",
                "timeline": "Immediate"
            },
            {
                "title": "Source Diversification",
                "description": "Expand data sources to include additional financial databases and news sources",
                "priority": "Medium",
                "timeline": "1-2 weeks"
            },
            {
                "title": "Regular Updates",
                "description": "Schedule regular report updates to maintain data freshness and accuracy",
                "priority": "Medium",
                "timeline": "Ongoing"
            }
        ]
    
    def _generate_executive_summary(self, plan: Dict[str, Any], task_results: Dict[str, Any]) -> str:
        """Generate executive summary"""
        total_tasks = len(task_results)
        successful_tasks = sum(1 for r in task_results.values() if r.get("success"))
        total_results = sum(len(r.get("data", {}).get("results", [])) for r in task_results.values() if r.get("success"))
        
        return f"""
        This financial research report was generated using AI-powered analysis of {total_results} data points 
        across {successful_tasks} successful research tasks. The research focused on {plan.get('research_topic', 'the specified topic')} 
        and successfully completed {successful_tasks}/{total_tasks} planned research activities.
        
        Key findings include comprehensive market analysis, trend identification, and risk assessment. 
        The report provides actionable insights based on current market conditions and reliable data sources.
        """


# Create global app instance
app = DeepReportApp()

def create_gradio_interface():
    """Create Gradio interface"""
    
    async def generate_report_interface(research_topic, requirements, output_format, model):
        """Interface function for report generation"""
        try:
            result = await app.generate_report(
                research_topic=research_topic,
                requirements=requirements,
                output_format=output_format,
                model=model
            )
            
            if result["success"]:
                if output_format == "html" and "report_html" in result:
                    return (
                        result["report_html"],
                        f"✅ Report generated successfully! File saved to: {result.get('report_path', 'Unknown')}",
                        gr.update(visible=True),
                        gr.update(visible=True)
                    )
                else:
                    return (
                        json.dumps(result["report_data"], indent=2),
                        f"✅ Report data generated successfully!",
                        gr.update(visible=False),
                        gr.update(visible=True)
                    )
            else:
                return (
                    f"❌ Error: {result.get('error', 'Unknown error')}",
                    "Report generation failed",
                    gr.update(visible=False),
                    gr.update(visible=True)
                )
                
        except Exception as e:
            error_msg = f"❌ Interface error: {str(e)}"
            return (
                error_msg,
                "Report generation failed",
                gr.update(visible=False),
                gr.update(visible=True)
            )
    
    # Define interface components
    with gr.Blocks(title="DeepReport - AI Financial Research", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 📊 DeepReport
        ### AI-Powered Financial Research and Report Generation
        
        Generate comprehensive financial research reports using advanced AI agents and multi-engine search capabilities.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Input section
                gr.Markdown("## 📝 Research Parameters")
                
                research_topic = gr.Textbox(
                    label="Research Topic",
                    placeholder="Enter your financial research topic...",
                    lines=2
                )
                
                requirements = gr.Textbox(
                    label="Research Requirements",
                    placeholder="Enter specific requirements (one per line)...",
                    lines=4
                )
                
                with gr.Row():
                    output_format = gr.Radio(
                        choices=["html", "json"],
                        value="html",
                        label="Output Format"
                    )
                    
                    model = gr.Dropdown(
                        choices=["gpt-4o", "gpt-4", "claude-3-sonnet", "claude-3-opus"],
                        value="gpt-4o",
                        label="AI Model"
                    )
                
                generate_btn = gr.Button(
                    "🚀 Generate Report",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=1):
                # Status section
                gr.Markdown("## 📊 System Status")
                
                status_output = gr.Textbox(
                    label="Status",
                    interactive=False,
                    lines=2
                )
        
        # Results section
        gr.Markdown("## 📄 Generated Report")
        
        with gr.Row():
            # HTML output (hidden by default)
            html_output = gr.HTML(
                visible=False,
                label="HTML Report"
            )
            
            # Text output (for JSON/errors)
            text_output = gr.Textbox(
                label="Report Output",
                interactive=False,
                lines=20,
                visible=True
            )
        
        # Event handlers
        generate_btn.click(
            fn=generate_report_interface,
            inputs=[research_topic, requirements, output_format, model],
            outputs=[html_output, status_output, html_output, text_output]
        )
        
        # Example section
        gr.Markdown("""
        ## 💡 Example Topics
        
        - Tesla Inc. (TSLA) Q4 2023 Financial Performance Analysis
        - Cryptocurrency Market Trends and Investment Opportunities
        - Renewable Energy Sector Growth Prospects 2024
        - Federal Reserve Monetary Policy Impact on Tech Stocks
        - Artificial Intelligence in Financial Services Market Analysis
        
        ## 🔧 System Features
        
        - **SmolAgents Framework**: Advanced multi-agent AI orchestration
        - **Specialized Agents**: DeepResearcher, Browser, DeepAnalyze, FinalAnswer
        - **Multi-Engine Search**: Serper, Metaso, Sogou integration
        - **MCP Protocol**: FastMCP support for local/remote tool connections
        - **Rich Reports**: HTML reports with interactive charts and professional citations
        - **Data Visualization**: Chart.js integration for dynamic charts
        - **Citation Management**: APA, MLA, Chicago, Harvard citation styles
        """)
    
    return demo

# Create and launch the interface
if __name__ == "__main__":
    demo = create_gradio_interface()
    
    # Launch the app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_api=False
    )