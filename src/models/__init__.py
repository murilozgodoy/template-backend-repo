# Todo modelo novo PRECISA ser importado aqui.
# E este arquivo que o Alembic importa para descobrir as tabelas:
# um modelo ausente daqui nao entra nas migracoes.
from .user_model import UserModel

__all__ = ["UserModel"]
