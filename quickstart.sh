#!/bin/bash

# UniRec Quick Start Script
# This script automates the setup process

echo "============================================"
echo "🚀 UniRec - Quick Start Setup"
echo "============================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${BLUE}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check if Node.js is installed
echo -e "${BLUE}Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 16+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"

# Create project structure
echo ""
echo -e "${BLUE}Creating project directories...${NC}"
mkdir -p data models

# Setup Python virtual environment
echo ""
echo -e "${BLUE}Setting up Python virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install Python dependencies
echo ""
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Generate data
echo ""
echo -e "${BLUE}Generating sample data (this may take a minute)...${NC}"
python generate_data.py
echo -e "${GREEN}✓ Sample data generated${NC}"

# Train models
echo ""
echo -e "${BLUE}Training models (this may take 5-10 minutes)...${NC}"
python train_all_models.py
echo -e "${GREEN}✓ Models trained successfully${NC}"

# Setup frontend
echo ""
echo -e "${BLUE}Setting up frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    npm install
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Frontend dependencies already installed${NC}"
fi

cd ..

# Final instructions
echo ""
echo "============================================"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "============================================"
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend (in one terminal):"
echo "   cd backend"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   python api.py"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open your browser to: http://localhost:3000"
echo ""
echo -e "${BLUE}Enjoy using UniRec! 🎉${NC}"
echo "============================================"