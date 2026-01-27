<#
.SYNOPSIS
    Cross-platform setup and dependency check script.
.DESCRIPTION
    Checks for required and optional tools, helps set up the development environment.
.PARAMETER Install
    Attempt to install missing tools (requires package manager)
.PARAMETER Verbose
    Show detailed information about each tool
.EXAMPLE
    .\setup.ps1
    .\setup.ps1 -Verbose
#>

param(
    [switch]$Install,
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  cpp-quick-starter Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Tool checking function
function Test-Tool {
    param(
        [string]$Name,
        [string]$Command = $Name,
        [string]$VersionArg = "--version",
        [switch]$Required
    )

    $tool = Get-Command $Command -ErrorAction SilentlyContinue
    $status = if ($tool) { "OK" } else { "Missing" }
    $color = if ($tool) { "Green" } elseif ($Required) { "Red" } else { "Yellow" }
    $reqText = if ($Required) { "[Required]" } else { "[Optional]" }

    if ($tool) {
        Write-Host "  [OK] " -ForegroundColor Green -NoNewline
        Write-Host "$Name " -NoNewline
        if ($Verbose) {
            try {
                $version = & $Command $VersionArg 2>&1 | Select-Object -First 1
                Write-Host "- $version" -ForegroundColor DarkGray
            } catch {
                Write-Host ""
            }
        } else {
            Write-Host ""
        }
        return $true
    } else {
        $marker = if ($Required) { "[MISSING]" } else { "[missing]" }
        Write-Host "  $marker " -ForegroundColor $color -NoNewline
        Write-Host "$Name $reqText" -ForegroundColor $color
        return $false
    }
}

# Check OS
Write-Host "System Information:" -ForegroundColor Yellow
Write-Host "  OS: $([System.Environment]::OSVersion.VersionString)"
Write-Host "  PowerShell: $($PSVersionTable.PSVersion)"
Write-Host ""

# Required tools
Write-Host "Required Tools:" -ForegroundColor Yellow
$allRequired = $true
$allRequired = (Test-Tool -Name "CMake" -Command "cmake" -Required) -and $allRequired
$allRequired = (Test-Tool -Name "C++ Compiler" -Command "cl" -VersionArg "" -Required:$false) -or `
              (Test-Tool -Name "C++ Compiler" -Command "g++" -Required:$false) -or `
              (Test-Tool -Name "C++ Compiler" -Command "clang++" -Required:$false)

if (-not $allRequired) {
    Write-Host "`n  A C++ compiler is required (MSVC cl, g++, or clang++)" -ForegroundColor Red
}

# Build tools
Write-Host "`nBuild Tools:" -ForegroundColor Yellow
Test-Tool -Name "Ninja" -Command "ninja" | Out-Null
Test-Tool -Name "xmake" -Command "xmake" | Out-Null
Test-Tool -Name "Make" -Command "make" | Out-Null

# Package managers
Write-Host "`nPackage Managers:" -ForegroundColor Yellow
Test-Tool -Name "vcpkg" -Command "vcpkg" | Out-Null
Test-Tool -Name "Conan" -Command "conan" | Out-Null

# Code quality
Write-Host "`nCode Quality Tools:" -ForegroundColor Yellow
Test-Tool -Name "clang-format" -Command "clang-format" | Out-Null
Test-Tool -Name "clang-tidy" -Command "clang-tidy" | Out-Null
Test-Tool -Name "cppcheck" -Command "cppcheck" | Out-Null

# Documentation
Write-Host "`nDocumentation Tools:" -ForegroundColor Yellow
Test-Tool -Name "Doxygen" -Command "doxygen" | Out-Null
Test-Tool -Name "MkDocs" -Command "mkdocs" | Out-Null
Test-Tool -Name "Python" -Command "python" -VersionArg "--version" | Out-Null
Test-Tool -Name "uv" -Command "uv" | Out-Null

# Git
Write-Host "`nVersion Control:" -ForegroundColor Yellow
Test-Tool -Name "Git" -Command "git" -Required | Out-Null
Test-Tool -Name "pre-commit" -Command "pre-commit" | Out-Null

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allRequired) {
    Write-Host "  All required tools are available!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Quick Start:" -ForegroundColor Yellow
    Write-Host "  cmake --preset ninja-debug"
    Write-Host "  cmake --build --preset ninja-debug"
    Write-Host "  ctest --preset ninja-debug"
} else {
    Write-Host "  Some required tools are missing!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installation suggestions:" -ForegroundColor Yellow
    Write-Host "  Windows: Install Visual Studio with C++ workload"
    Write-Host "           or use winget/scoop/chocolatey"
    Write-Host "  Linux:   sudo apt install build-essential cmake ninja-build"
    Write-Host "  macOS:   xcode-select --install && brew install cmake ninja"
}

Write-Host "========================================" -ForegroundColor Cyan
