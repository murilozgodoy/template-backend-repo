# Guia de Uso do Alembic

> **Duas regras que evitam os erros mais comuns**
>
> 1. Todo modelo novo precisa ser importado em `src/models/__init__.py`. Modelo fora dali não entra nas migrações.
> 2. Dentro de `src/`, importe sempre sem o prefixo `src.` (`from database.database import Base`). Misturar os dois estilos cria dois `Base` diferentes e o Alembic deixa de enxergar as tabelas.
>
> O banco usado pelos comandos vem das variáveis `DB_*` do `.env`. O CI roda `alembic check` a cada Pull Request: se um modelo mudou sem migração, o PR é barrado.

## O que é o Alembic?

Alembic é uma ferramenta de migração de banco de dados para SQLAlchemy. Ele permite versionar e gerenciar mudanças no esquema do banco de dados de forma controlada.

## Comandos Principais

### 1. Criar uma Nova Migração

Após alterar os modelos em `src/models/`, crie uma migração automática:

```bash
alembic revision --autogenerate -m "Descrição da alteração"
```

Exemplo:
```bash
alembic revision --autogenerate -m "Add phone field to users table"
```

### 2. Aplicar Migrações

Para aplicar todas as migrações pendentes:

```bash
alembic upgrade head
```

### 3. Reverter Migrações

Reverter a última migração:
```bash
alembic downgrade -1
```

Reverter para uma revisão específica:
```bash
alembic downgrade <revision_id>
```

Reverter todas as migrações:
```bash
alembic downgrade base
```

### 4. Ver Histórico de Migrações

Ver o histórico completo:
```bash
alembic history
```

Ver a revisão atual:
```bash
alembic current
```

### 5. Criar Migração Manual (Vazia)

Se precisar criar uma migração manualmente:
```bash
alembic revision -m "Descrição"
```

## Workflow Recomendado

### Adicionando um Novo Campo ao Modelo User

1. **Edite o modelo** (`src/models/user_model.py`):
```python
from sqlalchemy import Column, String

class UserModel(Base):
    # ... campos existentes ...
    phone = Column(String(20), nullable=True)  # Novo campo
```

2. **Crie a migração**:
```bash
alembic revision --autogenerate -m "Add phone field to users"
```

3. **Revise o arquivo de migração** gerado em `alembic/versions/`:
   - Verifique se o upgrade e downgrade estão corretos
   - Faça ajustes se necessário

4. **Aplique a migração**:
```bash
alembic upgrade head
```

### Criando uma Nova Tabela

1. **Crie o modelo** em `src/models/`:
```python
from sqlalchemy import Column, Integer, String
from database.database import Base  # sem o prefixo "src."

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
```

2. **Registre o modelo** em `src/models/__init__.py` (é esse arquivo que o Alembic lê):
```python
from .product_model import ProductModel
from .user_model import UserModel

__all__ = ["ProductModel", "UserModel"]
```

3. **Crie e aplique a migração**:
```bash
alembic revision --autogenerate -m "Create products table"
alembic upgrade head
```

## Estrutura de uma Migração

```python
"""Add phone field to users

Revision ID: abc123def456
Revises: previous_revision
Create Date: 2025-10-20 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abc123def456'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Mudanças a serem aplicadas
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))


def downgrade() -> None:
    # Como reverter as mudanças
    op.drop_column('users', 'phone')
```

## Dicas Importantes

### ✅ Boas Práticas

1. **Sempre revise** as migrações geradas automaticamente
2. **Teste** as migrações em ambiente de desenvolvimento primeiro
3. **Faça backup** do banco antes de aplicar migrações em produção
4. **Use mensagens descritivas** nas migrações
5. **Commit** os arquivos de migração no controle de versão

### ⚠️ Cuidados

1. **Nunca edite** migrações que já foram aplicadas em produção
2. **Não delete** arquivos de migração aplicados
3. **Cuidado com** operações destrutivas (drop table, drop column)
4. **Sempre implemente** tanto `upgrade()` quanto `downgrade()`

## Troubleshooting

### Erro: "Can't locate revision identified by 'xyz'"

Solução: Verifique se todos os arquivos de migração estão presentes em `alembic/versions/`

### Erro: "Target database is not up to date"

Solução: Execute `alembic upgrade head` para aplicar migrações pendentes

### Autogenerate não detecta mudanças

Possíveis causas:
- Modelo não foi importado em `src/models/__init__.py`
- Modelo importa `src.database.database` em vez de `database.database` (cria um segundo `Base`, invisível para o Alembic)
- Mudança não é detectável automaticamente (ex: índices, constraints)
- Base.metadata não está atualizado

### Resetar completamente o banco

```bash
# 1. Reverter todas as migrações
alembic downgrade base

# 2. Deletar o banco de dados
# docker exec -it postgres-local psql -U usuario -d postgres -c "DROP DATABASE appdb;"
# docker exec -it postgres-local psql -U usuario -d postgres -c "CREATE DATABASE appdb;"

# 3. Reaplicar todas as migrações
alembic upgrade head
```

## Integração com CI/CD

Para ambientes de produção, adicione ao seu pipeline:

```bash
# Verificar se há migrações pendentes
alembic current

# Aplicar migrações automaticamente
alembic upgrade head
```

## Referências

- [Documentação oficial do Alembic](https://alembic.sqlalchemy.org/)
- [Tutorial Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
