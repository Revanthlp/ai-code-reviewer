from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True)
    user = Column(String)
    repo = Column(String)
    question = Column(Text)
    answer = Column(Text)