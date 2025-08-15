@echo off
REM Tetracore Server - Start Script untuk Windows

echo.
echo 🌌 Tetracore Server Simulation - Startup
echo ========================================

REM Check MongoDB service
echo [INFO] Checking MongoDB status...
sc query MongoDB | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo [INFO] Starting MongoDB service...
    net start MongoDB
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to start MongoDB service
        echo Please run as Administrator or start MongoDB manually
        pause
        exit /b 1
    )
) else (
    echo [SUCCESS] MongoDB service is running
)

REM Wait for MongoDB to be ready
timeout /t 3 /nobreak >nul

REM Start Backend in new window
echo [INFO] Starting backend server...
start "Tetracore Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate.bat && python server.py"

REM Wait for backend to start
echo [INFO] Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Test backend health
curl -s http://localhost:8001/api/status >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Backend may still be starting up...
    timeout /t 3 /nobreak >nul
)

REM Start Frontend in new window  
echo [INFO] Starting frontend server...
start "Tetracore Frontend" cmd /k "cd /d %~dp0frontend && yarn start"

REM Wait for frontend to start
echo [INFO] Waiting for frontend to initialize...
timeout /t 8 /nobreak >nul

echo.
echo [SUCCESS] 🚀 All services started successfully!
echo.
echo Access your application:
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8001
echo   API Docs: http://localhost:8001/docs
echo.
echo Two new command windows have opened:
echo   - Tetracore Backend (running Python server)
echo   - Tetracore Frontend (running React dev server)
echo.
echo Close those windows to stop the services.
echo Your browser should automatically open to http://localhost:3000
echo.
echo [SUCCESS] Happy simulating! 🌌
echo.
pause