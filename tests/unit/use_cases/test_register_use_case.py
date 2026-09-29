from unittest.mock import MagicMock

from fastapi import Response

from use_cases.user.auth.register.register_dto import RegisterDTO
from use_cases.user.auth.register.register_use_case import RegisterUseCase


def test_registro_com_campo_vazio_retorna_406(user_repository):
    response = Response()

    result = RegisterUseCase(user_repository).execute(
        RegisterDTO(name="", email="joao@example.com", password="senha123"), response, MagicMock()
    )

    assert response.status_code == 406
    assert result["status"] == "error"
    user_repository.save.assert_not_called()


def test_registro_com_email_ja_cadastrado_retorna_409(user_repository, make_user):
    user_repository.find_by_email.return_value = [make_user()]
    response = Response()

    result = RegisterUseCase(user_repository).execute(
        RegisterDTO(name="Joao", email="joao@example.com", password="senha123"),
        response,
        MagicMock(),
    )

    assert response.status_code == 409
    assert result["status"] == "error"
    user_repository.save.assert_not_called()


def test_registro_com_sucesso_salva_e_retorna_201(user_repository):
    user_repository.find_by_email.return_value = []
    response = Response()

    result = RegisterUseCase(user_repository).execute(
        RegisterDTO(name="Joao", email="joao@example.com", password="senha123"),
        response,
        MagicMock(),
    )

    assert response.status_code == 201
    assert result["status"] == "success"
    user_repository.save.assert_called_once()
