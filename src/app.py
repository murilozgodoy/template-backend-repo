import os
import sys
from glob import glob
from importlib import import_module

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Os modulos do projeto sao importados sem o prefixo "src."
# (ex.: "from database.database import get_db"). Colocar esta pasta no
# sys.path faz "uvicorn src.app:app" funcionar a partir da raiz do repositorio,
# que e como o Dockerfile e o README sobem a aplicacao.
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from config.settings import get_settings  # noqa: E402

# Valida toda a configuracao na inicializacao: se faltar algo obrigatorio
# (ex.: USER_JWT_SECRET), a API nao sobe e o erro diz o que falta.
settings = get_settings()

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "OK"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_url],  # so o front-end configurado em CLIENT_URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro automatico das rotas: todo arquivo index.py dentro de use_cases/
# que expoe um "router" vira um conjunto de rotas da API.
# Um erro de import aqui derruba a inicializacao de proposito: uma rota
# quebrada nao pode sumir em silencio e a API subir "saudavel" sem ela.
USE_CASES_DIR = os.path.join(SRC_DIR, "use_cases")
route_files = sorted(glob(os.path.join(USE_CASES_DIR, "**", "index.py"), recursive=True))

for route_file in route_files:
    relative_path = os.path.relpath(route_file, SRC_DIR)
    module_name = os.path.splitext(relative_path)[0].replace(os.path.sep, ".")
    module = import_module(module_name)
    if hasattr(module, "router"):
        app.include_router(module.router)
