@echo off
REM NSQIP Analysis Helper Script for Windows

if "%1"=="" goto usage
if "%1"=="help" goto usage

if "%1"=="edit" goto edit
if "%1"=="run" goto run  
if "%1"=="new" goto new

echo Error: Unknown command '%1'
goto usage

:edit
if "%2"=="" (
    echo Error: Please specify a notebook file to edit
    echo Example: nsqip edit analysis.py
    exit /b 1
)
echo Starting marimo in sandbox mode...
uv run marimo edit --sandbox %2
goto end

:run
if "%2"=="" (
    echo Error: Please specify a notebook file to run
    echo Example: nsqip run analysis.py
    exit /b 1
)
echo Starting marimo in sandbox mode...
uv run marimo run --sandbox %2
goto end

:new
echo Starting marimo in sandbox mode...
if "%2"=="" (
    uv run marimo new --sandbox
) else (
    echo Note: Will create new notebook. Save as '%2' when ready.
    uv run marimo new --sandbox
)
goto end

:usage
echo.
echo NSQIP Analysis Helper
echo.
echo Usage:
echo     nsqip edit [notebook]     - Edit a notebook (creates if doesn't exist)
echo     nsqip run [notebook]      - Run a notebook in read-only mode
echo     nsqip new [name]          - Create a new notebook
echo     nsqip help               - Show this message
echo.
echo Examples:
echo     nsqip edit analysis.py
echo     nsqip edit projects\smith-mortality\analysis.py
echo     nsqip run shared\templates\basic_analysis.py
echo     nsqip new exploratory_analysis.py
echo.
echo All commands automatically use sandbox mode for safety.

:end