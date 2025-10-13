#!/bin/bash
# Simple development server for local testing
# This serves the site locally without needing Docker/Podman

set -e

PORT="${1:-8000}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting local development server...${NC}"
echo ""
echo -e "${GREEN}Server running at:${NC} http://localhost:${PORT}"
echo -e "${GREEN}Press Ctrl+C to stop${NC}"
echo ""

# Start Python's built-in HTTP server
python3 -m http.server "$PORT"
