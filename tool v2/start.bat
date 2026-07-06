@echo off
title Swaxx-Tools
cd /d "%~dp0"

:: Find Python
set PYTHON_CMD=
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    where py >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py -3
    ) else (
        echo Python not found. Please install Python 3.8+.
        pause
        exit /b 1
    )
)

%PYTHON_CMD% Swaxx\main.py
pause