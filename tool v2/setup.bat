@echo off
title Swaxx-Tools Setup

echo.
echo ================================================================
echo                     SWAXX-TOOLS SETUP
echo                     version 1.0
echo ================================================================
echo.
echo -----------------------------------------------------------------
echo  Tools Included:
echo   HOME      – GitHub, Discord, Changelog, Credits
echo   OSINT     – IP Lookup, Domain Intel, Email Search
echo   ATTACK    – UDP Flood, HTTP Flood, Ping Sweep
echo   DISCORD   – User Lookup, Token Checker, Invite Resolver
echo   SOCIAL    – Twitter, Instagram, Facebook OSINT
echo   ROBLOX    – User, Game, Group Lookup
echo   IP/WEB    – Geolocation, DNS, WHOIS
echo   GEN       – Username, Password, Email, Proxy Generators
echo   MONITOR   – Network, Webhook, Status Check
echo   UTILS     – Config, Sync, More Tools
echo -----------------------------------------------------------------
echo.

:: Find Python executable
set PYTHON_CMD=
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    where py >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py -3
    ) else (
        echo [ERROR] Python not found. Please install Python 3.8+ from https://python.org
        echo        Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
)

echo [*] Using Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

:: Check if requirements.txt exists
if not exist "Swaxx\requirements.txt" (
    echo [ERROR] requirements.txt not found in Swaxx folder.
    echo        Make sure you are running setup.bat from the root folder.
    pause
    exit /b 1
)

:: Upgrade pip
echo [*] Upgrading pip...
%PYTHON_CMD% -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [WARNING] pip upgrade failed. Continuing anyway...
)

:: Install dependencies
echo [*] Installing dependencies from Swaxx\requirements.txt...
%PYTHON_CMD% -m pip install -r Swaxx\requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    echo        Try running manually: %PYTHON_CMD% -m pip install -r Swaxx\requirements.txt
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All dependencies installed!
echo.
echo ================================================================
echo  Setup complete! Run start.bat to launch Swaxx-Tools.
echo ================================================================
pause