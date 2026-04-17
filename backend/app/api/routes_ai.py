from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

# 🚀 ANALYZE REPO
@router.post("/analyze")
def analyze(data: dict):
    repo_url = data.get("repo_url")

    if not repo_url:
        raise HTTPException(status_code=400, detail="Repo URL required")

    try:
        # ✅ Convert GitHub URL → API URL
        # Example:
        # https://github.com/user/repo → https://api.github.com/repos/user/repo
        parts = repo_url.replace("https://github.com/", "").split("/")

        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        user = parts[0]
        repo = parts[1]

        api_url = f"https://api.github.com/repos/{user}/{repo}"

        response = requests.get(api_url)

        # ❌ Repo not found
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Repo not found")

        repo_data = response.json()

        return {
            "message": "Repo analyzed successfully",
            "name": repo_data.get("name"),
            "stars": repo_data.get("stargazers_count"),
            "description": repo_data.get("description")
        }

    except Exception as e:
        print("Analyze Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# 🤖 ASK AI (temporary)
@router.post("/ask")
def ask(data: dict):
    question = data.get("q")

    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    # Simple response for now
    return {
        "answer": f"You asked: {question}. AI feature coming soon 🚀"
    }