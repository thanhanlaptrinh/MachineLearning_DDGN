$ErrorActionPreference = 'Stop'
Push-Location (Join-Path $PSScriptRoot '..')
try {
    if (-not (Test-Path '.venv\Scripts\python.exe')) { throw 'Chua cai moi truong. Xem README.md' }
    & '.\.venv\Scripts\python.exe' 'scripts/start_demo.py'
    if ($LASTEXITCODE -ne 0) { throw 'Demo da dung do loi. Xem thong bao phia tren.' }
} finally { Pop-Location }
