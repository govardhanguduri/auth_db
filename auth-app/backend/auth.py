#passlib is a password hashing library.
#CryptContext manages hashing algorithms.
from passlib.context import CryptContext 
from jose import JWTError, jwt            # Library used for JWT tokens, stateless authentication.
from datetime import datetime, timedelta  # Used to create token expiration times.
import os                                 # Used for environment variables.

#JWT tokens must be signed with a secret key.
#If .env variable exists → use SECRET_KEY
#Otherwise → fallback "supersecretkey"
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256" #The cryptographic algorithm used for signing tokens. 
ACCESS_TOKEN_EXPIRE_MINUTES = 30  #Tokens expire after 30 minutes.

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto") #hashing algorithm: 'Argon2' is a very secure password hashing algorithm.

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)