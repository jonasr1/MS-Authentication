from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import UserModel
from app.schemas import User
from decouple import config
from passlib.context import CryptContext
from jose import jwt, JWTError

crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')


class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_register(self, user: User):
        user_model = UserModel(username=user.username, password=crypt_context.hash(user.password))
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists'
            )

    def user_login(self, user: User, expires_in: int = 30):  # 30 minutos
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first()
        if user_on_db is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Invalid username or password')

        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Invalid username or password')

        expirar = datetime.utcnow() + timedelta(minutes=expires_in) # Obtém o horário atual em UTC (padrão global)

        payload = {
            'sub': user.username,
            'expirar': expirar.isoformat()
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {'access_token': access_token,
                'expirar': expirar.isoformat()}
