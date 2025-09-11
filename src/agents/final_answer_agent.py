"""
Final Answer Agent for HTML report generation and quality assessment using SmolAgents
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from smolagents import Tool
from smolagents.memory import ConversationMemory
from smolagents.models import OpenAIModel

from .base_agent import BaseAgent, Task, TaskResult

logger = logging.getLogger(__name__)

class HTMLReportTool(Tool):
    """Tool for generating HTML reports"""
    
    def __init__(self):
        super().__init__(
            name="generate_html_report",
            description="Generate comprehensive HTML financial reports",
            parameters={
                "report_data": {
                    "type": "object",
                    "description": "Report data and content"
                },
                "template_style": {
                    "type": "string",
                    "description": "Report template style",
                    "enum": ["professional", "modern", "academic", "executive"],
                    "default": "professional"
                },
                "include_charts": {
                    "type": "boolean",
                    "description": "Whether to include interactive charts",
                    "default": True
                },
                "include_citations": {
                    "type": "boolean",
                    "description": "Whether to include citations and references",
                    "default": True
                }
            }
        )
    
    async def run(self, report_data: Dict[str, Any], template_style: str = "professional", include_charts: bool = True, include_citations: bool = True) -> Dict[str, Any]:
        """Generate HTML report"""
        try:
            # Generate HTML content
            html_content = await self._generate_html_content(report_data, template_style, include_charts, include_citations)
            
            return {
                "format": "html",
                "content": html_content,
                "template_style": template_style,
                "includes_charts": include_charts,
                "includes_citations": include_citations,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"HTML report generation failed: {e}")
            return {"error": str(e)}
    
    async def _generate_html_content(self, report_data: Dict[str, Any], template_style: str, include_charts: bool, include_citations: bool) -> str:
        """Generate HTML content for the report"""
        try:
            title = report_data.get("title", "Financial Research Report")
            executive_summary = report_data.get("executive_summary", "")
            sections = report_data.get("sections", [])
            charts = report_data.get("charts", [])
            citations = report_data.get("citations", [])
            
            # CSS styling based on template
            css_styles = self._get_css_styles(template_style)
            
            # Chart.js integration
            charts_js = ""
            if include_charts and charts:
                charts_js = self._generate_charts_js(charts)
            
            # Citations section
            citations_html = ""
            if include_citations and citations:
                citations_html = self._generate_citations_html(citations)
            
            # Generate HTML
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <style>{css_styles}</style>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
            <body>
                <div class="container">
                    <header class="report-header">
                        <h1>{title}</h1>
                        <p class="report-date">Generated on {datetime.now().strftime('%B %d, %Y')}</p>
                    </header>
                    
                    <section class="executive-summary">
                        <h2>Executive Summary</h2>
                        <p>{executive_summary}</p>
                    </section>
                    
                    <main class="report-content">
            """
            
            # Add sections
            for section in sections:
                section_title = section.get("title", "")
                section_content = section.get("content", "")
                html += f"""
                        <section class="report-section">
                            <h2>{section_title}</h2>
                            <div class="section-content">
                                {section_content}
                            </div>
                        </section>
                """
            
            # Add charts
            if include_charts and charts:
                html += """
                        <section class="charts-section">
                            <h2>Data Visualizations</h2>
                            <div class="charts-container">
                """
                for i, chart in enumerate(charts):
                    html += f'                                <canvas id="chart{i}" width="400" height="200"></canvas>\n'
                html += """
                            </div>
                        </section>
                """
            
            # Add citations
            if include_citations and citations:
                html += f"""
                        <section class="citations-section">
                            <h2>References and Citations</h2>
                            <div class="citations-content">
                                {citations_html}
                            </div>
                        </section>
                """
            
            html += """
                    </main>
                    
                    <footer class="report-footer">
                        <p>Generated by DeepReport AI System</p>
                    </footer>
                </div>
                
                <script>
            """
            
            # Add chart JavaScript
            if include_charts and charts:
                html += charts_js
            
            html += """
                </script>
            </body>
            </html>
            """
            
            return html
            
        except Exception as e:
            logger.error(f"HTML content generation failed: {e}")
            return f"<html><body><h1>Error generating report</h1><p>{str(e)}</p></body></html>"
    
    def _get_css_styles(self, template_style: str) -> str:
        """Get CSS styles based on template"""
        base_styles = """
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f9f9f9;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            
            .report-header {
                text-align: center;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 2px solid #007bff;
            }
            
            .report-header h1 {
                color: #007bff;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .report-date {
                color: #666;
                font-size: 1.1em;
            }
            
            .executive-summary {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
            }
            
            .executive-summary h2 {
                color: #007bff;
                margin-bottom: 15px;
            }
            
            .report-section {
                margin-bottom: 40px;
            }
            
            .report-section h2 {
                color: #007bff;
                margin-bottom: 20px;
                font-size: 1.8em;
            }
            
            .section-content {
                line-height: 1.8;
            }
            
            .charts-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .citations-content {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
            }
            
            .citations-content h3 {
                margin-bottom: 15px;
                color: #007bff;
            }
            
            .citation-item {
                margin-bottom: 10px;
                padding: 10px;
                background-color: white;
                border-left: 4px solid #007bff;
            }
            
            .report-footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
            }
        """
        
        if template_style == "modern":
            return base_styles + """
                body {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                
                .container {
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 15px;
                }
                
                .report-header h1 {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
            """
        elif template_style == "academic":
            return base_styles + """
                body {
                    background-color: #f5f5f5;
                }
                
                .container {
                    background-color: white;
                    border: 1px solid #ddd;
                }
                
                .report-header h1 {
                    color: #2c3e50;
                }
                
                .report-section h2 {
                    color: #2c3e50;
                }
                
                .citation-item {
                    border-left-color: #2c3e50;
                }
            """
        elif template_style == "executive":
            return base_styles + """
                body {
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                }
                
                .container {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }
                
                .report-header h1 {
                    color: #4CAF50;
                }
                
                .executive-summary {
                    background-color: #3d3d3d;
                }
                
                .report-section h2 {
                    color: #4CAF50;
                }
            """
        else:  # professional
            return base_styles
    
    def _generate_charts_js(self, charts: List[Dict[str, Any]]) -> str:
        """Generate JavaScript for charts"""
        js_code = ""
        
        for i, chart in enumerate(charts):
            chart_type = chart.get("type", "line")
            chart_data = chart.get("data", {})
            chart_title = chart.get("title", f"Chart {i+1}")
            
            js_code += f"""
                    const ctx{i} = document.getElementById('chart{i}').getContext('2d');
                    new Chart(ctx{i}, {{
                        type: '{chart_type}',
                        data: {json.dumps(chart_data)},
                        options: {{
                            responsive: true,
                            plugins: {{
                                title: {{
                                    display: true,
                                    text: '{chart_title}'
                                }}
                            }}
                        }}
                    }});
            """
        
        return js_code
    
    def _generate_citations_html(self, citations: List[Dict[str, Any]]) -> str:
        """Generate HTML for citations"""
        html = ""
        
        for citation in citations:
            citation_type = citation.get("type", "webpage")
            title = citation.get("title", "")
            author = citation.get("author", "")
            url = citation.get("url", "")
            date = citation.get("date", "")
            
            if citation_type == "webpage":
                html += f"""
                                <div class="citation-item">
                                    <strong>{title}</strong>
                                    <br>{author}
                                    <br><a href="{url}" target="_blank">{url}</a>
                                    <br>{date}
                                </div>
                """
            elif citation_type == "academic":
                html += f"""
                                <div class="citation-item">
                                    <strong>{title}</strong>
                                    <br>{author}
                                    <br>{date}
                                </div>
                """
            else:
                html += f"""
                                <div class="citation-item">
                                    <strong>{title}</strong>
                                    <br>{citation.get('description', '')}
                                </div>
                """
        
        return html

