# ADR 0001 — PostgreSQL como banco padrao e Testcontainers nos testes de integracao

**Status:** aceito
**Data:** 2026-09-29

## Contexto
O template usava MySQL. A cartilha de DevWeb e o projeto piloto que a originou
usam PostgreSQL de ponta a ponta: banco local, testes de integracao e servidor
de producao. Manter bancos diferentes entre template e cartilha geraria
instrucoes contraditorias para os consultores.

Os testes de integracao precisam de um banco real que nao dependa do servidor
de producao nem de instalacao manual na maquina de cada consultor.

## Decisao
PostgreSQL 16 em todos os ambientes, com o driver `psycopg` (versao 3).
Testes de integracao sobem um PostgreSQL descartavel via Testcontainers.

## Alternativas consideradas
- Manter MySQL — exigiria reescrever a cartilha e divergiria do piloto ja validado.
- Banco em memoria (SQLite) nos testes — mais rapido, mas com dialeto SQL diferente
  do de producao: um teste pode passar e o mesmo codigo falhar no PostgreSQL.

## Consequencias
- Testes de integracao exigem Docker rodando na maquina e no runner do CI (que ja tem).
- A migracao inicial herdada do template usa apenas tipos genericos do SQLAlchemy
  e roda sem alteracao no PostgreSQL.
- Quem precisar rodar os testes sem Docker pode apontar `TEST_DATABASE_URL` para um
  PostgreSQL existente.
