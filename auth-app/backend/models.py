from sqlalchemy import Column, Integer, String # Used to define table columns.
from database import Base                      # Imports the Base class from database.py.

#Creates a User model.
#Each model corresponds to a database table.
class User(Base):
    __tablename__ = "users" #Table name in PostgreSQL 
    id = Column(Integer, primary_key=True, index=True)  # Primarykey #Auto-increment.
    username = Column(String, unique=True, index=True)  # unique=True ensures no duplicates.
    email = Column(String, unique=True, index=True)     
    hashed_password = Column(String)                    # Stores hashed password.