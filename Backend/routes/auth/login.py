from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from user_credential import load_users

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

@router.post("/")
def login(user: User):
    users = load_users()
    if user.username not in users or users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"message": "Login successful"}
