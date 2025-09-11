import os
from typing import Dict, Any, Optional
import json
import logging

from openai import OpenAI
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class ModelAdapter:
    """Adapter for different AI models (OpenAI, Anthropic, etc.)"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get("model", "gpt-4o")
        self.api_key = config.get("api_key")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 0.7)
        
        # Initialize clients
        self.openai_client = None
        self.anthropic_client = None
        
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize API clients based on model type"""
        if "gpt" in self.model_name.lower():
            if not self.api_key:
                raise ValueError("OpenAI API key is required for GPT models")
            self.openai_client = OpenAI(api_key=self.api_key)
            
        elif "claude" in self.model_name.lower():
            if not self.api_key:
                raise ValueError("Anthropic API key is required for Claude models")
            self.anthropic_client = Anthropic(api_key=self.api_key)
    
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate a response from the configured model"""
        try:
            if "gpt" in self.model_name.lower():
                return await self._generate_openai_response(prompt, system_prompt)
            elif "claude" in self.model_name.lower():
                return await self._generate_anthropic_response(prompt, system_prompt)
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
                
        except Exception as e:
            logger.error(f"Error generating response with {self.model_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _generate_openai_response(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate response using OpenAI API"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": self.model_name,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"OpenAI API error: {str(e)}"
            }
    
    async def _generate_anthropic_response(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate response using Anthropic API"""
        try:
            system_message = system_prompt or "You are a helpful assistant."
            
            response = self.anthropic_client.messages.create(
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_message,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                "success": True,
                "content": response.content[0].text,
                "model": self.model_name,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Anthropic API error: {str(e)}"
            }
    
    async def generate_structured_response(self, prompt: str, response_format: Dict[str, Any], system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate a structured response with specific format"""
        format_instruction = f"""
        Please respond with a JSON object that follows this structure:
        {json.dumps(response_format, indent=2)}
        
        Ensure your response is valid JSON and includes all required fields.
        """
        
        full_prompt = f"{prompt}\n\n{format_instruction}"
        
        response = await self.generate_response(full_prompt, system_prompt)
        
        if not response["success"]:
            return response
        
        try:
            # Try to parse the response as JSON
            content = response["content"]
            
            # Find JSON content in the response (might be wrapped in markdown code blocks)
            if "```json" in content:
                start = content.find("```json") + 7
                end = content.find("```", start)
                content = content[start:end].strip()
            elif "```" in content:
                start = content.find("```") + 3
                end = content.find("```", start)
                content = content[start:end].strip()
            
            parsed_content = json.loads(content)
            
            return {
                "success": True,
                "content": parsed_content,
                "model": self.model_name,
                "usage": response.get("usage", {})
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse JSON response: {str(e)}"
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model_name": self.model_name,
            "provider": "OpenAI" if "gpt" in self.model_name.lower() else "Anthropic",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "supports_structured_output": True
        }