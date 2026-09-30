@echo off
title Lymphoma Detection - Benchmark Evaluation
echo =======================================================
echo  Evaluating All 8 Deep Learning Models on Test Split...
echo =======================================================
cd /d "%~dp0"
set PYTHONPATH=%CD%
.\venv\Scripts\python.exe backend/training/evaluation/evaluate_and_benchmark.py
echo =======================================================
pause
