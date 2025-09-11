#!/usr/bin/env python3
"""
Example of MCP (Model Context Protocol) integration with DeepReport
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.utils.mcp_manager import MCPManager, financial_data_fetcher, news_sentiment_analyzer, market_data_aggregator

async def demonstrate_mcp_integration():
    """Demonstrate MCP tool integration"""
    
    print("🔗 Demonstrating MCP Integration...")
    
    # Initialize MCP manager
    mcp_manager = MCPManager({
        "mcp_server_url": "https://api.example.com/mcp",
        "mcp_api_key": "your_api_key_here"  # Replace with actual key
    })
    
    try:
        # Register local tools
        print("📝 Registering local tools...")
        
        await mcp_manager.register_local_tool(
            tool_name="financial_data_fetcher",
            tool_func=financial_data_fetcher,
            description="Fetch financial data for a given symbol",
            parameters={
                "symbol": {"type": "string", "description": "Stock symbol"},
                "period": {"type": "string", "description": "Time period (1y, 6m, etc.)"}
            }
        )
        
        await mcp_manager.register_local_tool(
            tool_name="news_sentiment_analyzer",
            tool_func=news_sentiment_analyzer,
            description="Analyze sentiment of news text",
            parameters={
                "text": {"type": "string", "description": "News text to analyze"}
            }
        )
        
        await mcp_manager.register_local_tool(
            tool_name="market_data_aggregator",
            tool_func=market_data_aggregator,
            description="Aggregate market data for multiple symbols",
            parameters={
                "symbols": {"type": "array", "description": "List of stock symbols"}
            }
        )
        
        print("✅ Local tools registered successfully!")
        
        # Connect to remote MCP server (if available)
        print("🌐 Connecting to remote MCP server...")
        server_url = "https://api.example.com/mcp"  # Replace with actual server
        connected = await mcp_manager.connect_to_server(server_url)
        
        if connected:
            print("✅ Connected to remote MCP server!")
        else:
            print("⚠️ Remote MCP server not available (this is expected in demo mode)")
        
        # Demonstrate tool usage
        print("\n🛠️ Demonstrating tool usage...")
        
        # Use financial data fetcher
        print("\n📈 Fetching financial data...")
        financial_result = await mcp_manager.call_tool(
            "financial_data_fetcher",
            {"symbol": "TSLA", "period": "1y"}
        )
        
        if financial_result["success"]:
            print("✅ Financial data fetched successfully!")
            print(f"Data: {financial_result['result']}")
        else:
            print(f"❌ Failed to fetch financial data: {financial_result['error']}")
        
        # Use sentiment analyzer
        print("\n📰 Analyzing news sentiment...")
        news_text = "Tesla reports record Q4 deliveries, stock price surges 8% in pre-market trading"
        sentiment_result = await mcp_manager.call_tool(
            "news_sentiment_analyzer",
            {"text": news_text}
        )
        
        if sentiment_result["success"]:
            print("✅ Sentiment analysis completed!")
            print(f"Sentiment: {sentiment_result['result']}")
        else:
            print(f"❌ Sentiment analysis failed: {sentiment_result['error']}")
        
        # Use market data aggregator
        print("\n📊 Aggregating market data...")
        market_result = await mcp_manager.call_tool(
            "market_data_aggregator",
            {"symbols": ["TSLA", "AAPL", "GOOGL"]}
        )
        
        if market_result["success"]:
            print("✅ Market data aggregated successfully!")
            print(f"Aggregated data: {market_result['result']}")
        else:
            print(f"❌ Market data aggregation failed: {market_result['error']}")
        
        # Show available tools
        print("\n🔍 Available tools:")
        available_tools = mcp_manager.get_available_tools()
        
        print("Local Tools:")
        for tool_name, tool_info in available_tools["local_tools"].items():
            print(f"  - {tool_name}: {tool_info['description']}")
        
        print("Remote Tools:")
        for tool_name, tool_info in available_tools["remote_tools"].items():
            print(f"  - {tool_name}: {tool_info['description']}")
        
        # Health check
        print("\n🏥 Performing health check...")
        health_status = await mcp_manager.health_check()
        
        print("MCP Client Status:", health_status["mcp_client"]["status"])
        print("Local Tools Count:", health_status["local_tools_count"])
        print("Remote Tools Count:", health_status["remote_tools_count"])
        
        for server_url, server_status in health_status["connected_servers"].items():
            print(f"Server {server_url}: {server_status['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DeepReport MCP Integration Example")
    print("=" * 50)
    
    success = asyncio.run(demonstrate_mcp_integration())
    
    if success:
        print("\n🎉 MCP integration example completed successfully!")
    else:
        print("\n💥 MCP integration example failed.")
        sys.exit(1)