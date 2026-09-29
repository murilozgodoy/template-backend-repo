from functools import lru_cache

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Configuracao do banco, usada pela aplicacao e pelo Alembic.

    Separada da configuracao completa para que as migracoes nao dependam
    de segredos da aplicacao. Os valores padrao servem apenas para
    desenvolvimento local.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,  # variavel vazia conta como ausente
        hide_input_in_errors=True,  # erros de configuracao nunca mostram valores (segredos)
        extra="ignore",
    )

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "appdb"
    db_user: str = "usuario"
    db_password: SecretStr = SecretStr("senha")


class Settings(DatabaseSettings):
    """Configuracao completa da aplicacao.

    Lida uma unica vez, na inicializacao. Se algo obrigatorio faltar ou
    estiver invalido, a API nao sobe e o erro lista exatamente o problema.
    Segredos sao SecretStr: aparecem como '**********' em logs e prints;
    o valor real so sai com .get_secret_value().
    """

    environment: str = "dev"
    client_url: str = "http://localhost:5173"

    # Obrigatorio
    user_jwt_secret: SecretStr = Field(min_length=16)

    # Opcionais: so necessarios quando o projeto usar o recurso
    hmac_secret_key: SecretStr | None = None
    sendgrid_api_key: SecretStr | None = None
    sendgrid_from_email: str = "noreply@example.com"

    @model_validator(mode="after")
    def client_url_de_producao(self):
        if self.environment == "prod" and "localhost" in self.client_url:
            raise ValueError("CLIENT_URL precisa apontar para o front-end em producao")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
