# Contributing to DeepReport

Thank you for your interest in contributing to DeepReport! This document provides guidelines and instructions for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Reporting Issues](#reporting-issues)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Python, async programming, and AI/ML concepts

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Fork the repository on GitHub
   git clone https://github.com/YOUR_USERNAME/DeepReport.git
   cd DeepReport
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (DO NOT commit this file)
   ```

6. **Verify setup**
   ```bash
   python -m pytest tests/
   python main.py  # Should start the application
   ```

## 🔄 Development Workflow

### 1. Choose an Issue

- Check existing [issues](https://github.com/your-username/DeepReport/issues)
- Look for issues labeled "good first issue" or "help wanted"
- Create a new issue if you have a feature idea or bug report

### 2. Create a Branch

```bash
# Create a new feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/your-fix-name

# Or for documentation
git checkout -b docs/your-docs-name
```

### 3. Make Changes

- Write clean, documented code
- Follow the coding standards below
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test
python -m pytest tests/test_agents.py

# Run linting
flake8 src/
black src/
mypy src/
```

### 5. Commit Changes

```bash
# Add your changes
git add .

# Commit with a clear message
git commit -m "Add: feature description"

# Push to your fork
git push origin feature/your-feature-name
```

## 📝 Pull Request Process

### Creating a Pull Request

1. **Ensure your branch is up to date**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch from the dropdown
   - Fill in the PR template

3. **PR Description**
   - Clear title describing the change
   - Detailed description of what you did and why
   - List any breaking changes
   - Include screenshots if applicable
   - Link to relevant issues

### PR Review Process

1. **Automated Checks**
   - All tests must pass
   - Code must pass linting
   - Documentation must build successfully

2. **Code Review**
   - At least one maintainer must approve
   - Address all review comments
   - Keep PRs focused and small

3. **Merge**
   - PRs are merged by maintainers
   - Squash commits for cleaner history
   - Delete feature branches after merge

## 📏 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 88 characters (Black default)

### Code Organization

```
src/
├── agents/          # AI agent implementations
├── search/          # Search engine integrations
├── report/          # Report generation
└── utils/           # Utility functions
```

### Documentation Standards

#### Docstrings

Use Google-style docstrings:

```python
def generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a comprehensive report from the given data.

    Args:
        data: Dictionary containing report data including sections,
              charts, and citations.

    Returns:
        Dictionary containing the generated report and metadata.

    Raises:
        ValueError: If required data is missing or invalid.
    """
    # Implementation
```

#### Comments

- Write self-documenting code
- Use comments to explain "why" not "what"
- Keep comments up to date
- Use TODO/FIXME/NOTE markers appropriately

### Type Hints

- Use type hints for all function signatures
- Use Optional for nullable types
- Define custom types for complex structures

```python
from typing import Dict, Any, List, Optional

def process_data(
    input_data: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Process input data with optional configuration."""
    # Implementation
```

### Error Handling

- Use specific exception types
- Provide meaningful error messages
- Log errors appropriately
- Don't suppress exceptions silently

```python
try:
    result = await agent.execute_task(task)
except ValueError as e:
    logger.error(f"Invalid task parameters: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error executing task: {e}")
    raise TaskExecutionError(f"Failed to execute task: {e}")
```

### Async/Await Patterns

- Use async/await consistently
- Handle timeouts appropriately
- Use asyncio.gather for concurrent operations
- Avoid blocking calls in async functions

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
└── fixtures/      # Test data
```

### Writing Tests

- Use pytest for all tests
- Write descriptive test names
- Use fixtures for common setup
- Mock external dependencies
- Test both success and failure cases

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_agent_execution_success():
    """Test that agent executes tasks successfully."""
    agent = TestAgent()
    task = Task(id="test", type="test", description="Test task", parameters={})
    
    result = await agent.execute_task(task)
    
    assert result.success is True
    assert result.result is not None
    assert result.execution_time > 0
```

### Test Coverage

- Aim for 80%+ code coverage
- Focus on critical paths
- Don't test implementation details
- Use coverage tools to identify gaps

```bash
# Generate coverage report
python -m pytest --cov=src --cov-report=html --cov-report=term tests/

# View HTML report
open htmlcov/index.html
```

## 📚 Documentation

### Documentation Types

1. **Code Documentation**
   - Docstrings for all public functions/classes
   - Inline comments for complex logic
   - Type hints for all signatures

2. **User Documentation**
   - README.md with setup and usage
   - API documentation
   - Example scripts and tutorials

3. **Developer Documentation**
   - Architecture overview
   - Contribution guidelines
   - Development setup

### Adding Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Create example scripts for new features
- Update architecture diagrams for structural changes

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Operating system
   - DeepReport version
   - Relevant dependencies

2. **Steps to Reproduce**
   - Clear, reproducible steps
   - Sample code if applicable
   - Expected vs actual behavior

3. **Error Messages**
   - Full error tracebacks
   - Log files if available
   - Screenshots if applicable

### Feature Requests

For feature requests, please provide:

1. **Problem Statement**
   - What problem are you trying to solve?
   - Current workarounds if any

2. **Proposed Solution**
   - Detailed description of the feature
   - How it would work
   - Use cases and examples

3. **Implementation Ideas**
   - Potential approaches
   - Relevant code changes
   - Breaking changes if any

### Issue Template

```markdown
## Issue Type
- [ ] Bug
- [ ] Feature Request
- [ ] Documentation
- [ ] Question

## Environment
- Python version: 
- Operating system: 
- DeepReport version: 

## Description
[Detailed description of the issue]

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
[What you expected to happen]

## Actual Behavior
[What actually happened]

## Additional Context
[Logs, screenshots, or other relevant information]
```

## 🏆 Recognition

Contributors are recognized for their valuable contributions:

- **Featured Contributors**: Listed in README.md
- **Release Notes**: Mentioned in changelog
- **Contributor Badges**: For significant contributions
- **Maintainer Access**: For consistent, high-quality contributions

## 📞 Getting Help

- **Discussions**: [GitHub Discussions](https://github.com/your-username/DeepReport/discussions)
- **Issues**: [GitHub Issues](https://github.com/your-username/DeepReport/issues)
- **Discord**: [Community Server](https://discord.gg/deepreport)
- **Email**: developers@deepreport.ai

## 📄 License

By contributing to DeepReport, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Thank you for contributing to DeepReport! 🎉