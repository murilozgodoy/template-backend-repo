from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.user_repository import UserRepository
from use_cases.user.auth.reset_pwd.reset_pwd_dto import ResetPwdDTO
from use_cases.user.auth.reset_pwd.reset_pwd_use_case import ResetPwdUseCase

router = APIRouter()


@router.post("/user/auth/reset/pwd")
def reset_pwd(
    reset_pwd_dto: ResetPwdDTO, response: Response, request: Request, db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    reset_pwd_use_case = ResetPwdUseCase(user_repository)
    return reset_pwd_use_case.execute(reset_pwd_dto, response, request)
