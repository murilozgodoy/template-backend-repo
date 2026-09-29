import bcrypt
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int | None = None
    name: str
    email: EmailStr
    password: str
    age: int | None = None
    is_active: bool = True
    reset_pwd_token: str | None = None
    reset_pwd_token_sent_at: float | None = None

    def hash_password(self) -> str:
        """Gera o hash da senha usando bcrypt"""
        return bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password_matches(self, plain_password: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return bcrypt.checkpw(plain_password.encode("utf-8"), self.password.encode("utf-8"))
