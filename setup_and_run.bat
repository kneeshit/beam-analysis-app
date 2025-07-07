@echo off
echo ========================================
echo Beam Analysis Application Setup
echo ========================================

echo.
echo Setting up Backend...
cd backend
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Python dependencies!
    pause
    exit /b 1
)

echo.
echo Setting up Frontend...
cd ..\frontend
echo Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo Error installing Node.js dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo 1. Run start_backend.bat in one terminal
echo 2. Run start_frontend.bat in another terminal
echo 3. Open http://localhost:3000 in your browser
echo.
echo Or test the backend first with: python test_backend.py
echo.
pause
