from app.db.connection import Connection


def get_db_session():
    connection = Connection()
    try:
        session = connection.get_session()
        yield session
    finally:
        session.close()
