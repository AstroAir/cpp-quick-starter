<#
.SYNOPSIS
    Cross-platform clean script for cpp-quick-starter.
.DESCRIPTION
    Removes build artifacts and generated files.
.PARAMETER All
    Remove all generated files including IDE caches
.PARAMETER BuildOnly
    Only remove build directory
.EXAMPLE
    .\clean.ps1
    .\clean.ps1 -All
#>

param(
    [switch]$All,
    [switch]$BuildOnly
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Cleaning project" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$dirsToRemove = @(
    "build"
)

if (-not $BuildOnly) {
    $dirsToRemove += @(
        ".xmake",
        ".cache"
    )
}

if ($All) {
    $dirsToRemove += @(
        ".vscode/.cache",
        ".idea"
    )
}

$filesToRemove = @(
    "compile_commands.json"
)

foreach ($dir in $dirsToRemove) {
    $dirPath = Join-Path $ProjectRoot $dir
    if (Test-Path $dirPath) {
        Write-Host "  Removing: $dir" -ForegroundColor Yellow
        Remove-Item -Recurse -Force $dirPath
    }
}

foreach ($file in $filesToRemove) {
    $filePath = Join-Path $ProjectRoot $file
    if (Test-Path $filePath) {
        Write-Host "  Removing: $file" -ForegroundColor Yellow
        Remove-Item -Force $filePath
    }
}

Write-Host "`nCleaned successfully!" -ForegroundColor Green
