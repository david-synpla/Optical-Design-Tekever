$ErrorActionPreference = 'Stop'

$ProjectRoot = 'C:\Users\david\OneDrive - Synopsis Planet\Documents\ChatGPT\Optical Design - Tekever'
$VenvRoot = Join-Path $env:LOCALAPPDATA 'ChatGPTOptics\venvs\tekever'
$BundledPython = 'C:\Users\david\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'

Set-Location -LiteralPath $ProjectRoot
New-Item -ItemType Directory -Force -Path (Split-Path $VenvRoot) | Out-Null

if (-not (Test-Path $VenvRoot)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.12 -m venv $VenvRoot
    }
    elseif (Test-Path -LiteralPath $BundledPython) {
        & $BundledPython -m venv $VenvRoot
    }
    else {
        throw 'Python 3.12 was not found. Install it or restore the Codex bundled runtime.'
    }
}

$Python = Join-Path $VenvRoot 'Scripts\python.exe'
& $Python -m pip install --upgrade pip
& $Python -m pip install 'optiland==0.6.2' pyyaml pandas matplotlib pytest

$Python | Set-Content -Encoding ASCII 'python_path.txt'
& $Python -m pip freeze | Set-Content -Encoding ASCII 'requirements-lock.txt'
& $Python 'src\verify_env.py'

Write-Host ''
Write-Host 'Environment ready.'
Write-Host "Python: $Python"
