import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging
from smolagents import Tool
from smolagents.memory import ConversationMemory
from smolagents.models import OpenAIModel

from .base_agent import BaseAgent, Task, TaskResult

logger = logging.getLogger(__name__)

class PlanningTool(Tool):
    """Tool for creating research plans"""
    
    def __init__(self):
        super().__init__(
            name="create_research_plan",
            description="Create a comprehensive research plan for financial topics",
            parameters={
                "research_topic": {
                    "type": "string",
                    "description": "The financial research topic to plan"
                },
                "requirements": {
                    "type": "array",
                    "description": "List of specific requirements for the research",
                    "items": {"type": "string"}
                },
                "output_format": {
                    "type": "string",
                    "description": "Desired output format (html, markdown, json)",
                    "default": "html"
                }
            }
        )
    
    async def run(self, research_topic: str, requirements: List[str] = None, output_format: str = "html") -> Dict[str, Any]:
        """Create a research plan"""
        prompt = f"""
You are an expert financial research planner. Given a research topic, decompose it into executable sub-tasks that can be handled by specialized agents.

Research Topic: {research_topic}
Requirements: {', '.join(requirements) if requirements else 'None specified'}
Output Format: {output_format}

Your task is to create a comprehensive research plan with the following structure:

1. Overview: Brief description of the research approach
2. Tasks: List of specific sub-tasks with:
   - task_id: Unique identifier
   - task_type: One of ['deep_researcher', 'browser_use', 'deep_analyze', 'final_answer']
   - description: What the task should accomplish
   - parameters: Specific parameters needed
   - dependencies: List of task_ids this depends on
   - priority: 1-5 (5 being highest)
   - estimated_duration: Estimated time in minutes

3. Expected Output: What the final report should contain
4. Data Sources: Types of data needed
5. Citations Required: Types of citations to include

Format your response as a JSON object with the following structure:
{{
    "overview": "string",
    "tasks": [
        {{
            "task_id": "string",
            "task_type": "string",
            "description": "string",
            "parameters": {{"key": "value"}},
            "dependencies": [],
            "priority": 1,
            "estimated_duration": 30
        }}
    ],
    "expected_output": "string",
    "data_sources": ["string"],
    "citations_required": ["string"],
    "estimated_duration": 0
}}

Ensure the tasks are logically ordered and dependencies are correctly specified.
"""
        
        # This would be called by the SmolAgents framework
        return {"prompt": prompt, "parameters": {"research_topic": research_topic, "requirements": requirements, "output_format": output_format}}

