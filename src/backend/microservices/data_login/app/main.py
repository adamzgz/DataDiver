from pydantic import BaseModel, EmailStr
import dotenv
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from database import connect_to_database, create_user, close_db_connection, create_access_token, authenticate_user, create_refresh_token
from fastapi import Depends, FastAPI, Body, HTTPException, status
from config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

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
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": str(user["user_id"])})
    refresh_token = create_refresh_token(data={"sub": str(user["user_id"])})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}



@app.post("/token/refresh/")
def refresh_access_token(refresh_token: str = Body(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}