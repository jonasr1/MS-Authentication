from decouple import config
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.connection import Connection
from app.auth_user import UserUseCases

LOGIN_URL = config('LOGIN_URL')  # Define a constante a partir da variável de ambiente .env

oauth_scheme = OAuth2PasswordBearer(tokenUrl=LOGIN_URL)  # Define o esquema de autenticação e onde buscar o token


def get_db_session():
    connection = Connection()
    try:
        session = connection.get_session()
        yield session  # garante que vai retorna e cair no finally
    finally:
        session.close()


def token_verifier(db_session: Session = Depends(get_db_session), token=Depends(oauth_scheme)):
    user_case = UserUseCases(db_session=db_session)              # Obtém o token ^^^^
    user_case.verify_token(access_token=token)

