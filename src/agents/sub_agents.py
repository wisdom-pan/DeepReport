"""
Sub-agents module for SmolAgents-based specialized agents
"""

from .deep_researcher_agent import DeepResearcherAgent
from .browser_agent import BrowserAgent
from .deep_analyze_agent import DeepAnalyzeAgent
from .final_answer_agent import FinalAnswerAgent

__all__ = [
    'DeepResearcherAgent',
    'BrowserAgent', 
    'DeepAnalyzeAgent',
    'FinalAnswerAgent'
]