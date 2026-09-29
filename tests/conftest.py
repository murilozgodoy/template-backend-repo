import os

# Configuracao ficticia para os testes. Definida antes de qualquer import da
# aplicacao; um .env local nao sobrescreve estes valores.
os.environ.setdefault("USER_JWT_SECRET", "segredo-de-teste-com-tamanho-suficiente")
os.environ.setdefault("HMAC_SECRET_KEY", "hmac-de-teste")
os.environ.setdefault("SENDGRID_API_KEY", "sendgrid-de-teste")
os.environ.setdefault("CLIENT_URL", "http://localhost:5173")
