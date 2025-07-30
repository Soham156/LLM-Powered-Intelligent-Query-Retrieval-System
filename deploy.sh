#!/bin/bash

echo "🚀 LLM-Powered Query-Retrieval System - Deployment Script"
echo "========================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Check environment variables
echo "🔍 Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    echo "❗ Please edit .env file with your OpenAI API key and other settings"
fi

# Test installation
echo "🧪 Testing installation..."
python3 -c "
try:
    import fastapi, uvicorn, openai, sentence_transformers, faiss
    print('✅ All required packages installed successfully')
except ImportError as e:
    print(f'❌ Missing package: {e}')
    exit(1)
"

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key"
echo "2. Run: python main.py"
echo "3. Test with: python test_api.py"
echo ""
echo "For deployment:"
echo "- Heroku: git push heroku main"
echo "- Railway: Connect GitHub repository"
echo "- Render: Deploy from GitHub"
