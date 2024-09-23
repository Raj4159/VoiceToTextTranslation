from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from user_credential import load_users, save_users

router = APIRouter()  # Create an APIRouter instance

class User(BaseModel):
    username: str
    password: str

@router.post("/")  # Define the route with the router instance
def signup(user: User):
    users = load_users()
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    users[user.username] = user.password
    save_users(users)
    return {"message": "User created successfully"}
