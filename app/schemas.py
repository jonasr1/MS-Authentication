import re
from pydantic import BaseModel, validator


class User(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, value):
        try:
            if not re.match('^([a-z]|[0-9]|@)+$', value):
                raise ValueError('O nome de usuário deve ter pelo menos um caractere e '
                                 'só pode conter letras minúsculas, números ou o símbolo `@`.')
            return value
        except TypeError:
            raise ValueError('O nome de usuário deve ser uma string')
        except Exception as e:
            raise ValueError(f"Erro ao validar o nome de usuário: {str(e)}")
