from unittest.mock import MagicMock

from fastapi import Response

from use_cases.user.auth.login.login_dto import LoginDTO
from use_cases.user.auth.login.login_use_case import LoginUseCase


def test_login_com_email_inexistente_retorna_404(user_repository):
    user_repository.find_by_email.return_value = []
    response = Response()

    result = LoginUseCase(user_repository).execute(
        LoginDTO(email="naoexiste@example.com", password="qualquer"), response, MagicMock()
    )

    assert response.status_code == 404
    assert result["status"] == "error"


def test_login_com_senha_errada_retorna_400(user_repository, make_user):
    user_repository.find_by_email.return_value = [make_user(password="senha123")]
    response = Response()

    result = LoginUseCase(user_repository).execute(
        LoginDTO(email="joao@example.com", password="errada"), response, MagicMock()
    )

    assert response.status_code == 400
    assert result["status"] == "error"


def test_login_com_sucesso_define_cookie_e_retorna_202(user_repository, make_user):
    user_repository.find_by_email.return_value = [make_user(password="senha123")]
    response = Response()

    result = LoginUseCase(user_repository).execute(
        LoginDTO(email="joao@example.com", password="senha123"), response, MagicMock()
    )

    assert response.status_code == 202
    assert result["status"] == "success"
    assert "user_auth_token" in response.headers["set-cookie"]
