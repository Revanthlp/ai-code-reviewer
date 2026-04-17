from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

# 🚀 ANALYZE REPO
@router.post("/analyze")
def analyze(data: dict):
    try:
        repo_url = data.get("repo_url")

        if not repo_url:
            raise HTTPException(status_code=400, detail="Repo URL required")

        if "github.com" not in repo_url:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        # ✅ Extract user/repo safely
        repo_path = repo_url.replace("https://github.com/", "").strip("/")
        parts = repo_path.split("/")

        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        user, repo = parts[0], parts[1]

        # ✅ GitHub API URL
        api_url = f"https://api.github.com/repos/{user}/{repo}"

        # ✅ Call GitHub API
        response = requests.get(api_url)

        print("GitHub API status:", response.status_code)
        print("GitHub response:", response.text)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Repo not found")

        repo_data = response.json()

        return {
            "message": "Repo analyzed successfully",
            "name": repo_data.get("name"),
            "stars": repo_data.get("stargazers_count"),
            "description": repo_data.get("description")
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("Analyze Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# 🤖 ASK
@router.post("/ask")
def ask(data: dict):
    question = data.get("q")

    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    return {
        "answer": f"You asked: {question}. AI feature coming soon 🚀"
    }