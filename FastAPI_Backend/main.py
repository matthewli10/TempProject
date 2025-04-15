from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends
from auth.database import SessionLocal, engine
from auth.models import User, Base
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
import os

load_dotenv()



# -------------------- App setup --------------------
app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your App",
        version="1.0.0",
        description="API with JWT Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# ----------------- Create database tables -------------
Base.metadata.create_all(bind=engine)

# ------------------ Create DB dependency -------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- Password hashing --------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# -------------------- JWT config --------------------
SECRET_KEY = os.getenv("SECRET_KEY")    # env file
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# -------------------- OAuth2 config --------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------- Auth route --------------------
@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# -------------------- Authenticated route --------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(db, username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

@app.get("/me")
def read_current_user(user: User = Depends(get_current_user)):
    return {"username": user.username, "email": user.email}


# -------------------- Root route --------------------
@app.get("/")
def root():
    return {"Hello": "World"}


# -------------- Testing postgresql login -----------
@app.post("/register-dev")
def create_test_user(db: Session = Depends(get_db)):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpass")
    )
    db.add(user)
    db.commit()
    return {"msg": "User created"}