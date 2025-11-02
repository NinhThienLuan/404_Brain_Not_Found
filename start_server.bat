@echo off
echo ========================================
echo   Starting Hackathon API Server
echo ========================================
echo.

echo [1/3] Checking dependencies...
python -c "import fastapi, uvicorn, pymongo, pydantic" 2>nul
if errorlevel 1 (
    echo [!] Missing dependencies. Installing...
    pip install -r requirements.txt
    echo [OK] Dependencies installed
) else (
    echo [OK] All dependencies found
)
echo.

echo [2/3] Checking email-validator...
python -c "import email_validator" 2>nul
if errorlevel 1 (
    echo [!] Installing email-validator...
    pip install email-validator
    echo [OK] email-validator installed
) else (
    echo [OK] email-validator found
)
echo.

echo [3/3] Starting server...
echo.
echo Server will run on: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

python -m BE.main

pause

