# Quick Setup Script for LinUtil Development (Windows PowerShell)

Write-Host "╔═══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      LinUtil - Quick Setup Script                 ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed!" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null
Write-Host "✓ Pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt | Out-Null
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Install development dependencies (optional)
$installDev = Read-Host "Install development dependencies? (y/n)"
if ($installDev -eq "y" -or $installDev -eq "Y") {
    pip install -r requirements-dev.txt | Out-Null
    Write-Host "✓ Development dependencies installed" -ForegroundColor Green
}

# Install package in development mode
Write-Host ""
Write-Host "Installing LinUtil in development mode..." -ForegroundColor Yellow
pip install -e . | Out-Null
Write-Host "✓ LinUtil installed" -ForegroundColor Green

# Note about running on Windows
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           Setup Complete! 🎉                      ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: LinUtil is designed for Linux systems." -ForegroundColor Yellow
Write-Host "On Windows, you can:" -ForegroundColor Yellow
Write-Host "  1. Use WSL (Windows Subsystem for Linux)" -ForegroundColor Yellow
Write-Host "  2. Test the configuration system" -ForegroundColor Yellow
Write-Host "  3. Develop and test UI components" -ForegroundColor Yellow
Write-Host ""
Write-Host "To test on Linux, use WSL:" -ForegroundColor Cyan
Write-Host "  wsl" -ForegroundColor White
Write-Host ""
Write-Host "To deactivate the virtual environment:" -ForegroundColor Cyan
Write-Host "  deactivate" -ForegroundColor White
Write-Host ""
