from datetime import datetime, timedelta
from jose import jwt
import os
from typing import Optional

# -------------------- JWT config --------------------
SECRET_KEY = os.getenv("SECRET_KEY")    # env file
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_email_verification_token(email: str):
    return create_access_token(
        data={"sub": email},
        expires_delta=timedelta(hours=1)
    )