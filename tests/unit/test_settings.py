import pytest
from pydantic import ValidationError

from config.settings import Settings


def test_sem_segredo_do_jwt_a_aplicacao_nao_sobe(monkeypatch):
    monkeypatch.delenv("USER_JWT_SECRET", raising=False)

    with pytest.raises(ValidationError, match="user_jwt_secret"):
        Settings(_env_file=None)


def test_segredo_do_jwt_curto_demais_e_rejeitado(monkeypatch):
    monkeypatch.setenv("USER_JWT_SECRET", "curto")

    with pytest.raises(ValidationError, match="user_jwt_secret"):
        Settings(_env_file=None)


def test_variavel_vazia_conta_como_ausente(monkeypatch):
    monkeypatch.setenv("CLIENT_URL", "")

    assert Settings(_env_file=None).client_url == "http://localhost:5173"


def test_producao_exige_a_url_real_do_front(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "prod")
    monkeypatch.setenv("CLIENT_URL", "http://localhost:5173")

    with pytest.raises(ValidationError, match="CLIENT_URL"):
        Settings(_env_file=None)


def test_producao_com_url_real_do_front_e_aceita(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "prod")
    monkeypatch.setenv("CLIENT_URL", "https://app.cliente.com.br")

    assert Settings(_env_file=None).client_url == "https://app.cliente.com.br"


def test_segredos_opcionais_podem_ficar_vazios(monkeypatch):
    monkeypatch.setenv("HMAC_SECRET_KEY", "")
    monkeypatch.setenv("SENDGRID_API_KEY", "")

    settings = Settings(_env_file=None)

    assert settings.hmac_secret_key is None
    assert settings.sendgrid_api_key is None


def test_erro_de_configuracao_nao_expoe_segredos(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "prod")
    monkeypatch.setenv("CLIENT_URL", "http://localhost:5173")
    monkeypatch.setenv("USER_JWT_SECRET", "segredo-que-nao-pode-vazar")
    monkeypatch.setenv("DB_PASSWORD", "senha-que-nao-pode-vazar")

    with pytest.raises(ValidationError) as erro:
        Settings(_env_file=None)

    assert "nao-pode-vazar" not in str(erro.value)


def test_segredos_nao_aparecem_ao_imprimir_as_configuracoes(monkeypatch):
    monkeypatch.setenv("USER_JWT_SECRET", "segredo-que-nao-pode-vazar")

    settings = Settings(_env_file=None)

    assert "nao-pode-vazar" not in repr(settings)
    assert settings.user_jwt_secret.get_secret_value() == "segredo-que-nao-pode-vazar"
