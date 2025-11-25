from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Optional
import os

# Use a non-bcrypt scheme to avoid system-level bcrypt build/runtime issues
PWD_CTX = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') or 60)

def get_password_hash(password: str) -> str:
    return PWD_CTX.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CTX.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_password_reset_token(email: str, expires_minutes: int = 15) -> str:
    payload = {"sub": email, "purpose": "pwd_reset"}
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise
