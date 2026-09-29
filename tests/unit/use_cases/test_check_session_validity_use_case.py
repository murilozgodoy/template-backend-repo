from unittest.mock import MagicMock

from fastapi import Response

from use_cases.user.auth.check_session_validity.check_session_validity_use_case import (
    CheckSessionValidityUseCase,
)


def test_sessao_valida_retorna_sucesso():
    result = CheckSessionValidityUseCase().execute(Response(), MagicMock())

    assert result["status"] == "success"
