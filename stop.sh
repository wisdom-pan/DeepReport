#!/bin/bash

# Quick stop script for DeepReport Docker deployment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🛑 Stopping DeepReport...${NC}"

# Stop services
if docker-compose ps | grep -q "Up"; then
    docker-compose down
    echo -e "${GREEN}✅ DeepReport stopped successfully${NC}"
else
    echo -e "${YELLOW}⚠️  No services are currently running${NC}"
fi

# Optional: Clean up unused resources
echo -e "${BLUE}Cleaning up unused Docker resources...${NC}"
docker system prune -f > /dev/null 2>&1

echo -e "${GREEN}🧹 Cleanup completed${NC}"