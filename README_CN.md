# 📊 DeepReport
- [English](README.md) | [中文](README_CN.md)

DeepReport是一个开源的AI驱动金融研究和报告生成系统，使用规划智能体和子智能体协作来创建具有丰富可视化、专业引用和数据溯源的综合金融报告。

## ✨ 功能特性

### 🤖 多智能体协作系统
- **规划智能体 (Planning Agent)**：将复杂研究任务分解为可执行的子任务
- **子智能体 (Sub-Agents)**：专门处理不同任务的智能体：
  - **深度研究智能体 (DeepResearcher Agent)**：筛选高质量数据源
  - **浏览器智能体 (Browser Agent)**：网页交互、PDF文件浏览等细粒度交互
  - **深度分析智能体 (DeepAnalyze Agent)**：深度分析数据、挖掘财报、专业估值分析
  - **最终报告智能体 (Final Answer Agent)**：HTML渲染、质量评估、格式转换

### 🔍 多引擎搜索
- **Serper**：Google搜索API集成
- **Metaso**：高级搜索功能
- **搜狗**：中文搜索引擎支持
- **结果聚合**：自动去重和相关性排序

### 🔗 MCP协议支持
- **FastMCP集成**：本地和远程MCP工具连接
- **工具注册**：动态工具注册和发现
- **灵活架构**：易于集成外部服务

### 📈 丰富报告生成
- **交互式HTML报告**：具有嵌入图表的专业Web报告
- **多种图表类型**：折线图、柱状图、饼图、雷达图、散点图、财务图表
- **引用管理**：APA、MLA、芝加哥、哈佛引用格式
- **数据可视化**：Chart.js集成，支持动态交互图表

### 🌐 用户界面
- **Gradio前端**：易用的Web界面
- **实时状态**：报告生成进度的实时反馈
- **导出选项**：HTML和JSON输出格式

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 必需的API密钥（参见配置部分）
- Chrome/Chromium浏览器（用于Web自动化）


## 🚀 快速启动命令

### 使用Docker（推荐）
```bash
# 克隆仓库
git clone https://github.com/your-username/DeepReport.git
cd DeepReport

# Docker快速启动
./start.sh

# 或使用Docker Compose手动启动
docker-compose up -d
```

### 手动安装
```bash
# 克隆仓库
git clone https://github.com/your-username/DeepReport.git
cd DeepReport

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp .env.example .env
# 编辑.env文件，添加您的API密钥和配置

# 运行应用
python main.py
```

## ⚙️ 配置说明

### 环境变量

基于 `.env.example` 创建 `.env` 文件：

```env
# OpenAI配置
OPENAI_API_KEY=您的openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic配置
ANTHROPIC_API_KEY=您的anthropic_api_key

# 搜索引擎API
SERPER_API_KEY=您的serper_api_key
METASO_API_KEY=您的metaso_api_key
SOGOU_API_KEY=您的sogou_api_key

# 模型配置
DEFAULT_MODEL=gpt-4o
MAX_TOKENS=4096
TEMPERATURE=0.7

# 报告配置
OUTPUT_DIR=./reports
CHARTS_ENABLED=true
DATA_SOURCES_ENABLED=true

# MCP配置
MCP_SERVER_URL=您的mcp服务器地址
MCP_API_KEY=您的mcp_api_key

# 浏览器配置
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30000
```

### API密钥设置

#### OpenAI
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 创建API密钥
3. 添加到您的 `.env` 文件

