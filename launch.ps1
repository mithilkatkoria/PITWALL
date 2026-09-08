$projectRoot = $PSScriptRoot
$shortRuntime = Join-Path $env:TEMP 'pitwall-0460-venv\Scripts\python.exe'
$localRuntime = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (Test-Path -LiteralPath $shortRuntime) {
    & $shortRuntime (Join-Path $projectRoot 'main.py')
} elseif (Test-Path -LiteralPath $localRuntime) {
    & $localRuntime (Join-Path $projectRoot 'main.py')
} else {
    Write-Error 'Python environment missing. See README.md setup instructions.'
}
