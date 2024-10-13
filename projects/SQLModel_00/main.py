from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List
from models import Users
from schemas import UserCreate
from projects.car_info_viewer.database import get_session

app = FastAPI()


# Create a user
@app.post("/users/", response_model=Users)
def create_user(user_create: UserCreate, session=Depends(get_session)):
    user = Users(name=user_create.name, email=user_create.email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Get all users
@app.get("/users/", response_model=List[Users])
def get_users(session=Depends(get_session)):
    return session.query(Users).all()


# # Get a user by ID
# @app.get("/users/{user_id}", response_model=Users)
# def get_user(user_id: int, session=Depends(get_session)):
#     user = session.get(Users, user_id)
#     if user:
#         return user
#     else:
#         raise HTTPException(status_code=404, detail="User not found")


# # Delete a user by ID
# @app.delete("/users/{user_id}", response_model=Users)
# def delete_user(user_id: int, session=Depends(get_session)):
#     user = session.get(Users, user_id)
#     if user:
#         session.delete(user)
#         session.commit()
#         return user
#     else:
#         raise HTTPException(status_code=404, detail="User not found")


# Get a user by ID
@app.get("/users/", response_model=Users)
def get_user(
    user_id: int = Query(..., description="ID of the user to retrieve"),
    session=Depends(get_session),
):
    user = session.get(Users, user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


# Delete a user by ID
@app.delete("/users/", response_model=Users)
def delete_user(
    user_id: int = Query(..., description="ID of the user to delete"),
    session=Depends(get_session),
):
    user = session.get(Users, user_id)
    if user:
        session.delete(user)
        session.commit()
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
