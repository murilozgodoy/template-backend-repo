from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.user_repository import UserRepository
from use_cases.user.auth.send_pwd_recovery_email.send_pwd_recovery_email_dto import (
    SendPwdRecoveryEmailDTO,
)
from use_cases.user.auth.send_pwd_recovery_email.send_pwd_recovery_email_use_case import (
    SendPwdRecoveryEmailUseCase,
)

router = APIRouter()


@router.post("/user/auth/pwd/recovery/email")
def send_pwd_recovery_email_route(
    send_pwd_recovery_email_dto: SendPwdRecoveryEmailDTO,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    send_pwd_recovery_email_use_case = SendPwdRecoveryEmailUseCase(user_repository)
    return send_pwd_recovery_email_use_case.execute(send_pwd_recovery_email_dto, response, request)
