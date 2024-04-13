from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.depends import get_db_session
from app.auth_user import UserUseCases
from app.schemas import User

router = APIRouter(prefix='/user')


@router.post('/api/v1/resgister/token/')
def user_register(user: User, db_session: Session = Depends(get_db_session)):
    user_case = UserUseCases(db_session=db_session)
    user_case.user_register(user=user)
    return JSONResponse(content={'msg': 'success'}, status_code=status.HTTP_201_CREATED)


@router.post('/login/api/v1/authetication/token/')
def user_login(request_form_user: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db_session)):
    user_case = UserUseCases(db_session=db_session)
    user = User(username=request_form_user.username,
                password=request_form_user.password
                )
    auth_data = user_case.user_login(user=user)
    return JSONResponse(content=auth_data,
                        status_code=status.HTTP_200_OK
                        )
