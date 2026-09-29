from datetime import datetime
from unittest.mock import MagicMock

from fastapi import Response

from use_cases.user.auth.reset_pwd.reset_pwd_dto import ResetPwdDTO
from use_cases.user.auth.reset_pwd.reset_pwd_use_case import ResetPwdUseCase


def test_reset_com_token_inexistente_retorna_404(user_repository):
    user_repository.find_by_reset_pwd_token.return_value = []
    response = Response()

    result = ResetPwdUseCase(user_repository).execute(
        ResetPwdDTO(token="invalido", password="nova123"), response, MagicMock()
    )

    assert response.status_code == 404
    assert result["status"] == "error"


def test_reset_com_token_expirado_retorna_400(user_repository, make_user):
    duas_horas_atras = datetime.now().timestamp() - 7200
    user_repository.find_by_reset_pwd_token.return_value = [
        make_user(reset_pwd_token_sent_at=duas_horas_atras)
    ]
    response = Response()

    result = ResetPwdUseCase(user_repository).execute(
        ResetPwdDTO(token="token", password="nova123"), response, MagicMock()
    )

    assert response.status_code == 400
    assert result["status"] == "error"
    user_repository.update_pwd.assert_not_called()


def test_reset_com_sucesso_troca_senha_e_invalida_token(user_repository, make_user):
    dez_segundos_atras = datetime.now().timestamp() - 10
    user = make_user(reset_pwd_token_sent_at=dez_segundos_atras)
    user_repository.find_by_reset_pwd_token.return_value = [user]

    result = ResetPwdUseCase(user_repository).execute(
        ResetPwdDTO(token="token", password="nova123"), Response(), MagicMock()
    )

    assert result["status"] == "success"
    user_repository.update_pwd.assert_called_once_with(user.id, "nova123")
    user_repository.update_reset_pwd_token.assert_called_once_with(
        email=user.email, sent_at=0, token=""
    )
