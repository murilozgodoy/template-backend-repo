from datetime import datetime
from unittest.mock import MagicMock

from fastapi import Response

from use_cases.user.auth.send_pwd_recovery_email.send_pwd_recovery_email_dto import (
    SendPwdRecoveryEmailDTO,
)
from use_cases.user.auth.send_pwd_recovery_email.send_pwd_recovery_email_use_case import (
    SendPwdRecoveryEmailUseCase,
)


def test_recuperacao_com_email_inexistente_retorna_404(user_repository):
    user_repository.find_by_email.return_value = []
    response = Response()

    result = SendPwdRecoveryEmailUseCase(user_repository).execute(
        SendPwdRecoveryEmailDTO(email="naoexiste@example.com"), response, MagicMock()
    )

    assert response.status_code == 404
    assert result["status"] == "error"


def test_recuperacao_pedida_ha_menos_de_uma_hora_retorna_400(user_repository, make_user):
    dez_minutos_atras = datetime.now().timestamp() - 600
    user_repository.find_by_email.return_value = [
        make_user(reset_pwd_token_sent_at=dez_minutos_atras)
    ]
    response = Response()

    result = SendPwdRecoveryEmailUseCase(user_repository).execute(
        SendPwdRecoveryEmailDTO(email="joao@example.com"), response, MagicMock()
    )

    assert response.status_code == 400
    assert result["status"] == "error"
    user_repository.update_reset_pwd_token.assert_not_called()


def test_recuperacao_pela_primeira_vez_gera_token(user_repository, make_user):
    user_repository.find_by_email.return_value = [make_user(reset_pwd_token_sent_at=None)]
    response = Response()

    result = SendPwdRecoveryEmailUseCase(user_repository).execute(
        SendPwdRecoveryEmailDTO(email="joao@example.com"), response, MagicMock()
    )

    assert response.status_code == 200
    assert result["status"] == "success"
    user_repository.update_reset_pwd_token.assert_called_once()


def test_recuperacao_depois_de_uma_hora_gera_novo_token(user_repository, make_user):
    duas_horas_atras = datetime.now().timestamp() - 7200
    user_repository.find_by_email.return_value = [
        make_user(reset_pwd_token_sent_at=duas_horas_atras)
    ]
    response = Response()

    SendPwdRecoveryEmailUseCase(user_repository).execute(
        SendPwdRecoveryEmailDTO(email="joao@example.com"), response, MagicMock()
    )

    assert response.status_code == 200
    user_repository.update_reset_pwd_token.assert_called_once()
