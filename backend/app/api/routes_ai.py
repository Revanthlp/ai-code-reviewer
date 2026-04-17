from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.post("/analyze")
def analyze(data: dict):
    try:
        repo_url = data.get("repo_url")

        print("RAW INPUT:", repo_url)

        if not repo_url:
            raise HTTPException(status_code=400, detail="Repo URL required")

        # ✅ CLEAN INPUT
        repo_url = repo_url.strip()

        # ✅ REMOVE .git if exists
        repo_url = repo_url.replace(".git", "")

        # ✅ ENSURE CORRECT FORMAT
        if not repo_url.startswith("https://github.com/"):
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        # ✅ SPLIT USER / REPO
        parts = repo_url.replace("https://github.com/", "").split("/")

        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        user = parts[0].strip()
        repo = parts[1].strip()

        print("USER:", user)
        print("REPO:", repo)

        # ✅ GITHUB API CALL
        api_url = f"https://api.github.com/repos/{user}/{repo}"
        print("API URL:", api_url)

        response = requests.get(api_url)

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Repo not found: {user}/{repo}")

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
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))