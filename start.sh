#!/bin/bash
# Quick start script for Mocchibird Discord Bot

echo "=================================="
echo "Mocchibird Discord Bot Quick Start"
echo "=================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your credentials:"
    echo "   - DISCORD_TOKEN"
    echo "   - OPENAI_API_KEY (or 'ollama' for local)"
    echo "   - OPENAI_API_BASE (default works for Ollama)"
    echo "   - MODEL_NAME"
    echo ""
    echo "Run this script again after configuring .env"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    # Check if python3 is available
    if command -v python3 &> /dev/null; then
        python3 -m venv venv
    elif command -v python &> /dev/null; then
        python -m venv venv
    else
        echo "❌ Python is not installed or not in PATH!"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Check if config.yaml exists
if [ ! -f config.yaml ]; then
    echo "❌ config.yaml not found!"
    exit 1
fi

echo ""
echo "=================================="
echo "Starting Mocchibird..."
echo "=================================="
echo ""

# Run the bot
python bot.py
