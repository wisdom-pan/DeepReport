"""
DeepReport setup configuration
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
def read_requirements(filename):
    """Read requirements from file"""
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="deepreport",
    version="1.0.0",
    author="DeepReport Team",
    author_email="contact@deepreport.ai",
    description="AI-powered financial research and report generation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/DeepReport",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "all": [
            "gradio==4.44.0",
            "langchain==0.2.12",
            "langchain-community==0.2.10",
            "langchain-openai==0.1.22",
            "langchain-core==0.3.23",
            "openai==1.44.0",
            "anthropic==0.34.2",
            "google-search-results==2.4.2",
            "requests==2.32.3",
            "beautifulsoup4==4.12.3",
            "pandas==2.2.2",
            "numpy==1.26.4",
            "matplotlib==3.9.2",
            "plotly==5.24.0",
            "jinja2==3.1.4",
            "pydantic==2.8.2",
            "asyncio==3.4.3",
            "aiohttp==3.9.5",
            "selenium==4.23.1",
            "browser-use==0.1.0",
            "PyMuPDF==1.23.8",
            "langchain-community==0.2.10",
            "lxml==5.3.0",
            "markdown==3.6",
            "python-dotenv==1.0.1",
            "tiktoken==0.7.0",
            "fastmcp==0.3.0",
            "webdriver-manager==4.0.2",
            "chromedriver-autoinstaller==0.6.4",
            "yfinance==0.2.40",
            "financial-datasets==0.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "deepreport=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*.html", "static/*", "docs/*"],
    },
    keywords="ai, financial, research, reports, agents, automation",
    project_urls={
        "Bug Reports": "https://github.com/your-username/DeepReport/issues",
        "Source": "https://github.com/your-username/DeepReport",
        "Documentation": "https://deepreport.readthedocs.io/",
    },
)