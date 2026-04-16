from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_auth, routes_ai
from app.db.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI()

# Enable CORS (ONLY ONCE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes_auth.router)
app.include_router(routes_ai.router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "🚀 AI Code Reviewer Running"}