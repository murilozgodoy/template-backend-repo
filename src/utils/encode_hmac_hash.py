import hashlib
import hmac

from config.settings import get_settings


def encode_hmac_hash(data: str) -> str:
    key = get_settings().hmac_secret_key
    if key is None:
        raise RuntimeError("HMAC_SECRET_KEY nao configurado")
    return hmac.new(
        key.get_secret_value().encode("utf-8"), data.encode("utf-8"), hashlib.sha256
    ).hexdigest()
