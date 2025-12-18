<#
.SYNOPSIS
    Cross-platform build script for cpp-quick-starter.
.DESCRIPTION
    Configures and builds the project using CMake presets or manual configuration.
.PARAMETER Preset
    CMake preset to use (default: ninja-debug on Unix, vs-debug on Windows)
.PARAMETER Clean
    Clean build directory before building
.PARAMETER Target
    Specific target to build
.PARAMETER Jobs
    Number of parallel jobs
.EXAMPLE
    .\build.ps1
    .\build.ps1 -Preset ninja-release
    .\build.ps1 -Clean -Target unit_tests
#>

param(
    [string]$Preset,
    [switch]$Clean,
    [string]$Target,
    [int]$Jobs = 0
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot

# Determine default preset based on platform
if (-not $Preset) {
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        # Check if Ninja is available
        if (Get-Command ninja -ErrorAction SilentlyContinue) {
            $Preset = "ninja-debug"
        } else {
            $Preset = "vs-debug"
        }
    } else {
        $Preset = "ninja-debug"
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Building with preset: $Preset" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Clean if requested
if ($Clean) {
    $BuildDir = Join-Path $ProjectRoot "build"
    if (Test-Path $BuildDir) {
        Write-Host "Cleaning build directory..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $BuildDir
    }
}

# Configure
Write-Host "`nConfiguring..." -ForegroundColor Green
$configArgs = @("--preset", $Preset)
& cmake $configArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "Configuration failed!" -ForegroundColor Red
    exit 1
}

# Build
Write-Host "`nBuilding..." -ForegroundColor Green
$buildArgs = @("--build", "--preset", $Preset)
if ($Target) {
    $buildArgs += "--target"
    $buildArgs += $Target
}
if ($Jobs -gt 0) {
    $buildArgs += "-j"
    $buildArgs += $Jobs
}

& cmake $buildArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`nBuild completed successfully!" -ForegroundColor Green
