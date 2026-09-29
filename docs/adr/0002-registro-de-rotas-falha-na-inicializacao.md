# ADR 0002 — Registro automatico de rotas falha alto na inicializacao

**Status:** aceito
**Data:** 2026-09-29

## Contexto
O `src/app.py` registra automaticamente todo `index.py` encontrado em `use_cases/`.
Na versao anterior, um erro ao importar um desses arquivos era capturado e apenas
impresso no console, e a API subia sem aquela rota.

Seguindo o README antigo (subir `src.app:app` a partir da raiz), nenhuma rota de
negocio era registrada: todas falhavam no import, em silencio. Em producao, o
container subiria respondendo so em `/`, com aparencia saudavel.

## Decisao
1. `src/app.py` adiciona a propria pasta ao `sys.path`, para que `src.app:app`
   funcione a partir da raiz.
2. Erros de import no registro de rotas nao sao mais capturados: a aplicacao
   falha na inicializacao, com o traceback completo.

## Alternativas consideradas
- Exigir `PYTHONPATH=src` em todo lugar — funciona, mas depende de todos lembrarem,
  e o erro continuaria silencioso para quem esquecesse.
- Converter todos os imports para `src.` — mudanca grande e espalhada pelo codigo.

## Consequencias
- Uma rota quebrada impede o deploy em vez de sumir: o erro aparece no CI
  (os testes de integracao importam o app) e no `docker logs`.
- Imports do projeto continuam sem o prefixo `src.`; misturar os dois estilos
  cria modulos duplicados (foi a causa de um bug no Alembic, ver `alembic/env.py`).
