@echo off
echo.
echo ============================================
echo Newleads Daily - Starting Application
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing Python packages...
pip install -q -r requirements.txt

REM Check if database exists
if not exist "instance" mkdir instance
if not exist "newleadsdaily.db" (
    echo Initializing database...
    python init_db.py
)

REM Start the app
echo.
echo ============================================
echo Starting app on http://localhost:5000
echo ============================================
echo.
echo Press Ctrl+C to stop the app
echo.

python app.py

pause
