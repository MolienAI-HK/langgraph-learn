<#
.SYNOPSIS
    food_analysis_api environment setup script
.DESCRIPTION
    Automatically sets up Python environment, installs dependencies and starts FastAPI server
#>

# Check Python installation
function Check-Python {
    try {
        $pythonVersion = (python --version 2>&1) -replace 'Python ', ''
        if (-not $pythonVersion) {
            throw "Python not found"
        }
        
        $majorVersion = $pythonVersion.Split('.')[0]
        if ($majorVersion -lt 3) {
            throw "Python 3.x required, found version: $pythonVersion"
        }
        
        Write-Host "Python $pythonVersion detected" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Error: $_" -ForegroundColor Red
        Write-Host "Please install Python 3.x from https://www.python.org/downloads/" -ForegroundColor Yellow
        return $false
    }
}

# Create/activate virtual environment
function Setup-Venv {
    param (
        [string]$venvPath = ".\venv"
    )
    
    try {
        if (-not (Test-Path $venvPath)) {
            Write-Host "Creating virtual environment..." -ForegroundColor Cyan
            python -m venv $venvPath
        }
        
        Write-Host "Activating virtual environment..." -ForegroundColor Cyan
        & "$venvPath\Scripts\Activate.ps1"
        
        Write-Host "Virtual environment activated" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Failed to setup virtual environment: $_" -ForegroundColor Red
        return $false
    }
}

# Install dependencies
function Install-Dependencies {
    param (
        [string]$requirementsFile = ".\food_analysis_api\requirements.txt"
    )
    
    try {
        if (-not (Test-Path $requirementsFile)) {
            throw "requirements.txt not found"
        }
        
        Write-Host "Installing dependencies..." -ForegroundColor Cyan
        pip install -r $requirementsFile
        
        Write-Host "Dependencies installed" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Failed to install dependencies: $_" -ForegroundColor Red
        return $false
    }
}

# Start FastAPI server
function Start-Server {
    try {
        Write-Host "`n=== Starting server ===" -ForegroundColor Magenta
        uvicorn food_analysis_api.main:app --reload
    }
    catch {
        Write-Host "Failed to start server: $_" -ForegroundColor Red
    }
}

# Main execution flow
Write-Host "`n=== food_analysis_api environment setup ===" -ForegroundColor Magenta

if (-not (Check-Python)) { exit 1 }
if (-not (Setup-Venv)) { exit 1 }
if (-not (Install-Dependencies)) { exit 1 }

Start-Server