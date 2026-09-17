# Thin wrapper around GdUnit4's own addons/gdUnit4/runtest.cmd, which already knows how
# to invoke Godot correctly for headless test runs (see that script for why it uses
# --remote-debug instead of --headless directly). This script's only job is to load
# GODOT_BIN from the gitignored tools/local.env before delegating.
#
# Implements the `tests-red-then-green` / `contract-tests-pass` rows of
# rubrics/run-baseline.rubrics.md. Coverage reporting is NOT wired in yet — see
# dev_kit/ci/godot/README.md's "Not yet automated" section.

param(
    [string]$TestPath = "res://tests"
)

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")
$LocalEnv = Join-Path $RepoRoot "tools\local.env"

if (Test-Path $LocalEnv) {
    Get-Content $LocalEnv | ForEach-Object {
        if ($_ -match '^\s*([^#=]+)=(.*)$') {
            Set-Item -Path "Env:$($Matches[1].Trim())" -Value $Matches[2].Trim()
        }
    }
}

if (-not $env:GODOT_BIN) {
    Write-Error "GODOT_BIN is not set. Add it to tools/local.env (see dev_kit/ci/godot/README.md)."
    exit 1
}

$RunTestCmd = Join-Path $RepoRoot "addons\gdUnit4\runtest.cmd"
if (-not (Test-Path $RunTestCmd)) {
    Write-Error "GdUnit4 addon not found at addons/gdUnit4. Install it first (dev_kit/ci/godot/README.md, Phase 0.3)."
    exit 1
}

Push-Location $RepoRoot
try {
    & $RunTestCmd -a $TestPath -c
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
