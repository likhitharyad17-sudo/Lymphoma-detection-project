@echo off
title Lymphoma Detection - Full Stack Launcher
echo =======================================================
echo  Starting Lymphoma Detection Full Stack System...
echo =======================================================

cd /d "%~dp0"
set "PATH=C:\Program Files\nodejs;%PATH%"

echo [1/2] Launching Backend Server in new window...
start "Lymphoma Detection - Backend API" cmd /k "call "%~dp0run_backend.bat""

timeout /t 3 /nobreak >nul

echo [2/2] Launching Frontend Dashboard in new window...
start "Lymphoma Detection - React UI" cmd /k "call "%~dp0run_frontend.bat""

timeout /t 3 /nobreak >nul

echo Opening browser at http://localhost:5173...
start http://localhost:5173

echo.
echo =======================================================
echo  System is running!
echo  - Frontend Dashboard : http://localhost:5173
echo  - Backend REST API   : http://127.0.0.1:8000
echo  - Interactive Docs   : http://127.0.0.1:8000/docs
echo =======================================================
echo Press any key to exit this launcher window (servers remain running).
pause >nul
