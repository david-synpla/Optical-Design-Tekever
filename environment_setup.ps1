$ErrorActionPreference = 'Stop'

$ProjectRoot = $PSScriptRoot
$Distro = 'Ubuntu'

if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
    throw 'wsl.exe is unavailable. Install WSL and Ubuntu before running this setup.'
}

$InstalledDistros = @(& wsl.exe --list --quiet) -replace "`0", ''
if ($InstalledDistros -notcontains $Distro) {
    throw "The $Distro WSL distribution is not installed."
}

$LinuxProjectRoot = (& wsl.exe -d $Distro -- wslpath -a -u $ProjectRoot).Trim()
if ($LASTEXITCODE -ne 0 -or -not $LinuxProjectRoot) {
    throw 'Could not translate the Windows project path for WSL.'
}

& wsl.exe -d $Distro -- bash "$LinuxProjectRoot/environment_setup_wsl.sh"
if ($LASTEXITCODE -ne 0) {
    throw "WSL environment setup failed with exit code $LASTEXITCODE."
}
