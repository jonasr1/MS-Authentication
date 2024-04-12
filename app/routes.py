from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.depends import get_db_session
from app.auth_user import UserUseCases
from app.schemas import User

route = APIRouter(prefix='/user')


@route.post('/resgister/api/v1/authetication/token/')
def user_register(user: User, db_session: Session = Depends(get_db_session)):
    user_case = UserUseCases(db_session=db_session)
    user_case.user_register(user=user)
    return Response(content={'msg': 'success'}, status_code=status.HTTP_201_CREATED)
