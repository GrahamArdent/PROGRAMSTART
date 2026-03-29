<#
.SYNOPSIS
    PROGRAMSTART convenience wrapper.
.DESCRIPTION
    Quick access to PROGRAMSTART workflow scripts.
    Usage:  .\pb.ps1 <command> [arguments]
.EXAMPLE
    .\pb.ps1 status
    .\pb.ps1 status --system programbuild
    .\pb.ps1 validate
    .\pb.ps1 validate --check metadata
    .\pb.ps1 state show
    .\pb.ps1 advance --system programbuild
    .\pb.ps1 progress
    .\pb.ps1 guide --kickoff
    .\pb.ps1 drift
    .\pb.ps1 drift PROGRAMBUILD/ARCHITECTURE.md PROGRAMBUILD/REQUIREMENTS.md
    .\pb.ps1 bootstrap --dest C:\Projects\NewApp --project-name NewApp --variant product
    .\pb.ps1 refresh --date 2026-03-27
    .\pb.ps1 dashboard
#>

param(
    [Parameter(Position = 0)]
    [string]$Command = "help",

    [Parameter(Position = 1, ValueFromRemainingArguments)]
    [string[]]$Arguments
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot = Split-Path -Parent $scriptDir
$venvPython = Join-Path $repoRoot ".venv/Scripts/python.exe"

Push-Location $repoRoot
try {
    if (Test-Path $venvPython) {
        & $venvPython -m scripts.programstart_cli $Command @Arguments
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python -m scripts.programstart_cli $Command @Arguments
    }
    elseif (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 -m scripts.programstart_cli $Command @Arguments
    }
    else {
        throw "Python interpreter not found. Run 'uv sync --extra dev' or install Python 3.12+."
    }

    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
