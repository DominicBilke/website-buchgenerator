#!/bin/bash

# BookGPT Server Startup Script
# This script sets up and starts the BookGPT server

set -e

echo "🚀 Starting BookGPT Server..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp env.example .env
    echo "📝 Please edit .env file and set your OPENAI_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Load environment variables
source .env

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "❌ OPENAI_API_KEY not set in .env file"
    echo "   Please edit .env file and set your OpenAI API key"
    exit 1
fi

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "🐳 Running in Docker container..."
    exec uvicorn main:app --host 0.0.0.0 --port 8000
else
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    
    # Start the server
    echo "🌟 Starting FastAPI server..."
    echo "   Server will be available at: http://localhost:8000"
    echo "   API docs will be available at: http://localhost:8000/docs"
    echo "   Health check: http://localhost:8000/health"
    echo "   Domain: bookgpt.bilke-projects.com"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fi 