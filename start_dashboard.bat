@echo off
REM NANDA Dashboard Quick Start Script for Windows

echo ========================================
echo  NANDA Hackathon Dashboard Setup
echo ========================================
echo.

REM Check Python
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.9+
    pause
    exit /b 1
)
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Check for secrets file
if not exist ".streamlit\secrets.toml" (
    echo First-time setup detected
    echo.
    set /p connect_notion="Do you want to connect to Notion? (y/n): "
    
    if /i "%connect_notion%"=="y" (
        echo.
        set /p api_key="Enter your Notion API key: "
        set /p database_id="Enter your Database ID: "
        
        if not exist ".streamlit" mkdir .streamlit
        
        (
            echo NOTION_API_KEY = "%api_key%"
            echo DATABASE_ID = "%database_id%"
        ) > .streamlit\secrets.toml
        
        echo Notion credentials saved
    ) else (
        echo Using sample data
    )
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Starting dashboard...
echo Dashboard will open at http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

REM Run the dashboard
streamlit run nanda_dashboard_app.py

pause
