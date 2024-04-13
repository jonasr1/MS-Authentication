from fastapi import FastAPI

from app.db.connection import Connection
from app.routes import router

app = FastAPI()

# {
#   "username": "joao",
#   "password": "joao123"
# }# {
#   "username": "jose",
#   "password": "12jose"
# }


@app.get('/')
def health_check():
    return "OK, it's working"


app.include_router(router)

if __name__ == "__main__":
    conn = Connection()
    conn.create_database()
    conn.create_user_table()
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)