class PlanningAgent(BaseAgent):
    """Planning agent that decomposes complex research tasks into sub-tasks using SmolAgents"""
    
    def __init__(self, model: OpenAIModel, memory: ConversationMemory = None):
        super().__init__(
            name="PlanningAgent",
            model=model,
            memory=memory or ConversationMemory()
        )
        
        # Add planning tools
        self.add_custom_tool(PlanningTool())
        
    async def execute_task(self, task: Task) -> TaskResult:
        """Execute a planning task to decompose research requirements"""
        start_time = datetime.now()
        
        try:
            research_topic = task.parameters.get("research_topic")
            requirements = task.parameters.get("requirements", [])
            output_format = task.parameters.get("output_format", "html")
            
            if not research_topic:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    error="Research topic is required"
                )
            
            # Use SmolAgents to create the research plan
            task_description = f"Create a comprehensive research plan for: {research_topic}"
            
            # Create a custom prompt for the planning task
            planning_prompt = self._create_planning_prompt(research_topic, requirements, output_format)
            
            # Use the model directly with the planning prompt
            response = await self.model.generate_response(planning_prompt)
            
            if not response.get("success"):
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    error=response.get("error", "Unknown error")
                )
            
            plan = self._parse_plan(response["content"])
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return TaskResult(
                task_id=task.id,
                success=True,
                result=plan,
                execution_time=execution_time,
                metadata={
                    "research_topic": research_topic,
                    "num_tasks": len(plan.get("tasks", [])),
                    "estimated_duration": plan.get("estimated_duration", 0),
                    "created_with": "smolagents"
                }
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def _create_planning_prompt(self, research_topic: str, requirements: List[str], output_format: str) -> str:
        """Create a prompt for planning the research"""
        return f"""
You are an expert financial research planner. Given a research topic, decompose it into executable sub-tasks that can be handled by specialized agents.

Research Topic: {research_topic}
Requirements: {', '.join(requirements) if requirements else 'None specified'}
Output Format: {output_format}

Your task is to create a comprehensive research plan with the following structure:

1. Overview: Brief description of the research approach
2. Tasks: List of specific sub-tasks with:
   - task_id: Unique identifier (e.g., "task_001", "task_002")
   - task_type: One of ['deep_researcher', 'browser_use', 'deep_analyze', 'final_answer']
   - description: What the task should accomplish
   - parameters: Specific parameters needed for the task
   - dependencies: List of task_ids this depends on
   - priority: 1-5 (5 being highest)
   - estimated_duration: Estimated time in minutes

3. Expected Output: What the final report should contain
4. Data Sources: Types of data needed
5. Citations Required: Types of citations to include

Format your response as a JSON object with the following structure:
{{
    "overview": "string",
    "tasks": [
        {{
            "task_id": "string",
            "task_type": "string",
            "description": "string",
            "parameters": {{"key": "value"}},
            "dependencies": [],
            "priority": 1,
            "estimated_duration": 30
        }}
    ],
    "expected_output": "string",
    "data_sources": ["string"],
    "citations_required": ["string"],
    "estimated_duration": 0
}}

Ensure the tasks are logically ordered and dependencies are correctly specified.
"""
    
    def _parse_plan(self, response_content: str) -> Dict[str, Any]:
        """Parse the model response into a structured plan"""
        try:
            plan = json.loads(response_content)
            
            # Validate required fields
            required_fields = ["overview", "tasks", "expected_output"]
            for field in required_fields:
                if field not in plan:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate tasks
            for task in plan["tasks"]:
                task_required_fields = ["task_id", "task_type", "description", "parameters"]
                for field in task_required_fields:
                    if field not in task:
                        raise ValueError(f"Task missing required field: {field}")
                
                # Set defaults for optional fields
                task.setdefault("dependencies", [])
                task.setdefault("priority", 1)
                task.setdefault("estimated_duration", 30)
            
            # Calculate total estimated duration
            total_duration = sum(task.get("estimated_duration", 0) for task in plan["tasks"])
            plan["estimated_duration"] = total_duration
            
            return plan
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing plan: {e}")
    
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        return [
            "research_planning",
            "task_decomposition",
            "workflow_orchestration",
            "dependency_resolution",
            "resource_estimation",
            "smolagents_integration"
        ]
    
    async def create_research_plan(self, research_topic: str, requirements: List[str] = None, output_format: str = "html") -> Dict[str, Any]:
        """Create a research plan for a given topic using SmolAgents"""
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            type="planning",
            description=f"Create research plan for: {research_topic}",
            parameters={
                "research_topic": research_topic,
                "requirements": requirements or [],
                "output_format": output_format
            }
        )
        
        result = await self.execute_task(task)
        if result.success:
            return result.result
        else:
            raise Exception(f"Failed to create research plan: {result.error}")
    
    async def create_research_plan_with_smolagents(self, research_topic: str, requirements: List[str] = None, output_format: str = "html") -> Dict[str, Any]:
        """Create a research plan using SmolAgents framework directly"""
        try:
            # Use SmolAgents to run the planning task
            task_description = f"Create a comprehensive research plan for: {research_topic}"
            
            # Add context about requirements
            if requirements:
                task_description += f"\nRequirements: {', '.join(requirements)}"
            if output_format:
                task_description += f"\nOutput Format: {output_format}"
            
            result = await self.run_task_with_smolagents(task_description)
            
            if result.get("success"):
                # Parse the result into a structured plan
                plan_content = result.get("result", "{}")
                return self._parse_plan(plan_content)
            else:
                raise Exception(f"SmolAgents planning failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"SmolAgents research plan creation failed: {e}")
            raise