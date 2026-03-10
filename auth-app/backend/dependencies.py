from fastapi import Depends, HTTPException, status   # Used for dependency injection and error handling.
from fastapi.security import OAuth2PasswordBearer    # Implements OAuth2 Bearer Token authentication.
from jose import jwt, JWTError                       # Used to decode JWT tokens.
from database import SessionLocal                    # Used to query the user from DB.
from models import User
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # Tells FastAPI:Expect a Bearer token
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)): # extracts token, decodes token, finds user in database, returns the user 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])        # Decodes the JWT.
        user_id = payload.get("sub")                                           # Extracts user ID stored in token.
        user = db.query(User).filter(User.id == user_id).first()               # Finds the user in the database.
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")