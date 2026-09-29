#!/usr/bin/env bash
# Setup do projeto para Git Bash (Windows), Mac e Linux.
set -e

echo "Criando ambiente virtual em .venv..."
python -m venv .venv

if [ -f .venv/Scripts/activate ]; then
  source .venv/Scripts/activate   # Windows (Git Bash)
else
  source .venv/bin/activate       # Mac / Linux
fi

echo "Instalando dependencias..."
pip install -r requirements.txt -r requirements-dev.txt

if git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Ativando o pre-commit..."
  pre-commit install
else
  echo "AVISO: esta pasta ainda nao e um repositorio Git, entao o pre-commit nao foi ativado."
  echo "       Depois do 'git init' (ou ao clonar do GitHub), rode: pre-commit install"
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Arquivo .env criado a partir do .env.example."
fi

echo
echo "Proximos passos:"
echo "  1. Ative o ambiente: source .venv/Scripts/activate (Windows) ou source .venv/bin/activate"
echo "  2. Suba o PostgreSQL local (comando no README)"
echo "  3. alembic upgrade head"
echo "  4. uvicorn src.app:app --reload"
