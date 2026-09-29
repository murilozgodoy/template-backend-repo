from fastapi import APIRouter, Depends, Request, Response

from middlewares.validate_user_auth_token import validate_user_auth_token
from use_cases.user.auth.check_session_validity.check_session_validity_use_case import (
    CheckSessionValidityUseCase,
)

router = APIRouter()
check_session_validity_use_case = CheckSessionValidityUseCase()


@router.post("/user/auth/check/token", dependencies=[Depends(validate_user_auth_token)])
def check_session_validity(response: Response, request: Request):
    return check_session_validity_use_case.execute(response, request)
