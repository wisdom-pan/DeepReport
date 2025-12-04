# 📊 DeepReport

DeepReport is an open-source AI-powered financial research and report generation system built on the SmolAgents framework.

## 📚 Documentation

For complete documentation, please visit our [docs directory](docs/):

- **[English Documentation](docs/en/README.md)**
- **[中文文档](docs/zh/README.md)**

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/DeepReport.git
cd DeepReport

# Quick start with Docker (recommended)
./start.sh

# Or manually start
docker-compose up -d

# Access the application
open http://localhost:7860
```

## 📁 Project Structure

```
DeepReport/
├── docs/                    # Documentation
│   ├── en/                 # English documentation
│   │   ├── README.md       # Main documentation
│   │   ├── CONTRIBUTING.md # Contributing guide
│   │   └── CODE_OF_CONDUCT.md # Code of conduct
│   ├── zh/                 # Chinese documentation
│   │   ├── README.md       # 主要文档
│   │   ├── CONTRIBUTING.md # 贡献指南
│   │   └── CODE_OF_CONDUCT.md # 行为准则
│   └── CHANGELOG.md        # Project changelog
├── src/                    # Source code
├── main.py                 # Main application
├── docker-compose.yml      # Docker compose configuration
├── Dockerfile             # Docker image configuration
├── requirements.txt        # Python dependencies
└── config.py              # Configuration management
```

## 🌟 Features

- **SmolAgents Framework**: Advanced multi-agent AI orchestration
- **Specialized Agents**: DeepResearcher, Browser, DeepAnalyze, FinalAnswer
- **Multi-Engine Search**: Serper, Metaso, Sogou integration
- **Rich Reports**: HTML reports with interactive charts and professional citations
- **Docker Support**: Complete containerization with one-click deployment
- **MCP Protocol**: FastMCP support for local/remote tool connections

## DEMO
[demo](https://modelscope.cn/studios/wisdom11111/DeepResearchReport)

## 🤝 Contributing

We welcome contributions! Please see our [contributing guide](docs/en/CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**DeepReport** - Empowering financial research with AI agents and comprehensive analysis tools.
