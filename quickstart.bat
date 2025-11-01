@echo off
REM UniRec Quick Start Script for Windows
REM This script automates the setup process

echo ============================================
echo 🚀 UniRec - Quick Start Setup (Windows)
echo ============================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python found
python --version

REM Check if Node.js is installed
echo.
echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+
    pause
    exit /b 1
)
echo ✓ Node.js found
node --version

REM Create project structure
echo.
echo Creating project directories...
if not exist data mkdir data
if not exist models mkdir models

REM Setup Python virtual environment
echo.
echo Setting up Python virtual environment...
python -m venv venv
echo ✓ Virtual environment created

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM Install Python dependencies
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✓ Python dependencies installed

REM Generate data
echo.
echo Generating sample data (this may take a minute)...
python generate_data.py
echo ✓ Sample data generated

REM Train models
echo.
echo Training models (this may take 5-10 minutes)...
python train_all_models.py
echo ✓ Models trained successfully

REM Setup frontend
echo.
echo Setting up frontend...
cd frontend

if not exist node_modules (
    echo Installing frontend dependencies...
    call npm install
    echo ✓ Frontend dependencies installed
) else (
    echo ✓ Frontend dependencies already installed
)

cd ..

REM Final instructions
echo.
echo ============================================
echo ✅ Setup Complete!
echo ============================================
echo.
echo To start the application:
echo.
echo 1. Start the backend (in one terminal):
echo    cd backend
echo    venv\Scripts\activate
echo    python api.py
echo.
echo 2. Start the frontend (in another terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Open your browser to: http://localhost:3000
echo.
echo Enjoy using UniRec! 🎉
echo ============================================
echo.
pause