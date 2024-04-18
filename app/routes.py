from decouple import config
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth_user import UserUseCases
from app.depends import get_db_session, token_verifier
from app.schemas import User

user_router = APIRouter()
# Essa dependência garante que todas as rotas dentro do 'test_router' tenha o método token_verifier
test_router = APIRouter(prefix='/test', dependencies=[Depends(token_verifier)])


LOGIN_URL = config('LOGIN_URL')  # Define a constante a partir da variável de ambiente .env


@user_router.post('/user/resgister/api/v1/')
def user_register(user: User, db_session: Session = Depends(get_db_session)):
    user_case = UserUseCases(db_session=db_session)
    user_case.user_register(user=user)
    return JSONResponse(content={'msg': 'success'}, status_code=status.HTTP_201_CREATED)


@user_router.post(LOGIN_URL)
def user_login(request_form_user: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db_session)):
    user_case = UserUseCases(db_session=db_session)
    user = User(username=request_form_user.username,
                password=request_form_user.password
                )
    auth_data = user_case.user_login(user=user)
    return JSONResponse(content=auth_data,
                        status_code=status.HTTP_200_OK
                        )


@user_router.post('/user/api/v1/authentication/validation/')
async def user_verify(request: Request, db_session: Session = Depends(get_db_session)):
    payload = await request.json()
    token = payload.get('token')

    user_case = UserUseCases(db_session=db_session)
    user_case.verify_token(access_token=token)

    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


@test_router.get('/api/v1/authentication/validation/')
def test_user_verify():
    return 'It works'
