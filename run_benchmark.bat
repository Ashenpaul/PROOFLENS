@echo off
title Proof-Carrying Data Analyst (Benchmark Suite)
cd /d "%~dp0"
echo ======================================================================
echo Running All 10 Adversarial & Analytical Benchmarks...
echo ======================================================================
python -m unittest tests\test_benchmark.py
echo.
echo ======================================================================
echo Benchmark run complete. Press any key to close this window.
echo ======================================================================
pause
