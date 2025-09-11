import os
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field

class Config(BaseSettings):
    """Configuration for DeepReport system"""
    
    # API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    serper_api_key: Optional[str] = Field(None, env="SERPER_API_KEY")
    metaso_api_key: Optional[str] = Field(None, env="METASO_API_KEY")
    sogou_api_key: Optional[str] = Field(None, env="SOGOU_API_KEY")
    
    # Model Configuration
    default_model: str = Field("gpt-4o", env="DEFAULT_MODEL")
    max_tokens: int = Field(4096, env="MAX_TOKENS")
    temperature: float = Field(0.7, env="TEMPERATURE")
    
    # Search Engine Configuration
    enabled_search_engines: list[str] = Field(["serper"], env="ENABLED_SEARCH_ENGINES")
    
    # Report Configuration
    output_dir: str = Field("./reports", env="OUTPUT_DIR")
    charts_enabled: bool = Field(True, env="CHARTS_ENABLED")
    data_sources_enabled: bool = Field(True, env="DATA_SOURCES_ENABLED")
    
    # MCP Configuration
    mcp_server_url: Optional[str] = Field(None, env="MCP_SERVER_URL")
    mcp_api_key: Optional[str] = Field(None, env="MCP_API_KEY")
    
    # Browser Configuration
    headless_browser: bool = Field(True, env="HEADLESS_BROWSER")
    browser_timeout: int = Field(30000, env="BROWSER_TIMEOUT")
    
    class Config:
        env_file = ".env"

# Global configuration instance
config = Config()

def get_model_config(model_name: str = None) -> Dict[str, Any]:
    """Get configuration for a specific model"""
    model_name = model_name or config.default_model
    
    base_config = {
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
    }
    
    if "gpt" in model_name.lower():
        return {
            **base_config,
            "model": model_name,
            "api_key": config.openai_api_key,
        }
    elif "claude" in model_name.lower():
        return {
            **base_config,
            "model": model_name,
            "api_key": config.anthropic_api_key,
        }
    else:
        return base_config