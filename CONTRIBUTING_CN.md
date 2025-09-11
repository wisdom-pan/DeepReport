# DeepReport 贡献指南

感谢您对DeepReport项目的贡献兴趣！本文档为贡献者提供指导说明。

## 📋 目录

- [行为准则](#行为准则)
- [入门指南](#入门指南)
- [开发工作流](#开发工作流)
- [Pull Request流程](#pull-request流程)
- [编码标准](#编码标准)
- [测试指南](#测试指南)
- [文档编写](#文档编写)
- [问题报告](#问题报告)

## 🤝 行为准则

本项目和所有参与者都遵守[行为准则](CODE_OF_CONDUCT_CN.md)。通过参与，您期望遵守该准则。

## 🚀 入门指南

### 前置要求

- Python 3.8 或更高版本
- Git
- Python、异步编程和AI/ML概念的基础知识

### 设置开发环境

1. **Fork仓库**
   ```bash
   # 在GitHub上Fork仓库
   git clone https://github.com/YOUR_USERNAME/DeepReport.git
   cd DeepReport
   ```

2. **设置虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # 开发依赖
   ```

4. **设置pre-commit钩子**
   ```bash
   pre-commit install
   ```

5. **创建环境文件**
   ```bash
   cp .env.example .env
   # 编辑.env文件配置（不要提交此文件）
   ```

6. **验证设置**
   ```bash
   python -m pytest tests/
   python main.py  # 应该启动应用
   ```

## 🔄 开发工作流

### 1. 选择问题

- 查看现有的[issues](https://github.com/your-username/DeepReport/issues)
- 寻找标记为"good first issue"或"help wanted"的问题
- 如果您有功能想法或错误报告，创建新问题

### 2. 创建分支

```bash
# 创建新功能分支
git checkout -b feature/您的功能名称

# 或用于错误修复
git checkout -b fix/您的修复名称

# 或用于文档
git checkout -b docs/您的文档名称
```

### 3. 进行更改

- 编写清晰、有文档的代码
- 遵循下面的编码标准
- 为新功能添加测试
- 根据需要更新文档

### 4. 测试您的更改

```bash
# 运行所有测试
python -m pytest tests/

# 带覆盖率运行
python -m pytest --cov=src tests/

# 运行特定测试
python -m pytest tests/test_agents.py

# 运行代码检查
flake8 src/
black src/
mypy src/
```

### 5. 提交更改

```bash
# 添加您的更改
git add .

# 清晰的提交信息
git commit -m "添加: 功能描述"

# 推送到您的fork
git push origin feature/您的功能名称
```

## 📝 Pull Request流程

### 创建Pull Request

1. **确保您的分支是最新的**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **创建Pull Request**
   - 转到GitHub上的原始仓库
   - 点击"New Pull Request"
   - 从下拉列表中选择您的分支
   - 填写PR模板

3. **PR描述**
   - 描述更改的清晰标题
   - 详细说明您做了什么以及为什么
   - 列出任何破坏性更改
   - 如适用，包含截图
   - 链接到相关问题

### PR审核流程

1. **自动检查**
   - 所有测试必须通过
   - 代码必须通过linting
   - 文档必须成功构建

2. **代码审核**
   - 至少需要一名维护者批准
   - 解决所有审核意见
   - 保持PR聚焦和小型化

3. **合并**
   - PR由维护者合并
   - 为更清晰的历史记录压缩提交
   - 合并后删除功能分支

## 📏 编码标准

### Python风格指南

- 遵循[PEP 8](https://www.python.org/dev/peps/pep-0008/)
- 使用[Black](https://black.readthedocs.io/)进行格式化
- 使用[isort](https://pycqa.github.io/isort/)进行导入排序
- 最大行长度：88个字符（Black默认值）

### 代码组织

```
src/
├── agents/          # AI智能体实现
├── search/          # 搜索引擎集成
├── report/          # 报告生成
└── utils/           # 工具函数
```

### 文档标准

#### Docstrings

使用Google风格的docstrings：

```python
def generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
    """从给定数据生成综合报告。

    Args:
        data: 包含报告数据的字典，包括部分、图表和引用。

    Returns:
        包含生成的报告和元数据的字典。

    Raises:
        ValueError: 如果缺少或无效必需数据。
    """
    # 实现
```

#### 注释

- 编写自文档化的代码
- 用注释解释"为什么"而不是"是什么"
- 保持注释更新
- 适当使用TODO/FIXME/NOTE标记

### 类型提示

- 为所有函数签名使用类型提示
- 对可空类型使用Optional
- 为复杂结构定义自定义类型

```python
from typing import Dict, Any, List, Optional

def process_data(
    input_data: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """处理输入数据和可选配置"""
    # 实现
```

### 错误处理

- 使用特定的异常类型
- 提供有意义的错误消息
- 适当记录错误
- 不要静默抑制异常

```python
try:
    result = await agent.execute_task(task)
except ValueError as e:
    logger.error(f"无效任务参数: {e}")
    raise
except Exception as e:
    logger.error(f"执行任务时出现意外错误: {e}")
    raise TaskExecutionError(f"执行任务失败: {e}")
```

### Async/Await模式

- 一致使用async/await
- 适当处理超时
- 使用asyncio.gather进行并发操作
- 避免在async函数中阻塞调用

## 🧪 测试指南

### 测试结构

```
tests/
├── unit/           # 单元测试
├── integration/    # 集成测试
├── e2e/           # 端到端测试
└── fixtures/      # 测试数据
```

### 编写测试

- 对所有测试使用pytest
- 编写描述性的测试名称
- 对常见设置使用fixtures
- 模拟外部依赖
- 测试成功和失败情况

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_agent_execution_success():
    """测试智能体成功执行任务"""
    agent = TestAgent()
    task = Task(id="test", type="test", description="测试任务", parameters={})
    
    result = await agent.execute_task(task)
    
    assert result.success is True
    assert result.result is not None
    assert result.execution_time > 0
```

### 测试覆盖率

- 目标80%+的代码覆盖率
- 专注于关键路径
- 不要测试实现细节
- 使用覆盖率工具识别差距

```bash
# 生成覆盖率报告
python -m pytest --cov=src --cov-report=html --cov-report=term tests/

# 查看HTML报告
open htmlcov/index.html
```

## 📚 文档编写

### 文档类型

1. **代码文档**
   - 所有公共函数/类的docstrings
   - 复杂逻辑的内联注释
   - 所有签名的类型提示

2. **用户文档**
   - README.md包含设置和使用说明
   - API文档
   - 新功能的示例脚本和教程

3. **开发者文档**
   - 架构概览
   - 贡献指南
   - 开发设置

### 添加文档

- 为面向用户的更改更新README.md
- 为新函数/类添加docstrings
- 为新功能创建示例脚本
- 为架构更改更新架构图

## 🐛 问题报告

### 错误报告

报告错误时，请包括：

1. **环境信息**
   - Python版本
   - 操作系统
   - DeepReport版本
   - 相关依赖

2. **重现步骤**
   - 清晰、可重现的步骤
   - 如适用的示例代码
   - 预期与实际行为

3. **错误消息**
   - 完整的错误堆栈跟踪
   - 可用的日志文件
   - 如适用的屏幕截图

### 功能请求

对于功能请求，请提供：

1. **问题陈述**
   - 您试图解决什么问题？
   - 当前的解决方法（如果有）

2. **建议的解决方案**
   - 功能的详细描述
   - 它如何工作
   - 用例和示例

3. **实现想法**
   - 潜在方法
   - 相关代码更改
   - 如适用，破坏性更改

### 问题模板

```markdown
## 问题类型
- [ ] 错误
- [ ] 功能请求
- [ ] 文档
- [ ] 问题

## 环境
- Python版本: 
- 操作系统: 
- DeepReport版本: 

## 描述
[问题的详细描述]

## 重现步骤
1. 步骤一
2. 步骤二
3. 步骤三

## 预期行为
[您期望发生什么]

## 实际行为
[实际发生了什么]

## 附加上下文
[日志、屏幕截图或其他相关信息]
```

## 🏆 认可

贡献者因其宝贵贡献而获得认可：

- **特色贡献者**：在README.md中列出
- **发布说明**：在更新日志中提及
- **贡献者徽章**：用于重要贡献
- **维护者权限**：用于一致、高质量的贡献

## 📞 获取帮助

- **讨论**：[GitHub Discussions](https://github.com/your-username/DeepReport/discussions)
- **问题**：[GitHub Issues](https://github.com/your-username/DeepReport/issues)
- **Discord**：[社区服务器](https://discord.gg/deepreport)
- **邮件**：developers@deepreport.ai

## 📄 许可证

通过为DeepReport做贡献，您同意您的贡献将在[MIT许可证](LICENSE)下许可。

---

感谢您为DeepReport做出贡献！🎉

---

## 🌐 语言选择 / Language Selection

- [English](CONTRIBUTING.md) | [中文](CONTRIBUTING_CN.md)
- [README(English)](README.md) | [README(中文)](README_CN.md)