class MarkdownReportTool(Tool):
    """Tool for generating Markdown reports"""
    
    def __init__(self):
        super().__init__(
            name="generate_markdown_report",
            description="Generate comprehensive Markdown financial reports",
            parameters={
                "report_data": {
                    "type": "object",
                    "description": "Report data and content"
                },
                "include_toc": {
                    "type": "boolean",
                    "description": "Whether to include table of contents",
                    "default": True
                }
            }
        )
    
    async def run(self, report_data: Dict[str, Any], include_toc: bool = True) -> Dict[str, Any]:
        """Generate Markdown report"""
        try:
            title = report_data.get("title", "Financial Research Report")
            executive_summary = report_data.get("executive_summary", "")
            sections = report_data.get("sections", [])
            citations = report_data.get("citations", [])
            
            # Generate markdown content
            markdown_content = f"# {title}\n\n"
            markdown_content += f"*Generated on {datetime.now().strftime('%B %d, %Y')}*\n\n"
            
            # Table of contents
            if include_toc:
                markdown_content += "## Table of Contents\n\n"
                markdown_content += "1. [Executive Summary](#executive-summary)\n"
                for i, section in enumerate(sections, 2):
                    section_title = section.get("title", f"Section {i-1}")
                    markdown_content += f"{i}. [{section_title}](#{section_title.lower().replace(' ', '-')})\n"
                if citations:
                    markdown_content += f"{len(sections)+1}. [References](#references)\n"
                markdown_content += "\n"
            
            # Executive summary
            markdown_content += "## Executive Summary\n\n"
            markdown_content += f"{executive_summary}\n\n"
            
            # Sections
            for section in sections:
                section_title = section.get("title", "")
                section_content = section.get("content", "")
                markdown_content += f"## {section_title}\n\n"
                markdown_content += f"{section_content}\n\n"
            
            # References
            if citations:
                markdown_content += "## References\n\n"
                for citation in citations:
                    title = citation.get("title", "")
                    url = citation.get("url", "")
                    author = citation.get("author", "")
                    
                    markdown_content += f"- **{title}**"
                    if author:
                        markdown_content += f" - {author}"
                    if url:
                        markdown_content += f" [Link]({url})"
                    markdown_content += "\n"
            
            return {
                "format": "markdown",
                "content": markdown_content,
                "includes_toc": include_toc,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Markdown report generation failed: {e}")
            return {"error": str(e)}

class QualityAssessmentTool(Tool):
    """Tool for assessing report quality"""
    
    def __init__(self):
        super().__init__(
            name="assess_report_quality",
            description="Assess the quality and completeness of reports",
            parameters={
                "report_data": {
                    "type": "object",
                    "description": "Report data to assess"
                },
                "quality_criteria": {
                    "type": "array",
                    "description": "Quality criteria to assess",
                    "items": {"type": "string"},
                    "default": ["completeness", "accuracy", "clarity", "structure", "citations"]
                }
            }
        )
    
    async def run(self, report_data: Dict[str, Any], quality_criteria: List[str] = None) -> Dict[str, Any]:
        """Assess report quality"""
        try:
            if quality_criteria is None:
                quality_criteria = ["completeness", "accuracy", "clarity", "structure", "citations"]
            
            assessment = {
                "overall_score": 0.0,
                "criteria_scores": {},
                "strengths": [],
                "weaknesses": [],
                "recommendations": []
            }
            
            total_score = 0.0
            
            # Assess each criterion
            for criterion in quality_criteria:
                score = await self._assess_criterion(report_data, criterion)
                assessment["criteria_scores"][criterion] = score
                total_score += score
                
                # Generate feedback
                if score >= 0.8:
                    assessment["strengths"].append(f"Strong {criterion}")
                elif score < 0.6:
                    assessment["weaknesses"].append(f"Needs improvement in {criterion}")
            
            # Calculate overall score
            assessment["overall_score"] = total_score / len(quality_criteria) if quality_criteria else 0
            
            # Generate recommendations
            assessment["recommendations"] = await self._generate_quality_recommendations(assessment)
            
            return assessment
            
        except Exception as e:
            logger.error(f"Quality assessment failed: {e}")
            return {"error": str(e)}
    
    async def _assess_criterion(self, report_data: Dict[str, Any], criterion: str) -> float:
        """Assess a specific quality criterion"""
        try:
            if criterion == "completeness":
                return await self._assess_completeness(report_data)
            elif criterion == "accuracy":
                return await self._assess_accuracy(report_data)
            elif criterion == "clarity":
                return await self._assess_clarity(report_data)
            elif criterion == "structure":
                return await self._assess_structure(report_data)
            elif criterion == "citations":
                return await self._assess_citations(report_data)
            else:
                return 0.5  # Default score
                
        except Exception as e:
            logger.warning(f"Failed to assess {criterion}: {e}")
            return 0.5
    
    async def _assess_completeness(self, report_data: Dict[str, Any]) -> float:
        """Assess report completeness"""
        try:
            required_elements = ["title", "executive_summary", "sections"]
            present_elements = 0
            
            for element in required_elements:
                if report_data.get(element):
                    present_elements += 1
            
            # Check sections have content
            sections = report_data.get("sections", [])
            if sections:
                sections_with_content = sum(1 for section in sections if section.get("content"))
                section_score = sections_with_content / len(sections)
            else:
                section_score = 0
            
            base_score = present_elements / len(required_elements)
            return (base_score * 0.7) + (section_score * 0.3)
            
        except Exception as e:
            logger.warning(f"Completeness assessment failed: {e}")
            return 0.5
    
    async def _assess_accuracy(self, report_data: Dict[str, Any]) -> float:
        """Assess report accuracy (simplified)"""
        try:
            # Check for data consistency
            sections = report_data.get("sections", [])
            data_points = 0
            consistent_data = 0
            
            for section in sections:
                content = section.get("content", "")
                # Look for numerical data
                if any(char.isdigit() for char in content):
                    data_points += 1
                    consistent_data += 1  # Simplified - assume consistency
            
            if data_points == 0:
                return 0.5  # Neutral score for no data
            
            return consistent_data / data_points
            
        except Exception as e:
            logger.warning(f"Accuracy assessment failed: {e}")
            return 0.5
    
    async def _assess_clarity(self, report_data: Dict[str, Any]) -> float:
        """Assess report clarity"""
        try:
            total_content = ""
            sections = report_data.get("sections", [])
            
            for section in sections:
                total_content += section.get("content", "")
            
            if not total_content:
                return 0.0
            
            # Simple clarity metrics
            avg_sentence_length = len(total_content.split('.')) / len(total_content.split()) if total_content.split() else 0
            readability_score = max(0, 1 - (avg_sentence_length / 50))  # Penalize very long sentences
            
            return readability_score
            
        except Exception as e:
            logger.warning(f"Clarity assessment failed: {e}")
            return 0.5
    
    async def _assess_structure(self, report_data: Dict[str, Any]) -> float:
        """Assess report structure"""
        try:
            sections = report_data.get("sections", [])
            
            if not sections:
                return 0.0
            
            # Check for logical structure
            has_intro = any("intro" in section.get("title", "").lower() for section in sections)
            has_conclusion = any("conclusion" in section.get("title", "").lower() for section in sections)
            has_analysis = any("analysis" in section.get("title", "").lower() for section in sections)
            
            structure_score = 0
            if has_intro:
                structure_score += 0.3
            if has_analysis:
                structure_score += 0.4
            if has_conclusion:
                structure_score += 0.3
            
            return structure_score
            
        except Exception as e:
            logger.warning(f"Structure assessment failed: {e}")
            return 0.5
    
    async def _assess_citations(self, report_data: Dict[str, Any]) -> float:
        """Assess citations and references"""
        try:
            citations = report_data.get("citations", [])
            
            if not citations:
                return 0.0
            
            # Check citation quality
            valid_citations = 0
            for citation in citations:
                if citation.get("title") and citation.get("url"):
                    valid_citations += 1
            
            return valid_citations / len(citations)
            
        except Exception as e:
            logger.warning(f"Citation assessment failed: {e}")
            return 0.5
    
    async def _generate_quality_recommendations(self, assessment: Dict[str, Any]) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        try:
            criteria_scores = assessment.get("criteria_scores", {})
            
            for criterion, score in criteria_scores.items():
                if score < 0.6:
                    if criterion == "completeness":
                        recommendations.append("Add missing sections and ensure comprehensive coverage")
                    elif criterion == "accuracy":
                        recommendations.append("Verify data accuracy and add supporting evidence")
                    elif criterion == "clarity":
                        recommendations.append("Improve writing clarity and reduce technical jargon")
                    elif criterion == "structure":
                        recommendations.append("Improve report structure with clear introduction and conclusion")
                    elif criterion == "citations":
                        recommendations.append("Add proper citations and references for all data sources")
            
            if not recommendations:
                recommendations.append("Report quality is good - consider minor formatting improvements")
            
        except Exception as e:
            logger.warning(f"Failed to generate quality recommendations: {e}")
            recommendations.append("Manual review recommended for quality improvement")
        
        return recommendations

class DataVisualizationTool(Tool):
    """Tool for creating data visualizations"""
    
    def __init__(self):
        super().__init__(
            name="create_visualizations",
            description="Create charts and data visualizations",
            parameters={
                "data": {
                    "type": "object",
                    "description": "Data to visualize"
                },
                "chart_types": {
                    "type": "array",
                    "description": "Types of charts to create",
                    "items": {"type": "string", "enum": ["line", "bar", "pie", "scatter", "radar"]},
                    "default": ["line", "bar"]
                }
            }
        )
    
    async def run(self, data: Dict[str, Any], chart_types: List[str] = None) -> Dict[str, Any]:
        """Create data visualizations"""
        try:
            if chart_types is None:
                chart_types = ["line", "bar"]
            
            charts = []
            
            for chart_type in chart_types:
                chart = await self._create_chart(data, chart_type)
                if chart:
                    charts.append(chart)
            
            return {
                "charts": charts,
                "total_charts": len(charts),
                "chart_types": chart_types
            }
            
        except Exception as e:
            logger.error(f"Data visualization failed: {e}")
            return {"error": str(e)}
    
    async def _create_chart(self, data: Dict[str, Any], chart_type: str) -> Dict[str, Any]:
        """Create a specific type of chart"""
        try:
            # Extract chart data from provided data
            labels = data.get("labels", [])
            datasets = data.get("datasets", [])
            
            if not labels or not datasets:
                return None
            
            chart_config = {
                "type": chart_type,
                "data": {
                    "labels": labels,
                    "datasets": []
                },
                "options": {
                    "responsive": True,
                    "plugins": {
                        "title": {
                            "display": True,
                            "text": f"{chart_type.title()} Chart"
                        }
                    }
                }
            }
            
            # Process datasets
            for dataset in datasets:
                chart_dataset = {
                    "label": dataset.get("label", "Dataset"),
                    "data": dataset.get("data", []),
                    "backgroundColor": dataset.get("backgroundColor", "rgba(54, 162, 235, 0.2)"),
                    "borderColor": dataset.get("borderColor", "rgba(54, 162, 235, 1)"),
                    "borderWidth": dataset.get("borderWidth", 1)
                }
                
                if chart_type == "line":
                    chart_dataset["fill"] = dataset.get("fill", False)
                    chart_dataset["tension"] = dataset.get("tension", 0.1)
                
                chart_config["data"]["datasets"].append(chart_dataset)
            
            return chart_config
            
        except Exception as e:
            logger.warning(f"Failed to create {chart_type} chart: {e}")
            return None

class FinalAnswerAgent(BaseAgent):
    """Agent for generating final comprehensive reports using SmolAgents"""
    
    def __init__(self, model: OpenAIModel, memory: ConversationMemory = None):
        super().__init__(
            name="FinalAnswerAgent",
            model=model,
            memory=memory or ConversationMemory()
        )
        
        # Add report generation tools
        self.add_custom_tool(HTMLReportTool())
        self.add_custom_tool(MarkdownReportTool())
        self.add_custom_tool(QualityAssessmentTool())
        self.add_custom_tool(DataVisualizationTool())
    
    async def execute_task(self, task: Task) -> TaskResult:
        """Generate final answer/report using SmolAgents"""
        start_time = datetime.now()
        
        try:
            report_data = task.parameters.get("report_data")
            output_format = task.parameters.get("output_format", "html")
            requirements = task.parameters.get("requirements", [])
            
            if not report_data:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    error="Report data is required"
                )
            
            # Create task description for SmolAgents
            task_description = f"Generate comprehensive {output_format} report with data visualizations and quality assessment"
            
            # Use SmolAgents to orchestrate the report generation
            result = await self.run_task_with_smolagents(task_description)
            
            if result.get("success"):
                report_result = result.get("result", {})
                
                # Enhance with specific report generation
                enhanced_result = await self._enhance_report_result(report_result, task)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=enhanced_result,
                    execution_time=execution_time,
                    metadata={
                        "output_format": output_format,
                        "report_sections": len(report_data.get("sections", [])),
                        "requirements_met": len(requirements),
                        "method": "smolagents"
                    }
                )
            else:
                # Fallback to traditional method
                fallback_result = await self._execute_traditional_report_generation(task)
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
    
    async def _enhance_report_result(self, smolagents_result: Dict[str, Any], task: Task) -> Dict[str, Any]:
        """Enhance SmolAgents result with specific report generation"""
        try:
            output_format = task.parameters.get("output_format", "html")
            report_data = task.parameters.get("report_data")
            
            if output_format == "html":
                html_tool = HTMLReportTool()
                html_result = await html_tool.run(
                    report_data, 
                    template_style="professional",
                    include_charts=True,
                    include_citations=True
                )
                smolagents_result.update(html_result)
                
                # Generate charts
                if report_data.get("charts_data"):
                    viz_tool = DataVisualizationTool()
                    charts_result = await viz_tool.run(report_data["charts_data"])
                    smolagents_result["charts"] = charts_result.get("charts", [])
                
                # Quality assessment
                quality_tool = QualityAssessmentTool()
                quality_result = await quality_tool.run(report_data)
                smolagents_result["quality_assessment"] = quality_result
                
            elif output_format == "markdown":
                markdown_tool = MarkdownReportTool()
                markdown_result = await markdown_tool.run(report_data)
                smolagents_result.update(markdown_result)
            
            elif output_format == "json":
                smolagents_result.update(self._generate_json_report(report_data))
            
            # Add metadata
            smolagents_result["enhanced_at"] = datetime.now().isoformat()
            smolagents_result["enhanced_by"] = "FinalAnswerAgent"
            
            return smolagents_result
            
        except Exception as e:
            logger.error(f"Failed to enhance report result: {e}")
            return smolagents_result
    
    async def _execute_traditional_report_generation(self, task: Task) -> TaskResult:
        """Fallback traditional report generation"""
        try:
            report_data = task.parameters.get("report_data")
            output_format = task.parameters.get("output_format", "html")
            requirements = task.parameters.get("requirements", [])
            
            if output_format == "html":
                result = await self._generate_html_report(report_data, requirements)
            elif output_format == "markdown":
                result = await self._generate_markdown_report(report_data, requirements)
            elif output_format == "json":
                result = await self._generate_json_report(report_data)
            else:
                result = {"error": f"Unsupported output format: {output_format}"}
            
            return TaskResult(
                task_id=task.id,
                success="error" not in result,
                result=result if "error" not in result else None,
                error=result.get("error") if "error" in result else None,
                metadata={
                    "output_format": output_format,
                    "report_sections": len(report_data.get("sections", [])),
                    "requirements_met": len(requirements),
                    "method": "traditional"
                }
            )
            
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e)
            )
    
    async def _generate_html_report(self, report_data: Dict[str, Any], requirements: List[str]) -> Dict[str, Any]:
        """Generate HTML report"""
        try:
            html_tool = HTMLReportTool()
            return await html_tool.run(report_data)
        except Exception as e:
            return {"error": f"HTML report generation failed: {str(e)}"}
    
    async def _generate_markdown_report(self, report_data: Dict[str, Any], requirements: List[str]) -> Dict[str, Any]:
        """Generate Markdown report"""
        try:
            markdown_tool = MarkdownReportTool()
            return await markdown_tool.run(report_data)
        except Exception as e:
            return {"error": f"Markdown report generation failed: {str(e)}"}
    
    def _generate_json_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON report"""
        try:
            structured_report = {
                "metadata": {
                    "title": report_data.get("title", "Financial Research Report"),
                    "generated_at": datetime.now().isoformat(),
                    "version": "1.0"
                },
                "executive_summary": report_data.get("executive_summary", ""),
                "sections": report_data.get("sections", []),
                "data": report_data.get("data", {}),
                "charts": report_data.get("charts", []),
                "citations": report_data.get("citations", []),
                "conclusions": report_data.get("conclusions", ""),
                "recommendations": report_data.get("recommendations", [])
            }
            
            return {
                "format": "json",
                "content": structured_report,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"JSON report generation failed: {str(e)}"}
    
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        return [
            "report_generation",
            "html_generation",
            "markdown_generation",
            "data_visualization",
            "citation_formatting",
            "quality_assessment",
            "executive_summary",
            "smolagents_integration"
        ]
    
    async def generate_report_with_smolagents(self, report_data: Dict[str, Any], output_format: str = "html") -> Dict[str, Any]:
        """Generate report using SmolAgents framework directly"""
        try:
            # Create comprehensive report generation task
            task_description = f"""
            Generate a comprehensive {output_format} financial report with the following features:
            
            1. Professional formatting and styling
            2. Interactive data visualizations and charts
            3. Proper sections and subsections
            4. Citations and references
            5. Executive summary
            6. Data tables and analysis
            7. Conclusions and recommendations
            8. Quality assessment and review
            
            Output format: {output_format}
            Report data: {json.dumps(report_data, indent=2)}
            """
            
            result = await self.run_task_with_smolagents(task_description)
            
            if result.get("success"):
                return result.get("result", {})
            else:
                raise Exception(f"SmolAgents report generation failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"SmolAgents report generation failed: {e}")
            raise