# Setup do projeto para PowerShell.

Write-Host "Criando ambiente virtual em .venv..." -ForegroundColor Yellow
python -m venv .venv

.\.venv\Scripts\Activate.ps1

Write-Host "Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt -r requirements-dev.txt

git rev-parse --git-dir 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Ativando o pre-commit..." -ForegroundColor Yellow
    pre-commit install
} else {
    Write-Host "AVISO: esta pasta ainda nao e um repositorio Git, entao o pre-commit nao foi ativado." -ForegroundColor Red
    Write-Host "       Depois do 'git init' (ou ao clonar do GitHub), rode: pre-commit install" -ForegroundColor Red
}

if (!(Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "Arquivo .env criado a partir do .env.example." -ForegroundColor Green
}

Write-Host "`nProximos passos:" -ForegroundColor Cyan
Write-Host "  1. Suba o PostgreSQL local (comando no README)"
Write-Host "  2. alembic upgrade head"
Write-Host "  3. uvicorn src.app:app --reload"
