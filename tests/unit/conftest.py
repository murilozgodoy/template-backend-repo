from unittest.mock import MagicMock

import bcrypt
import pytest


@pytest.fixture
def user_repository():
    """Repositorio falso: cada teste define o que ele devolve."""
    return MagicMock()


@pytest.fixture
def make_user():
    """Cria um usuario falso com a senha ja em hash, como vem do banco."""

    def _make_user(password="senha123", reset_pwd_token_sent_at=None):
        user = MagicMock()
        user.id = 1
        user.name = "Joao Silva"
        user.email = "joao@example.com"
        user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=4)).decode()
        user.reset_pwd_token_sent_at = reset_pwd_token_sent_at
        return user

    return _make_user
