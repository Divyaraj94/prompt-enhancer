@echo off
title AI Prompt Coach
echo ============================================
echo        AI Prompt Coach - Starting...
echo ============================================
echo.
cd /d "%~dp0"

:: REPLACE 'your_api_key_here' WITH YOUR ACTUAL GEMINI API KEY!
set GEMINI_API_KEY=your_api_key_here

python main.py
pause
