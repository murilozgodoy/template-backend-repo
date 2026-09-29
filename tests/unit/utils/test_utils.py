import base64
from unittest.mock import MagicMock, patch

import pytest

from utils.encode_hmac_hash import encode_hmac_hash
from utils.generate_random_pwd import generate_random_password
from utils.send_email import send_email


def test_hmac_e_deterministico():
    assert encode_hmac_hash("dado") == encode_hmac_hash("dado")
    assert encode_hmac_hash("dado") != encode_hmac_hash("outro")


def test_senha_aleatoria_tem_o_tamanho_pedido():
    senha = base64.b64decode(generate_random_password(length=16)).decode()

    assert len(senha) == 16


@patch("utils.send_email.SendGridAPIClient")
def test_send_email_devolve_a_resposta_do_sendgrid(sendgrid_client):
    sendgrid_client.return_value.send.return_value = MagicMock(status_code=202, body="", headers={})

    result = send_email(email="joao@example.com", content="<p>oi</p>", subject="Teste")

    assert result["status_code"] == 202


@patch("utils.send_email.SendGridAPIClient")
def test_send_email_propaga_erro_do_sendgrid(sendgrid_client):
    sendgrid_client.return_value.send.side_effect = RuntimeError("falha")

    with pytest.raises(RuntimeError):
        send_email(email="joao@example.com", content="<p>oi</p>", subject="Teste")


@patch("utils.encode_hmac_hash.get_settings")
def test_hmac_sem_chave_configurada_falha_com_mensagem_clara(get_settings):
    get_settings.return_value = MagicMock(hmac_secret_key=None)

    with pytest.raises(RuntimeError, match="HMAC_SECRET_KEY"):
        encode_hmac_hash("dado")


@patch("utils.send_email.get_settings")
def test_send_email_sem_chave_configurada_falha_com_mensagem_clara(get_settings):
    get_settings.return_value = MagicMock(sendgrid_api_key=None)

    with pytest.raises(RuntimeError, match="SENDGRID_API_KEY"):
        send_email(email="joao@example.com", content="<p>oi</p>", subject="Teste")
