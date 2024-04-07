from pydantic import BaseModel, EmailStr
from datetime import timedelta
import dotenv
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from database import connect_to_database, create_user, close_db_connection, create_access_token, authenticate_user
from fastapi import Depends, FastAPI
from datetime import timedelta
from config import ACCESS_TOKEN_EXPIRE_MINUTES

dotenv.load_dotenv('token.env')


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/register/")
def register(user: UserCreate):
    db = connect_to_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    result = create_user(db, user)
    close_db_connection(db)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {"message": "User created successfully.", "user_id": result["user_id"]}


@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}