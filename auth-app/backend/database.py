#SQLAlchemy is a Python library used to interact with databases.
#create_engine creates a connection engine to your database.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base #Used to create a base class for database models.
from sqlalchemy.orm import sessionmaker  #A session is like a temporary workspace where you interact with the database.
import os #Python’s built-in module to access environment variables and system information.

DATABASE_URL = "postgresql://postgres:987654321@localhost:5432/authdb"  #This is the database connection string.
#database_type://username:password@server:postgreSQLdefaultport/databasename

engine = create_engine(DATABASE_URL) #The engine, manages connections, communicates with PostgreSQL

SessionLocal = sessionmaker(    # Meaning: whenever we call SessionLocal() we get a new database session.
    autocommit=False,           # won't automatically save
    autoflush=False,            # Prevents automatic syncing of changes to DB before queries.
    bind=engine                 # This tells the session which database engine to use.
)

Base = declarative_base()      # Creates the base class for all models.


#yield returns the database session to FastAPI.
#FastAPI then injects it into routes using Depends().


# ADD THIS FUNCTION
def get_db():            #This function provides a database session to API routes.
    db = SessionLocal()  #Creates a new database session.
    try:
        yield db
    finally:
        db.close()