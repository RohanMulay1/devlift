# DevLift Backend Startup Script for Windows PowerShell

Write-Host "🚀 Starting DevLift Backend..." -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "backend/main.py")) {
    Write-Host "❌ Error: Please run this script from the devlift root directory" -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path "backend/.env")) {
    Write-Host "❌ Error: backend/.env file not found" -ForegroundColor Red
    Write-Host "Please create backend/.env with your credentials" -ForegroundColor Yellow
    exit 1
}

# Check if dependencies are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
$pipList = pip list 2>&1
if ($pipList -notmatch "fastapi") {
    Write-Host "⚠️  Dependencies not installed. Installing now..." -ForegroundColor Yellow
    Set-Location backend
    python -m pip install -r requirements.txt
    Set-Location ..
}

Write-Host "✅ Dependencies OK" -ForegroundColor Green

# Start the server
Write-Host ""
Write-Host "🌐 Starting FastAPI server on http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "❤️  Health Check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

Set-Location backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Made with Bob
