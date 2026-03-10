from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware #Helps your frontend talk to your API
from sqlalchemy.orm import Session                 #A SQLAlchemy object that represents a connection to the database.
#Base → SQLAlchemy’s base class that defines database models (like User).
#engine → The database engine; it tells SQLAlchemy how to connect to your database (PostgreSQL, SQLite, etc.).
#get_db → A helper function that gives us a database session for each API request.
from database import Base, engine, get_db 
from models import User  #User → Our database model representing a user table with fields like username, email, and hashed_password.
from schemas import UserCreate, UserLogin, UserOut #modal schemas representation
from auth import hash_password, verify_password, create_access_token
from dependencies import get_current_user #A function that checks the token sent by the user

#This line creates all the tables in the database according to your models (if they don’t exist yet). 
# bind=engine means it uses your database connection.
Base.metadata.create_all(bind=engine)

app = FastAPI()  #Creates a FastAPI application instance.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Accept requests from any frontend
    allow_credentials=True,  # Allow cookies or authentication headers.
    allow_methods=["*"],     # Accept all HTTP methods (GET, POST, etc.).
    allow_headers=["*"],     # Accept all headers.
)


@app.get("/") #Simple test route to check if the API works
def read_root():
    return {"message": "API is running!"}

@app.post("/signup", response_model=UserOut) #The API will only return fields defined in UserOut, e.g., not the password.
#Injects a database session into the function
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)      # Add the user to the database session.
    db.commit()           # Save changes to the database.
    db.refresh(new_user)  # Refresh the object to get updated data (like id assigned by the database
    return new_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)): #Expect email and password in the request body.
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({"sub": str(db_user.id)}) #The sub field usually holds the user ID. This token will later verify the user’s identity.
    return {"access_token": token, "token_type": "bearer"}

@app.get("/dashboard", response_model=UserOut)
def dashboard(current_user: User = Depends(get_current_user)):
    return current_user