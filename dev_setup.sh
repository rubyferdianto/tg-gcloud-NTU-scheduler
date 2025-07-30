#!/bin/bash

# Development script for local testing
echo "🔧 Setting up local development environment"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file template..."
    cat > .env << EOF
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Only needed for Cloud Run deployment
# WEBHOOK_URL=https://your-service-url.run.app
EOF
    echo "⚠️  Please edit .env file and add your Telegram bot token"
else
    echo "✅ .env file already exists"
fi

echo "🧪 Running setup tests..."
python test_setup.py

echo ""
echo "🚀 To start local development:"
echo "1. Edit .env and add your TELEGRAM_BOT_TOKEN"
echo "2. Run: source venv/bin/activate"
echo "3. Run: export \$(cat .env | xargs) && python src/index.py"
