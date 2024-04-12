from decouple import config
from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.models import UserModel


class Connection:
    def __init__(self):
        self.POSTGRES_DB = config('POSTGRES_DB')
        self.POSTGRES_USER = config('POSTGRES_USER')
        self.POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
        # Carregar as variáveis de ambiente
        self.DB_URL = config('DB_URL')

        self.DB_URL = f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost/{self.POSTGRES_DB}"

        self.engine = create_engine(self.DB_URL, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)

        self.metadata = MetaData()


    def create_database(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

    def create_user_table(self):
        # Carrega as informações do banco de dados existente
        self.metadata.reflect(bind=self.engine)
        if "users" not in self.metadata.tables:
            Base.metadata.create_all(bind=self.engine, tables=[UserModel.__table__])

    def get_session(self):
        return self.Session()
