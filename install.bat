@echo off
REM install.bat
REM Windows batch file to install Notepad++ PythonScript scripts with shortcuts
REM Uses %~dp0 to find install.py in the same directory as this batch file

setlocal EnableDelayedExpansion

echo.
echo ======================================================================
echo Notepad++ PythonScript Scripts Installer
echo ======================================================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3 from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Check if install.py exists
if not exist "%SCRIPT_DIR%install.py" (
    echo ERROR: install.py not found in: %SCRIPT_DIR%
    echo.
    echo Please make sure install.py is in the same directory as install.bat
    echo.
    pause
    exit /b 1
)

REM Run the Python installer
echo Running installer...
echo.
python "%SCRIPT_DIR%install.py"

REM Check if installation was successful
if errorlevel 1 (
    echo.
    echo Installation failed! Please check the error messages above.
    echo.
    pause
    exit /b 1
)

REM Success
echo.
echo ======================================================================
echo Press any key to exit...
pause >nul
exit /b 0
