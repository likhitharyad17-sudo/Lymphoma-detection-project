@echo off
title Lymphoma Detection - React Frontend Dashboard
echo =======================================================
echo  Starting React Frontend Dashboard on http://localhost:5173
echo =======================================================
cd /d "%~dp0\frontend"
set "PATH=C:\Program Files\nodejs;%PATH%"
npm run dev
pause
