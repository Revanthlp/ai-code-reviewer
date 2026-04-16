from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(user: UserCreate):
    db: Session = next(get_db())

    # Check if user exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Create user
    new_user = User(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@router.post("/login")
def login(user: UserCreate):
    db: Session = next(get_db())

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": "fake-jwt-token"}