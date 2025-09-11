"""
Report generation modules for DeepReport
"""

from .html_generator import HTMLReportGenerator
from .chart_generator import ChartGenerator
from .citation_manager import CitationManager

__all__ = [
    "HTMLReportGenerator",
    "ChartGenerator", 
    "CitationManager"
]