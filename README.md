# Template Backend — FastAPI + PostgreSQL

Repositório-base de back-end dos projetos de DevWeb da Insper Júnior.
Todo projeto novo nasce daqui, pelo botão **Use this template** do Github, e já vem com:

- arquitetura em camadas (use cases, repositories, models, entities)
- autenticação de usuários com JWT (registro, login, sessão, recuperação de senha)
- migrações com Alembic
- configuração validada na inicialização: faltou um segredo, a API não sobe
- testes unitários e de integração, com cobertura mínima garantida pelo CI
- pre-commit com lint, formatação e testes
- Dockerfile e deploy automático na AWS EC2 via GitHub Actions

O passo a passo completo, com o porquê de cada decisão, está na **Cartilha DevWeb** do Núcleo de Inovação.

## Antes de iniciar

### Dê uma estrela e utilize o botão "Use this template" do repositório

1. **Dê uma estrela** neste repositório (Star).
2. **Use this template** do repositório para sua conta no GitHub. Isso criará esse repositório na sua conta.

## Começando um projeto

Requisitos: **Python 3.12 ou 3.13**, Git e Docker Desktop rodando. O template foi validado nas duas versões; a imagem de produção e o CI usam 3.13.

1. No GitHub: **Use this template → Create a new repository**.
2. Clone e rode o setup:

```bash
git clone https://github.com/<organizacao>/<projeto>.git
cd <projeto>
./setup.sh          # Git Bash, Mac, Linux
# .\setup.ps1       # PowerShell
```

3. Suba o banco local e a API:

```bash
docker network create -d bridge rede
docker run -d --name postgres-local --network rede \
  -e POSTGRES_DB=appdb -e POSTGRES_USER=usuario -e POSTGRES_PASSWORD=senha \
  -p 5432:5432 postgres:16

alembic upgrade head
uvicorn src.app:app --reload
```

A documentação interativa fica em **http://localhost:8000/docs**.

4. Preencha `docs/prd.md` antes da primeira sprint.
5. Cadastre os secrets do deploy (tabela abaixo) e ative a proteção da `main`.

## Comandos do dia a dia

| Tarefa | Comando |
| --- | --- |
| Subir a API | `uvicorn src.app:app --reload` |
| Todos os testes + cobertura geral (mín. 80%) | `pytest` |
| Só os unitários | `pytest tests/unit` |
| Gate dos use cases (100%) | `coverage report --include="src/use_cases/**/*_use_case.py" --fail-under=100` |
| Lint e formatação | `ruff check . && ruff format .` |
| Todas as verificações do pre-commit | `pre-commit run --all-files` |
| Nova migração | `alembic revision --autogenerate -m "descricao"` |
| Aplicar migrações | `alembic upgrade head` |
| Conferir se modelos e migrações batem | `alembic check` |

Os testes de integração sobem um PostgreSQL descartável com Testcontainers: **o Docker precisa estar rodando**. Sem Docker, aponte `TEST_DATABASE_URL` para um PostgreSQL existente.

## Estrutura

```
.
├── .github/
│   ├── workflows/ci.yml          testes, lint, migrações e cobertura a cada PR
│   ├── workflows/deploy.yml      build da imagem e deploy na EC2 a cada merge
│   └── pull_request_template.md
├── alembic/                      migrações (guia em ALEMBIC_GUIDE.md)
├── docs/
│   ├── prd.md                    requisitos do projeto
│   └── adr/                      registro de decisões de arquitetura
├── src/
│   ├── app.py                    aplicação e registro automático de rotas
│   ├── config/                   configuração lida do ambiente
│   ├── database/                 conexão e get_db()
│   ├── entities/                 entidades Pydantic
│   ├── middlewares/              validação do token de autenticação
│   ├── models/                   modelos SQLAlchemy (registre todos no __init__.py)
│   ├── repositories/             acesso a dados
│   ├── use_cases/                regras de negócio, uma pasta por caso de uso
│   └── utils/
├── tests/
│   ├── unit/                     use cases e utils, com mocks
│   └── integration/              rotas contra PostgreSQL real
├── Dockerfile
├── pyproject.toml                pytest, cobertura e ruff
├── requirements.txt              dependências de produção
└── requirements-dev.txt          dependências de teste e qualidade
```

### Criando um caso de uso

Cada caso de uso é uma pasta em `src/use_cases/` com três arquivos:

| Arquivo | Papel |
| --- | --- |
| `index.py` | a rota (`router = APIRouter()`); registrada automaticamente pelo `app.py` |
| `<nome>_dto.py` | o formato de entrada, em Pydantic |
| `<nome>_use_case.py` | a regra de negócio — **exige 100% de cobertura** |

Dentro de `src/`, importe sempre sem o prefixo `src.` (`from database.database import get_db`).

## Variáveis de ambiente

Toda a configuração é lida e validada em `src/config/settings.py`. Código novo usa `get_settings()`, nunca `os.getenv`.

Local: copie `.env.example` para `.env`. Produção: GitHub **Settings → Secrets and variables → Actions**.

| Nome | Onde cadastrar | Obrigatória | Uso |
| --- | --- | --- | --- |
| `DOCKERHUB_TOKEN` | Secrets | sim | publicar a imagem |
| `EC2_HOST` | Secrets | sim | IP do servidor |
| `EC2_SSH_KEY` | Secrets | sim | conteúdo inteiro do `.pem` |
| `DB_USER` | Secrets | sim | usuário do PostgreSQL de produção |
| `DB_PASSWORD` | Secrets | sim | senha do PostgreSQL de produção |
| `USER_JWT_SECRET` | Secrets | sim | assinatura dos tokens de login (mínimo 16 caracteres) |
| `HMAC_SECRET_KEY` | Secrets | quando usar | hashes HMAC |
| `SENDGRID_API_KEY` | Secrets | quando usar | envio de email |
| `DOCKERHUB_USERNAME` | Variables | sim | usuário do Docker Hub; sem ela o deploy nem roda |
| `DB_HOST` | Variables | sim | nome do container do banco (`postgres`) |
| `DB_PORT` | Variables | sim | `5432` |
| `DB_NAME` | Variables | sim | nome do banco |
| `CLIENT_URL` | Variables | sim | URL do front-end; único origin liberado no CORS |
| `SENDGRID_FROM_EMAIL` | Variables | quando usar | remetente dos emails |

Faltando uma obrigatória, a API recusa a inicialização e o deploy fica vermelho mostrando o motivo.

### Como o deploy funciona

A imagem é publicada como `<DOCKERHUB_USERNAME>/<nome-do-repositório>`. Na EC2, o deploy:

1. baixa a imagem nova, com a versão antiga ainda no ar;
2. aplica as migrações num container temporário — se falhar, para aqui e nada muda;
3. troca o container `app` (porta 8000);
4. confere se a API respondeu; se não, marca o deploy como falho e mostra o log.

Detalhes e riscos em `docs/adr/0004-migracoes-antes-da-troca-de-versao.md`.

## Decisões de arquitetura

Registradas em `docs/adr/`. Leia antes de mudar algo estrutural; para uma decisão nova, copie `docs/adr/0000-modelo.md`.
