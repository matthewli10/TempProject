from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta

# -------------------- App setup --------------------
app = FastAPI()

# -------------------- Password hashing --------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# -------------------- JWT config --------------------
SECRET_KEY = "6691aa1e301ce408ae939b2c9dfcefa3d95b7d8b1ad64addef387b0eb93e0258"  # Use env variable later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -------------------- In-memory 'fake' user DB --------------------
# Replace with actual DB queries later
fake_user_db = {
    "testuser": {
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": hash_password("testpass"),
    }
}

def get_user(username: str):
    return fake_user_db.get(username)

# -------------------- OAuth2 config --------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------- Auth route --------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# -------------------- Authenticated route --------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        return get_user(username)
    except JWTError:
        raise credentials_exception

@app.get("/me")
def read_current_user(user: dict = Depends(get_current_user)):
    return {"username": user["username"], "email": user["email"]}

# -------------------- Root route --------------------
@app.get("/")
def root():
    return {"Hello": "World"}
