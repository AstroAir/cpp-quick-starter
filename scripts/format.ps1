<#
.SYNOPSIS
    Cross-platform code formatting script.
.DESCRIPTION
    Formats C++ source files using clang-format.
.PARAMETER Check
    Check formatting without modifying files (exit 1 if changes needed)
.PARAMETER Verbose
    Show files being processed
.EXAMPLE
    .\format.ps1
    .\format.ps1 -Check
#>

param(
    [switch]$Check,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot

# Check for clang-format
$clangFormat = Get-Command clang-format -ErrorAction SilentlyContinue
if (-not $clangFormat) {
    Write-Host "Error: clang-format not found in PATH" -ForegroundColor Red
    Write-Host "Install clang-format or add it to PATH" -ForegroundColor Yellow
    exit 1
}

Write-Host "Using: $($clangFormat.Source)" -ForegroundColor Cyan

# Find source files
$extensions = @("*.cpp", "*.hpp", "*.h", "*.cc", "*.cxx", "*.hxx")
$directories = @("include", "src", "tests", "benchmarks", "examples")

$files = @()
foreach ($dir in $directories) {
    $dirPath = Join-Path $ProjectRoot $dir
    if (Test-Path $dirPath) {
        foreach ($ext in $extensions) {
            $files += Get-ChildItem -Path $dirPath -Filter $ext -Recurse -File
        }
    }
}

if ($files.Count -eq 0) {
    Write-Host "No source files found" -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($files.Count) files to format" -ForegroundColor Cyan

$hasChanges = $false
$formatArgs = @("-style=file")

if ($Check) {
    $formatArgs += "--dry-run"
    $formatArgs += "--Werror"

    foreach ($file in $files) {
        if ($Verbose) {
            Write-Host "  Checking: $($file.Name)"
        }
        $output = & clang-format $formatArgs $file.FullName 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  Needs formatting: $($file.FullName)" -ForegroundColor Yellow
            $hasChanges = $true
        }
    }

    if ($hasChanges) {
        Write-Host "`nSome files need formatting. Run: .\scripts\format.ps1" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "`nAll files are properly formatted" -ForegroundColor Green
    }
} else {
    $formatArgs += "-i"
    foreach ($file in $files) {
        if ($Verbose) {
            Write-Host "  Formatting: $($file.Name)"
        }
        & clang-format $formatArgs $file.FullName
    }
    Write-Host "`nFormatted $($files.Count) files" -ForegroundColor Green
}
