# ADR 0003 — Configuracao centralizada e validada na inicializacao

**Status:** aceito
**Data:** 2026-09-29

## Contexto
As variaveis de ambiente eram lidas com `os.getenv` em seis arquivos diferentes,
cada um com seu `load_dotenv()`. Nenhum deles verificava se o valor existia.

Consequencia medida: sem `USER_JWT_SECRET`, a API subia normalmente e so quebrava
no primeiro login, com erro 500 (`TypeError: Expected a string value`). Em producao,
um secret esquecido no GitHub gerava um deploy verde e uma API quebrada.

## Decisao
Toda a configuracao passa por `src/config/settings.py`, com `pydantic-settings`:

- `DatabaseSettings`: so o banco. Usada pela aplicacao e pelo Alembic, para que as
  migracoes nao dependam de segredos da aplicacao.
- `Settings`: a configuracao completa, validada uma vez quando a API sobe. Faltou algo
  obrigatorio, a API recusa a inicializacao e o erro diz o que falta.
- Regras: `USER_JWT_SECRET` obrigatorio com no minimo 16 caracteres; em producao,
  `CLIENT_URL` nao pode apontar para localhost; variavel vazia conta como ausente.
- Segredos sao `SecretStr` e as mensagens de erro nunca mostram valores
  (`hide_input_in_errors`).
- `HMAC_SECRET_KEY` e SendGrid sao opcionais: nenhuma rota ativa os usa. Quem chamar
  esses recursos sem configurar recebe um erro explicito na hora do uso.

## Alternativas consideradas
- Manter `os.getenv` e verificar manualmente cada variavel — repete a verificacao em
  cada arquivo e depende de ninguem esquecer.
- Tudo numa unica classe — as migracoes passariam a exigir o segredo do JWT.

## Consequencias
- Configuracao incompleta aparece no deploy (a verificacao final falha), nao no
  primeiro usuario.
- Codigo novo nunca usa `os.getenv`: usa `get_settings()`.
- Descoberto na validacao: sem `hide_input_in_errors`, o erro de validacao imprimia o
  final do segredo do JWT. O deploy copia esse log para o GitHub Actions, que so
  mascara o segredo quando ele aparece inteiro.
