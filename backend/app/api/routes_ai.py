from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import requests

router = APIRouter()

class RepoRequest(BaseModel):
    repo_url: str

class QuestionRequest(BaseModel):
    q: str


# Temporary memory (demo)
repo_data = {}


@router.post("/analyze")
def analyze_repo(data: RepoRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        # Extract repo API URL
        if "github.com" not in data.repo_url:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        parts = data.repo_url.replace("https://github.com/", "").split("/")
        owner, repo = parts[0], parts[1]

        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        res = requests.get(api_url)

        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Repo not found")

        repo_info = res.json()

        # Save minimal data
        repo_data["info"] = {
            "name": repo_info["name"],
            "description": repo_info["description"],
            "stars": repo_info["stargazers_count"]
        }

        return {"message": "Repo analyzed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask")
def ask_ai(q: QuestionRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    if "info" not in repo_data:
        raise HTTPException(status_code=400, detail="Analyze repo first")

    info = repo_data["info"]

    # Simple AI response (demo)
    answer = f"""
Repository: {info['name']}
Description: {info['description']}
Stars: {info['stars']}

Answer to your question: {q.q}
(This is a demo response)
"""

    return {"answer": answer}