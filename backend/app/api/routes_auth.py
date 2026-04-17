from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ SIGNUP
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(models.User).filter(models.User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = models.User(
            username=user.username,
            password=user.password  # ⚠️ plain text for now
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully"}

    except Exception as e:
        print("Signup Error:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ✅ LOGIN
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.username == user.username).first()

        if not db_user or db_user.password != user.password:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        return {"token": "fake-jwt-token"}

    except Exception as e:
        print("Login Error:", e)
        raise HTTPException(status_code=500, detail=str(e))