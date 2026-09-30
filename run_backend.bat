@echo off
title Lymphoma Detection - FastAPI Backend Server
echo =======================================================
echo  Starting FastAPI Backend Server on http://localhost:8000
echo =======================================================
cd /d "%~dp0"
set PYTHONPATH=%CD%
.\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
pause
