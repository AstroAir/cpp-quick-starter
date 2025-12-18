<#
.SYNOPSIS
    Cross-platform test runner script.
.DESCRIPTION
    Builds and runs tests using CTest.
.PARAMETER Preset
    CMake preset to use
.PARAMETER Filter
    Test name filter pattern
.PARAMETER Verbose
    Show verbose test output
.PARAMETER Build
    Build before running tests
.EXAMPLE
    .\test.ps1
    .\test.ps1 -Filter "unit*" -Verbose
    .\test.ps1 -Preset ninja-release -Build
#>

param(
    [string]$Preset,
    [string]$Filter,
    [switch]$Verbose,
    [switch]$Build
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot

# Determine default preset
if (-not $Preset) {
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
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
Write-Host "  Running tests with preset: $Preset" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Build if requested
if ($Build) {
    Write-Host "`nBuilding..." -ForegroundColor Green
    & cmake --preset $Preset
    & cmake --build --preset $Preset
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Build failed!" -ForegroundColor Red
        exit 1
    }
}

# Run tests
Write-Host "`nRunning tests..." -ForegroundColor Green
$testArgs = @("--preset", $Preset, "--output-on-failure")

if ($Verbose) {
    $testArgs += "--verbose"
}

if ($Filter) {
    $testArgs += "-R"
    $testArgs += $Filter
}

& ctest $testArgs
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "`nAll tests passed!" -ForegroundColor Green
} else {
    Write-Host "`nSome tests failed!" -ForegroundColor Red
}

exit $exitCode
