from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.database import SessionLocal
from app.db import models
from pydantic import BaseModel

router = APIRouter()

# ✅ Password hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ✅ Request schema
class UserCreate(BaseModel):
    username: str
    password: str

# ✅ DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚀 SIGNUP
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # ✅ Check if user exists
        existing_user = db.query(models.User).filter(models.User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # ✅ Hash password
        hashed_password = pwd_context.hash(user.password)

        # ✅ Create user
        new_user = models.User(
            username=user.username,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully"}

    except Exception as e:
        print("Signup Error:", e)  # 🔥 VERY IMPORTANT FOR DEBUG
        raise HTTPException(status_code=500, detail="Internal Server Error")


# 🚀 LOGIN
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # ✅ Find user
        db_user = db.query(models.User).filter(models.User.username == user.username).first()

        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid username")

        # ✅ Verify password
        if not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid password")

        # ✅ Return dummy token (simple version)
        return {"token": "fake-jwt-token"}

    except Exception as e:
        print("Login Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")