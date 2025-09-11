# 📊 DeepReport
- [English](README.md) | [中文](README_CN.md)
DeepReport is an open-source AI-powered financial research and report generation system built on the SmolAgents framework. It utilizes specialized agents (DeepResearcher, Browser, DeepAnalyze, FinalAnswer) to create comprehensive financial reports with rich visualizations, professional citations, and data溯源.

## ✨ Features

### 🤖 SmolAgents-Powered AI System
- **SmolAgents Framework**: Advanced multi-agent AI orchestration with tool management
- **Planning Agent**: Task decomposition and workflow orchestration using SmolAgents
- **Specialized Sub-Agents**: Optimized agents for specific tasks:
  - **DeepResearcher Agent**: High-quality data source filtering and discovery
  - **Browser Agent**: Web navigation, PDF browsing, and interactive content extraction
  - **DeepAnalyze Agent**: Financial analysis, valuation, and insights generation
  - **FinalAnswer Agent**: HTML rendering, quality assessment, and report formatting

### 🔍 Multi-Engine Search
- **Serper**: Google search API integration
- **Metaso**: Advanced search capabilities
- **Sogou**: Chinese search engine support
- **Result Aggregation**: Automatic deduplication and relevance ranking

### 🔗 MCP Protocol Support
- **FastMCP Integration**: Local and remote MCP tool connections
- **Tool Registry**: Dynamic tool registration and discovery
- **Flexible Architecture**: Easy integration with external services

### 📈 Rich Report Generation
- **Interactive HTML Reports**: Professional, web-based reports with embedded charts
- **Multiple Chart Types**: Line, bar, pie, radar, scatter, and financial charts
- **Citation Management**: APA, MLA, Chicago, Harvard citation styles
- **Data Visualization**: Chart.js integration for dynamic, interactive charts