#### Serper (Google搜索)
1. 访问 [Serper.dev](https://serper.dev/)
2. 注册并获取API密钥
3. 添加到您的 `.env` 文件

#### Anthropic
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 创建API密钥
3. 添加到您的 `.env` 文件

#### Metaso
1. 联系Metaso获取API访问权限
2. 将API密钥添加到您的 `.env` 文件

#### 搜狗
1. 申请搜狗API访问权限
2. 将API密钥添加到您的 `.env` 文件

## 📚 使用指南

### 基础使用

1. **启动应用**
启动命令：

  * 最简单的方式
  ./start.sh

  # 使用docker-compose
  docker-compose up -d

2. **打开Web界面**
   导航到 `http://localhost:7860`

3. **生成报告**
   - 输入您的研究主题
   - 指定要求（每行一个）
   - 选择输出格式（推荐HTML）
   - 选择AI模型
   - 点击"生成报告"

### 示例研究主题

```
特斯拉(TSLA) 2023年第四季度财务业绩分析
加密货币市场趋势和投资机会
可再生能源行业2024年前景展望
美联储货币政策对科技股的影响
金融服务中人工智能市场分析
```

### 高级使用

#### 自定义MCP工具

您可以向MCP管理器注册自定义工具：

```python
from src.utils.mcp_manager import MCPManager

async def custom_analysis_tool(data: str) -> Dict[str, Any]:
    # 您的自定义分析逻辑
    return {"result": f"已分析: {data}"}

# 注册工具
await mcp_manager.register_local_tool(
    tool_name="custom_analysis",
    tool_func=custom_analysis_tool,
    description="执行自定义数据分析",
    parameters={"data": {"type": "string", "description": "要分析的数据"}}
)
```

#### 自定义图表类型

扩展图表生成器以支持专门的财务图表：

```python
from src.report.chart_generator import ChartGenerator

class CustomChartGenerator(ChartGenerator):
    async def generate_custom_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # 自定义图表生成逻辑
        return chart_config
```

## 🏗️ 系统架构

### 系统概览

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gradio UI     │    │   Planning      │    │   Sub-Agents    │
│   界面           │◄──►│   Agent         │◄──►│   (Browser,     │
│                 │    │   规划智能体    │    │    Search,       │
└─────────────────┘    └─────────────────┘    │    Analyze,       │
                              ▲                │    Final)        │
                              │                └─────────────────┘
                              │                         ▲
┌─────────────────┐    ┌─────────────────┐          │
│   Search        │    │   MCP           │          │
│   搜索引擎      │    │   Manager       │──────────┘
│   (Serper,      │    │   管理器        │             
│    Metaso,      │    └─────────────────┘             
│    Sogou)       │             
└─────────────────┘             
         ▲                             
         │                             
┌─────────────────┐             
│   Report        │             
│   报告生成器    │             
│   (HTML,        │             
│    Charts,      │             
│    Citations)   │             
└─────────────────┘             
```

### 核心组件

#### 智能体 (Agents)
- **BaseAgent**: 所有智能体的抽象基类
- **PlanningAgent**: 任务分解和工作流编排
- **BrowserAgent**: Web自动化和内容提取
- **DeepSearchAgent**: 多引擎搜索协调
- **DeepAnalyzeAgent**: 金融数据分析
- **FinalAnswerAgent**: 报告生成和格式化

#### 搜索集成 (Search Integration)
- **SearchManager**: 协调多个搜索引擎
- **SerperEngine**: Google搜索API封装
- **MetasoEngine**: Metaso搜索API封装
- **SogouEngine**: 搜狗搜索API封装

#### 报告生成 (Report Generation)
- **HTMLReportGenerator**: 创建专业HTML报告
- **ChartGenerator**: 使用Chart.js生成各种图表
- **CitationManager**: 管理多种引用格式

#### MCP集成 (MCP Integration)
- **MCPManager**: 处理MCP协议通信
- **Tool Registry**: 动态工具注册和发现
- **Connection Management**: 本地和远程服务器连接

## 🔧 开发指南

### 项目结构

```
DeepReport/
├── src/
│   ├── agents/                 # AI智能体
│   │   ├── base_agent.py      # 基础智能体类
│   │   ├── planning_agent.py  # 规划智能体
│   │   └── sub_agents.py      # 专门子智能体
│   ├── search/                # 搜索引擎集成
│   │   ├── search_manager.py  # 搜索协调
│   │   └── engines.py         # 搜索引擎实现
│   ├── report/                # 报告生成
│   │   ├── html_generator.py  # HTML报告生成器
│   │   ├── chart_generator.py # 图表生成
│   │   └── citation_manager.py # 引用管理
│   └── utils/                 # 工具类
│       ├── model_adapter.py   # AI模型适配器
│       └── mcp_manager.py     # MCP协议管理器
├── templates/                 # HTML模板
├── static/                    # 静态资源
├── tests/                     # 测试文件
├── docs/                      # 文档
├── main.py                    # 主应用
├── config.py                  # 配置管理
├── requirements.txt           # 依赖
└── README.md                  # 英文说明
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_agents.py

# 带覆盖率运行
python -m pytest --cov=src tests/
```


## 🤝 参与贡献

我们欢迎贡献！请参阅我们的[贡献指南](CONTRIBUTING_CN.md)了解详情。

### 如何贡献

1. **Fork仓库**
2. **创建功能分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **进行更改**
4. **添加测试**
5. **确保所有测试通过**
6. **提交更改**
   ```bash
   git commit -m '添加惊人功能'
   ```
7. **推送到分支**
   ```bash
   git push origin feature/amazing-feature
   ```
8. **打开Pull Request**

## 🐳 Docker部署

### 🚀 一键快速启动

最简单的启动DeepReport的方式：

```bash
# 克隆并启动
git clone https://github.com/your-username/DeepReport.git
cd DeepReport
./start.sh
```

这将：
- 检查Docker是否运行
- 创建.env文件（如果需要）
- 构建并启动所有服务
- 提供访问URL

### 快速启动脚本

```bash
# 启动应用
./start.sh

# 停止应用
./stop.sh

# 完整部署（包含所有选项）
./docker-deploy.sh deploy

# 检查状态
./docker-deploy.sh status

# 查看日志
./docker-deploy.sh logs
```


## 📋 路线图

### 版本1.0 (当前)
- ✅ 基于SmolAgents框架
- ✅ 专门化智能体：DeepResearcher、Browser、DeepAnalyze、FinalAnswer
- ✅ 多引擎搜索协调
- ✅ 带有丰富可视化的HTML报告生成
- ✅ Gradio Web界面
- ✅ 基于FastMCP的MCP协议支持
- ✅ 每个智能体的完整工具系统
- ✅ 专业引用管理

### 版本1.1 (计划中)
- 🔄 增强多模态能力
- 🔄 更好的上下文管理
- 🔄 私有数据接入功能

## 📄 许可证

本项目采用MIT许可证 - 详情请参阅[LICENSE](LICENSE)文件。

## 参考
[browser-use](https://github.com/browser-use/browser-use)
[smolagents](https://github.com/huggingface/smolagents)

## 📞 支持

- **文档**: [docs/](docs/)
- **问题**: [GitHub Issues](https://github.com/your-username/DeepReport/issues)
- **讨论**: [GitHub Discussions](https://github.com/your-username/DeepReport/discussions)
- **邮件**: support@deepreport.ai

## 🌟 Star历史

如果您觉得这个项目有用，请考虑在GitHub上给它一个star！

---

**DeepReport** - 用AI智能体和综合分析工具赋能金融研究。

---




- [贡献指南(English)](CONTRIBUTING.md) | [贡献指南(中文)](CONTRIBUTING_CN.md)