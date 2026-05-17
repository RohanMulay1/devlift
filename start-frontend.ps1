# DevLift Frontend Startup Script for Windows PowerShell

Write-Host "🚀 Starting DevLift Frontend..." -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "frontend/package.json")) {
    Write-Host "❌ Error: Please run this script from the devlift root directory" -ForegroundColor Red
    exit 1
}

# Check if node_modules exists
if (-not (Test-Path "frontend/node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✅ Dependencies OK" -ForegroundColor Green
}

# Check if .env.local exists
if (-not (Test-Path "frontend/.env.local")) {
    Write-Host "⚠️  Creating .env.local file..." -ForegroundColor Yellow
    "NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath "frontend/.env.local" -Encoding utf8
    Write-Host "✅ Created frontend/.env.local" -ForegroundColor Green
}

# Start the development server
Write-Host ""
Write-Host "🌐 Starting Next.js development server on http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Make sure the backend is running on http://localhost:8000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

Set-Location frontend
npm run dev

# Made with Bob
