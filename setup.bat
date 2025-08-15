@echo off
REM Tetracore Server - Automated Setup Script for Windows

echo.
echo 🌌 Tetracore Server Simulation - Automated Setup
echo ==================================================

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo [SUCCESS] Python found
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 16 or higher.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
) else (
    echo [SUCCESS] Node.js found
)

REM Check Yarn
yarn --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Yarn not found. Installing Yarn...
    npm install -g yarn
) else (
    echo [SUCCESS] Yarn found
)

REM Check MongoDB
mongod --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] MongoDB not found. 
    echo Please install MongoDB Community Server from:
    echo https://www.mongodb.com/try/download/community
    echo.
    echo After installation, make sure MongoDB service is running:
    echo   net start MongoDB
    echo.
    pause
)

echo.
echo [INFO] Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [INFO] Installing Python dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [ERROR] requirements.txt not found in backend directory
    pause
    exit /b 1
)

REM Setup environment variables
if not exist ".env" (
    echo [INFO] Creating backend .env file...
    copy .env.example .env
    echo [SUCCESS] Backend .env created from template
) else (
    echo [WARNING] Backend .env already exists, skipping...
)

echo [SUCCESS] Backend setup completed!

REM Setup Frontend
echo.
echo [INFO] Setting up frontend...
cd ..\frontend

REM Install dependencies
echo [INFO] Installing Node.js dependencies...
if exist "package.json" (
    yarn install
) else (
    echo [ERROR] package.json not found in frontend directory
    pause
    exit /b 1
)

REM Setup environment variables
if not exist ".env" (
    echo [INFO] Creating frontend .env file...
    copy .env.example .env
    echo [SUCCESS] Frontend .env created from template
) else (
    echo [WARNING] Frontend .env already exists, skipping...
)

echo [SUCCESS] Frontend setup completed!

REM Start MongoDB service
echo.
echo [INFO] Starting MongoDB service...
net start MongoDB >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Could not start MongoDB service automatically.
    echo Please start it manually: net start MongoDB
) else (
    echo [SUCCESS] MongoDB service started
)

cd ..

echo.
echo [SUCCESS] Setup completed successfully!
echo.
echo 🚀 To start the application:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   python server.py
echo.
echo Terminal 2 - Frontend:
echo   cd frontend  
echo   yarn start
echo.
echo Then open http://localhost:3000 in your browser
echo.
echo [SUCCESS] Happy simulating! 🌌
echo.
pause