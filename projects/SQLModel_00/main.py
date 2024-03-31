from fastapi import FastAPI, Depends
from models import Users
from schemas import UserCreate
from database import get_session

app = FastAPI()


@app.get("/users")
async def get_users(session=Depends(get_session)):
    return session.query(Users).all()
