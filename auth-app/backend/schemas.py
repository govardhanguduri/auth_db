from pydantic import BaseModel, EmailStr # data validation schemas using Pydantic.

class UserCreate(BaseModel):             # Used during signup.
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):             # Used for login requests.
    email: EmailStr
    password: str

class UserOut(BaseModel):               # Used for responses.
    id: int
    username: str
    email: EmailStr
    class Config:                       # Allows Pydantic to read SQLAlchemy objects directly.
        orm_mode = True                 # User object → JSON response