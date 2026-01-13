@echo off
echo 🚀 Starting Smart YouTube Analyzer...

REM Check if virtual environment exists
if not exist "backend\venv\" (
    echo ⚠️  Virtual environment not found. Please run setup first.
    exit /b 1
)

REM Start backend
echo 📡 Starting backend server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python main.py"

REM Wait for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend
echo 🎨 Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo ✅ Application started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Close the terminal windows to stop the servers
