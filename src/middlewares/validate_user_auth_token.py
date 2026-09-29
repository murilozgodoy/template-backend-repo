import jwt
from fastapi import HTTPException, Request, Response

from config.settings import get_settings


def validate_user_auth_token(request: Request, response: Response):
    token = request.cookies.get("user_auth_token")

    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        payload = jwt.decode(
            token.split(" ")[1],
            get_settings().user_jwt_secret.get_secret_value(),
            algorithms=["HS256"],
        )

        user_id = payload.get("id")
        user_email = payload.get("email")
        request.state.auth_payload = {"user_id": user_id, "user_email": user_email}

    except (jwt.PyJWTError, IndexError):  # IndexError: cookie sem o prefixo "Bearer "
        response.delete_cookie("user_auth_token")

        raise HTTPException(status_code=401, detail="Invalid JWT token") from None

    return True
