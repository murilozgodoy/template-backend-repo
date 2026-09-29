FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias primeiro: a camada so e refeita quando requirements.txt muda.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY alembic ./alembic
COPY src ./src

EXPOSE 8000

# As migracoes NAO rodam aqui: o deploy as aplica num container temporario
# antes de trocar a versao no ar (ver .github/workflows/deploy.yml).
# --host 0.0.0.0 e obrigatorio: sem ele, nada de fora do container alcanca a API.
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
