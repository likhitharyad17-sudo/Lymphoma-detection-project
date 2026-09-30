@echo off
title Lymphoma Detection - Automated Test Suite
echo =======================================================
echo  Running Automated PyTest Suite...
echo =======================================================
cd /d "%~dp0"
set PYTHONPATH=%CD%
.\venv\Scripts\pytest.exe backend/tests/test_api.py -v
echo =======================================================
pause
