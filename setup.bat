@echo off
echo 🚀 LLM-Powered Query-Retrieval System - Windows Setup
echo ========================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing requirements...
pip install -r requirements.txt

REM Check environment variables
echo 🔍 Checking environment configuration...
if not exist ".env" (
    echo ⚙️ Creating .env file from template...
    copy .env.example .env
    echo ❗ Please edit .env file with your OpenAI API key and other settings
)

REM Test installation
echo 🧪 Testing installation...
python -c "try: import fastapi, uvicorn, openai, sentence_transformers, faiss; print('✅ All required packages installed successfully'); except ImportError as e: print(f'❌ Missing package: {e}'); exit(1)"

echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your OpenAI API key
echo 2. Run: python main.py
echo 3. Test with: python test_api.py
echo.
echo For deployment:
echo - Heroku: git push heroku main
echo - Railway: Connect GitHub repository
echo - Render: Deploy from GitHub

pause