### 🌐 User Interface
- **Gradio Frontend**: Easy-to-use web interface
- **Real-time Status**: Live feedback on report generation progress
- **Export Options**: HTML and JSON output formats

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required API keys (see Configuration section)
- Chrome/Chromium browser (for web automation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/DeepReport.git
   cd DeepReport
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

The application will start at `http://localhost:7860`

## 🚀 Quick Start Commands

### Using Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-username/DeepReport.git
cd DeepReport

# Quick start with Docker
./start.sh

# Or manually start with Docker Compose
docker-compose up -d
```

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/your-username/DeepReport.git
cd DeepReport

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run the application
python main.py
```

## 🐳 Docker Deployment

### 🚀 One-Command Quick Start

The simplest way to start DeepReport:

```bash
# Clone and start
git clone https://github.com/your-username/DeepReport.git
cd DeepReport
./start.sh
```

This will:
- Check Docker is running
- Create .env file if needed
- Build and start all services
- Provide access URL

### Quick Start Scripts

```bash
# Start the application
./start.sh

# Stop the application
./stop.sh

# Full deployment with all options
./docker-deploy.sh deploy

# Check status
./docker-deploy.sh status

# View logs
./docker-deploy.sh logs
```

### Standard Docker Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/DeepReport.git
   cd DeepReport
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   Open `http://localhost:7860` in your browser

### Manual Docker Build

1. **Build the Docker image**
   ```bash
   docker build -t deepreport:latest .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     --name deepreport-app \
     -p 7860:7860 \
     -v $(pwd)/reports:/app/reports \
     -v $(pwd)/logs:/app/logs \
     --env-file .env \
     deepreport:latest
   ```

### Docker Configuration Options

#### Environment Variables
Create a `.env` file for Docker configuration:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Search Engine APIs
SERPER_API_KEY=your_serper_api_key_here
METASO_API_KEY=your_metaso_api_key_here
SOGOU_API_KEY=your_sogou_api_key_here

# Model Configuration
DEFAULT_MODEL=gpt-4o
MAX_TOKENS=4096
TEMPERATURE=0.7

# Report Configuration
OUTPUT_DIR=./reports
CHARTS_ENABLED=true
DATA_SOURCES_ENABLED=true

# MCP Configuration
MCP_SERVER_URL=your_mcp_server_url
MCP_API_KEY=your_mcp_api_key

# Browser Configuration
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30000

# Gradio Configuration
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=false
GRADIO_DEBUG=false
```

#### Docker Compose Services
- **deepreport**: Main application service
- **redis**: Optional Redis caching (uncomment in docker-compose.yml)
- **nginx**: Optional Nginx reverse proxy (uncomment in docker-compose.yml)

### Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f deepreport

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# Access container shell
docker exec -it deepreport-app bash

# Check container status
docker-compose ps

# Start specific service only
docker-compose up deepreport

# Stop specific service
docker-compose stop deepreport

# Restart service
docker-compose restart deepreport

# Remove containers and volumes (cleanup)
docker-compose down -v
```

### Quick Docker Commands

#### Using the deployment script
```bash
# Full deployment (recommended)
./docker-deploy.sh deploy

# Quick start
./docker-deploy.sh start

# View logs
./docker-deploy.sh logs

# Check status
./docker-deploy.sh status

# Stop services
./docker-deploy.sh stop
```

#### Manual Docker commands
```bash
# Build image manually
docker build -t deepreport:latest .

# Run container manually
docker run -d \
  --name deepreport-app \
  -p 7860:7860 \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  deepreport:latest

# Run with resource limits
docker run -d \
  --name deepreport-app \
  -p 7860:7860 \
  --memory=4g \
  --cpus=2 \
  -v $(pwd)/reports:/app/reports \
  --env-file .env \
  deepreport:latest

# Run with custom environment variables
docker run -d \
  --name deepreport-app \
  -p 7860:7860 \
  -e OPENAI_API_KEY=your_key \
  -e SERPER_API_KEY=your_key \
  -e DEFAULT_MODEL=gpt-4o \
  deepreport:latest
```

### Production Deployment

#### With Nginx Reverse Proxy
1. Uncomment the nginx service in `docker-compose.yml`
2. Create `nginx.conf` file
3. Add SSL certificates to `./ssl/` directory
4. Start the stack:

```bash
docker-compose up -d
```

#### Security Considerations
- Use strong API keys and rotate them regularly
- Enable HTTPS in production
- Use Docker secrets for sensitive data
- Limit container permissions
- Monitor container logs
- Regularly update base images

#### Resource Management
```bash
# Limit container resources
docker run -d \
  --name deepreport-app \
  --memory=4g \
  --cpus=2 \
  -p 7860:7860 \
  deepreport:latest
```

#### Health Checks
The Docker image includes built-in health checks:
- Checks application availability every 30 seconds
- Restarts container if unhealthy
- Provides status monitoring

### Troubleshooting

#### Common Issues
1. **Chrome installation errors**: Ensure all system dependencies are installed
2. **Permission issues**: Check volume mount permissions
3. **API key errors**: Verify environment variables in `.env`
4. **Port conflicts**: Ensure port 7860 is available

#### Debug Commands
```bash
# Check container logs
docker logs deepreport-app

# Check container health
docker inspect deepreport-app --format='{{.State.Health.Status}}'

# Access container for debugging
docker exec -it deepreport-app bash

# Test application inside container
docker exec deepreport-app curl http://localhost:7860/
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Search Engine APIs
SERPER_API_KEY=your_serper_api_key_here
METASO_API_KEY=your_metaso_api_key_here
SOGOU_API_KEY=your_sogou_api_key_here

# Model Configuration
DEFAULT_MODEL=gpt-4o
MAX_TOKENS=4096
TEMPERATURE=0.7

# Report Configuration
OUTPUT_DIR=./reports
CHARTS_ENABLED=true
DATA_SOURCES_ENABLED=true

# MCP Configuration
MCP_SERVER_URL=your_mcp_server_url
MCP_API_KEY=your_mcp_api_key

# Browser Configuration
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30000
```

### API Key Setup

#### OpenAI
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an API key
3. Add it to your `.env` file

#### Serper (Google Search)
1. Go to [Serper.dev](https://serper.dev/)
2. Sign up and get an API key
3. Add it to your `.env` file

#### Anthropic
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Add it to your `.env` file

#### Metaso
1. Contact Metaso for API access
2. Add the API key to your `.env` file

#### Sogou
1. Apply for Sogou API access
2. Add the API key to your `.env` file

## 📚 Usage Guide

### Basic Usage

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Open the web interface**
   Navigate to `http://localhost:7860`

3. **Generate a report**
   - Enter your research topic
   - Specify requirements (one per line)
   - Choose output format (HTML recommended)
   - Select AI model
   - Click "Generate Report"

### Example Research Topics

```
Tesla Inc. (TSLA) Q4 2023 Financial Performance Analysis
Cryptocurrency Market Trends and Investment Opportunities
Renewable Energy Sector Growth Prospects 2024
Federal Reserve Monetary Policy Impact on Tech Stocks
Artificial Intelligence in Financial Services Market Analysis
```

### Advanced Usage

#### Custom MCP Tools

You can register custom tools with the MCP manager:

```python
from src.utils.mcp_manager import MCPManager

async def custom_analysis_tool(data: str) -> Dict[str, Any]:
    # Your custom analysis logic
    return {"result": f"Analyzed: {data}"}

# Register the tool
await mcp_manager.register_local_tool(
    tool_name="custom_analysis",
    tool_func=custom_analysis_tool,
    description="Perform custom data analysis",
    parameters={"data": {"type": "string", "description": "Data to analyze"}}
)
```

#### Custom Chart Types

Extend the chart generator for specialized financial charts:

```python
from src.report.chart_generator import ChartGenerator

class CustomChartGenerator(ChartGenerator):
    async def generate_custom_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Custom chart generation logic
        return chart_config
```

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gradio UI     │    │   Planning      │    │   SmolAgents    │
│   Interface     │◄──►│   Agent         │◄──►│   Framework     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              ▲                         ▲
                              │                         │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Search        │    │   MCP           │    │   Specialized   │
│   Engines       │    │   Manager       │◄───┤   Agents        │
│   (Serper,      │    │                 │    │   (DeepResearcher│
│    Metaso,      │    └─────────────────┘    │    Browser,      │
│    Sogou)       │                           │    DeepAnalyze,   │
└─────────────────┘                           │    FinalAnswer)   │
         ▲                                    └─────────────────┘
         │                                              ▲
┌─────────────────┐                                │
│   Report        │                                │
│   Generator     │────────────────────────────────┘
│   (HTML,        │
│    Charts,      │
│    Citations)   │
└─────────────────┘
```

### Key Components

#### SmolAgents-Based Architecture
- **BaseAgent**: Abstract base class inheriting from SmolAgents Agent
- **PlanningAgent**: Task decomposition using SmolAgents with custom PlanningTool
- **DeepResearcherAgent**: Source filtering with SourceDiscoveryTool, ContentExtractionTool, QualityAssessmentTool
- **BrowserAgent**: Web automation with WebNavigationTool, PDFAnalysisTool, FormInteractionTool
- **DeepAnalyzeAgent**: Financial analysis with FinancialMetricsTool, SentimentAnalysisTool, ValuationTool
- **FinalAnswerAgent**: Report generation with HTMLReportTool, QualityAssessmentTool, DataVisualizationTool

#### Key SmolAgents Features
- **Tool Management**: Dynamic tool registration and execution
- **Memory Management**: ConversationMemory for context preservation
- **Model Integration**: Support for OpenAI, Anthropic, and other models
- **Async Execution**: Non-blocking agent coordination
- **Error Handling**: Robust error recovery and logging

#### Search Integration
- **SearchManager**: Coordinates multiple search engines
- **SerperEngine**: Google search API wrapper
- **MetasoEngine**: Metaso search API wrapper
- **SogouEngine**: Sogou search API wrapper

#### Report Generation
- **HTMLReportGenerator**: Creates professional HTML reports
- **ChartGenerator**: Generates various chart types using Chart.js
- **CitationManager**: Manages citations in multiple styles

#### MCP Integration
- **MCPManager**: Handles MCP protocol communications
- **Tool Registry**: Dynamic tool registration and discovery
- **Connection Management**: Local and remote server connections

## 🔧 Development

### Project Structure

```
DeepReport/
├── src/
│   ├── agents/                 # AI agents
│   │   ├── base_agent.py      # Base agent class
│   │   ├── planning_agent.py  # Planning agent
│   │   └── sub_agents.py      # Specialized sub-agents
│   ├── search/                # Search engine integration
│   │   ├── search_manager.py  # Search coordination
│   │   └── engines.py         # Search engine implementations
│   ├── report/                # Report generation
│   │   ├── html_generator.py  # HTML report generator
│   │   ├── chart_generator.py # Chart generation
│   │   └── citation_manager.py # Citation management
│   └── utils/                 # Utilities
│       ├── model_adapter.py   # AI model adapter
│       └── mcp_manager.py     # MCP protocol manager
├── templates/                 # HTML templates
├── static/                    # Static assets
├── tests/                     # Test files
├── docs/                      # Documentation
├── main.py                    # Main application
├── config.py                  # Configuration management
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_agents.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests**
5. **Ensure all tests pass**
6. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
7. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
8. **Open a Pull Request**


## 📋 Roadmap

### Version 1.0 (Current)
- ✅ SmolAgents framework integration
- ✅ Specialized agents: DeepResearcher, Browser, DeepAnalyze, FinalAnswer
- ✅ Multi-engine search coordination
- ✅ HTML report generation with rich visualizations
- ✅ Gradio web interface
- ✅ MCP protocol support with FastMCP
- ✅ Comprehensive tool systems for each agent
- ✅ Professional citation management

### Version 1.1 (Planned)
- 🔄 Enhanced financial chart types and real-time updates
- 🔄 Real-time market data integration
- 🔄 Advanced PDF export and report formatting
- 🔄 Machine learning-based predictive analytics
- 🔄 Multi-agent collaboration optimization



## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SmolAgents** for the advanced multi-agent AI framework
- OpenAI for GPT models
- Anthropic for Claude models
- Gradio for the web interface framework
- Chart.js for data visualization
- FastMCP for protocol implementation
- Browser-use for web automation
- All contributors and community members

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-username/DeepReport/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/DeepReport/discussions)
- **Email**: wisdompan1@outlook.com

## 🌟 Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**DeepReport** - Empowering financial research with AI agents and comprehensive analysis tools.

---

- [English](README.md) | [中文](README_CN.md)
- [Contribution Guidelines(English)](CONTRIBUTING.md) | [贡献指南(中文)](CONTRIBUTING_CN.md)