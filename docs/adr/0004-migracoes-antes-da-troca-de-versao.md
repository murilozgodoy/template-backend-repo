# ADR 0004 — Migracoes aplicadas antes da troca de versao no deploy

**Status:** aceito
**Data:** 2026-09-29

## Contexto
A primeira versao do Dockerfile aplicava as migracoes quando o container subia.
O deploy removia o container antigo e iniciava o novo. Se a migracao falhasse, o
novo container entrava em loop de reinicio e o antigo ja nao existia: a API ficava
fora do ar.

## Decisao
O script de deploy na EC2 segue quatro passos, com `set -e` (para no primeiro erro):

1. Baixa a imagem nova, com a versao antiga ainda no ar.
2. Aplica as migracoes num container temporario (`docker run --rm ... alembic upgrade head`).
   Se falhar, o deploy para e a versao antiga continua atendendo.
3. Troca o container `app`.
4. Consulta a API por ate 30 segundos. Sem resposta, imprime o log e marca o deploy como falho.

O Dockerfile so sobe a API.

## Alternativas consideradas
- Migrar ao subir o container — simples, mas uma migracao quebrada derruba a producao.
- Dois containers em paralelo com troca sem interrupcao — elimina a janela de indisponibilidade,
  mas exige proxy reverso; desproporcional para uma EC2 por projeto.

## Consequencias
- Migracao quebrada: deploy vermelho, producao intacta.
- Configuracao incompleta: a API recusa a inicializacao (ADR 0003), o passo 4 falha e o
  motivo aparece no log do deploy. Neste caso ha indisponibilidade, porque o container
  antigo ja foi removido; e o risco residual aceito.
- Migracoes precisam ser compativeis com a versao anterior do codigo, que continua no ar
  enquanto elas rodam (ex.: adicionar coluna, nao renomear).
- Rodar a imagem manualmente exige aplicar as migracoes antes (`alembic upgrade head`).
