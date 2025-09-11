import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import aiohttp
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

class MCPManager:
    """Manager for MCP (Model Context Protocol) connections"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.mcp_client = None
        self.connected_servers = {}
        self.local_tools = {}
        self.remote_tools = {}
        
        # Initialize FastMCP client
        self._initialize_mcp_client()
    
    def _initialize_mcp_client(self):
        """Initialize FastMCP client"""
        try:
            self.mcp_client = FastMCP()
            logger.info("FastMCP client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize FastMCP client: {e}")
            raise
    
    async def connect_to_server(self, server_url: str, api_key: str = None) -> bool:
        """Connect to a remote MCP server"""
        try:
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            # Test connection
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(f"{server_url}/health", timeout=10) as response:
                    if response.status == 200:
                        # Get available tools
                        async with session.get(f"{server_url}/tools", timeout=10) as tools_response:
                            if tools_response.status == 200:
                                tools_data = await tools_response.json()
                                self.connected_servers[server_url] = {
                                    "url": server_url,
                                    "api_key": api_key,
                                    "tools": tools_data.get("tools", []),
                                    "connected_at": datetime.now().isoformat(),
                                    "status": "connected"
                                }
                                
                                # Update remote tools cache
                                await self._update_remote_tools_cache(server_url, tools_data.get("tools", []))
                                
                                logger.info(f"Connected to MCP server: {server_url}")
                                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to connect to MCP server {server_url}: {e}")
            return False
    
    async def disconnect_from_server(self, server_url: str) -> bool:
        """Disconnect from a remote MCP server"""
        try:
            if server_url in self.connected_servers:
                del self.connected_servers[server_url]
                
                # Remove tools from cache
                self.remote_tools = {
                    k: v for k, v in self.remote_tools.items() 
                    if v.get("server_url") != server_url
                }
                
                logger.info(f"Disconnected from MCP server: {server_url}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to disconnect from MCP server {server_url}: {e}")
            return False
    
    async def register_local_tool(self, tool_name: str, tool_func: Callable, 
                                 description: str, parameters: Dict[str, Any]) -> bool:
        """Register a local tool with MCP"""
        try:
            # Register with FastMCP
            self.mcp_client.add_tool(tool_func, name=tool_name, description=description)
            
            # Store in local tools registry
            self.local_tools[tool_name] = {
                "name": tool_name,
                "description": description,
                "parameters": parameters,
                "function": tool_func,
                "registered_at": datetime.now().isoformat()
            }
            
            logger.info(f"Registered local tool: {tool_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register local tool {tool_name}: {e}")
            return False
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool (local or remote)"""
        try:
            # Check local tools first
            if tool_name in self.local_tools:
                return await self._call_local_tool(tool_name, parameters)
            
            # Check remote tools
            if tool_name in self.remote_tools:
                return await self._call_remote_tool(tool_name, parameters)
            
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
            
        except Exception as e:
            logger.error(f"Failed to call tool {tool_name}: {e}")
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            }
    
    async def _call_local_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a local tool"""
        try:
            tool_info = self.local_tools[tool_name]
            tool_func = tool_info["function"]
            
            # Execute the tool function
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(**parameters)
            else:
                result = tool_func(**parameters)
            
            return {
                "success": True,
                "result": result,
                "tool_name": tool_name,
                "tool_type": "local",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Local tool execution failed: {str(e)}",
                "tool_name": tool_name,
                "tool_type": "local"
            }
    
    async def _call_remote_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a remote tool"""
        try:
            tool_info = self.remote_tools[tool_name]
            server_url = tool_info["server_url"]
            api_key = self.connected_servers.get(server_url, {}).get("api_key")
            
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(
                    f"{server_url}/tools/{tool_name}/invoke",
                    json=parameters,
                    timeout=30
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "result": result,
                            "tool_name": tool_name,
                            "tool_type": "remote",
                            "server_url": server_url,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"Remote tool call failed: {error_text}",
                            "tool_name": tool_name,
                            "tool_type": "remote",
                            "server_url": server_url
                        }
                        
        except Exception as e:
            return {
                "success": False,
                "error": f"Remote tool execution failed: {str(e)}",
                "tool_name": tool_name,
                "tool_type": "remote"
            }
    
    async def _update_remote_tools_cache(self, server_url: str, tools: List[Dict[str, Any]]):
        """Update the remote tools cache"""
        for tool in tools:
            tool_name = tool.get("name")
            if tool_name:
                self.remote_tools[tool_name] = {
                    "name": tool_name,
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {}),
                    "server_url": server_url,
                    "cached_at": datetime.now().isoformat()
                }
    
    def get_available_tools(self) -> Dict[str, Any]:
        """Get all available tools (local and remote)"""
        return {
            "local_tools": {name: {
                "name": info["name"],
                "description": info["description"],
                "parameters": info["parameters"],
                "registered_at": info["registered_at"]
            } for name, info in self.local_tools.items()},
            "remote_tools": {name: {
                "name": info["name"],
                "description": info["description"],
                "parameters": info["parameters"],
                "server_url": info["server_url"],
                "cached_at": info["cached_at"]
            } for name, info in self.remote_tools.items()}
        }
    
    def get_connected_servers(self) -> Dict[str, Any]:
        """Get information about connected MCP servers"""
        return {
            server_url: {
                "url": info["url"],
                "tools_count": len(info["tools"]),
                "connected_at": info["connected_at"],
                "status": info["status"]
            }
            for server_url, info in self.connected_servers.items()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all connections"""
        health_status = {
            "mcp_client": {"status": "healthy", "message": "FastMCP client running"},
            "connected_servers": {},
            "local_tools_count": len(self.local_tools),
            "remote_tools_count": len(self.remote_tools)
        }
        
        # Check connected servers
        for server_url, server_info in self.connected_servers.items():
            try:
                headers = {}
                if server_info.get("api_key"):
                    headers["Authorization"] = f"Bearer {server_info['api_key']}"
                
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get(f"{server_url}/health", timeout=5) as response:
                        if response.status == 200:
                            health_status["connected_servers"][server_url] = {
                                "status": "healthy",
                                "message": "Server responding"
                            }
                        else:
                            health_status["connected_servers"][server_url] = {
                                "status": "unhealthy",
                                "message": f"Server returned status {response.status}"
                            }
                            
            except Exception as e:
                health_status["connected_servers"][server_url] = {
                    "status": "unhealthy",
                    "message": f"Connection error: {str(e)}"
                }
        
        return health_status


# Example local tools that can be registered
async def financial_data_fetcher(symbol: str, period: str = "1y") -> Dict[str, Any]:
    """Example local tool for fetching financial data"""
    try:
        # This is a placeholder - you would implement actual financial data fetching
        return {
            "symbol": symbol,
            "period": period,
            "data": {
                "price": 100.0,
                "change": 2.5,
                "change_percent": 2.56,
                "volume": 1000000
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


async def news_sentiment_analyzer(text: str) -> Dict[str, Any]:
    """Example local tool for sentiment analysis"""
    try:
        # This is a placeholder - you would implement actual sentiment analysis
        return {
            "text": text,
            "sentiment": "positive",
            "confidence": 0.85,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


async def market_data_aggregator(symbols: List[str]) -> Dict[str, Any]:
    """Example local tool for market data aggregation"""
    try:
        # This is a placeholder - you would implement actual data aggregation
        return {
            "symbols": symbols,
            "aggregated_data": {
                "total_volume": 5000000,
                "average_price": 150.0,
                "top_performer": symbols[0] if symbols else None
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}