#!/bin/bash

# Quick start script for DeepReport Docker deployment
# This provides the simplest way to start the application

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 DeepReport Quick Start${NC}"
echo "=============================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env file with your API keys:${NC}"
    echo "- OPENAI_API_KEY"
    echo "- SERPER_API_KEY"
    echo "- ANTHROPIC_API_KEY (optional)"
    read -p "Press Enter after editing .env file, or Ctrl+C to exit..."
fi

# Create directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p reports logs ssl

# Build and start
echo -e "${BLUE}Building and starting DeepReport...${NC}"
docker-compose up -d --build

# Wait for startup
echo -e "${BLUE}Waiting for service to start...${NC}"
sleep 10

# Check status
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ DeepReport is running successfully!${NC}"
    echo -e "${GREEN}📱 Access the application at: http://localhost:7860${NC}"
    echo ""
    echo "Useful commands:"
    echo "  View logs:    docker-compose logs -f"
    echo "  Stop service: docker-compose down"
    echo "  Restart:      docker-compose restart"
    echo ""
    echo "📊 Generated reports will be saved in the ./reports directory"
else
    echo -e "${YELLOW}⚠️  Service may have issues. Check logs with: docker-compose logs${NC}"
fi