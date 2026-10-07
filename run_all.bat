@echo off
title Lymphoma Detection - Full Stack Launcher
echo =======================================================
echo  Starting Lymphoma Detection Full Stack System...
echo =======================================================

cd /d "%~dp0"
set "PATH=C:\Program Files\nodejs;%PATH%"

echo [1/2] Launching Backend Server in new window...
start "Lymphoma Detection - Backend API (Port 8000)" cmd /k "cd /d "%~dp0" && set PYTHONPATH=%CD% && .\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo [2/2] Launching Frontend Dashboard in new window...
start "Lymphoma Detection - React UI (Port 5173)" cmd /k "cd /d "%~dp0\frontend" && set "PATH=C:\Program Files\nodejs;%%PATH%%" && npm run dev"

timeout /t 3 /nobreak >nul

echo Opening browser at http://localhost:5173...
start http://localhost:5173

echo.
echo =======================================================
echo  System is running!
echo  - Frontend Dashboard : http://localhost:5173
echo  - Backend REST API   : http://localhost:8000
echo  - Interactive Docs   : http://localhost:8000/docs
echo =======================================================
echo Press any key to exit this launcher window (servers remain running).
pause >nul
