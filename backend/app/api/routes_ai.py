from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.post("/analyze")
def analyze(data: dict):
    try:
        repo_url = data.get("repo_url")

        if not repo_url:
            raise HTTPException(status_code=400, detail="Repo URL required")

        # ✅ CLEAN URL
        repo_url = repo_url.strip()

        if "github.com" not in repo_url:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        # ✅ EXTRACT USER + REPO SAFELY
        parts = repo_url.replace("https://github.com/", "").strip("/").split("/")

        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        user = parts[0].strip()
        repo = parts[1].strip()

        print("User:", user)
        print("Repo:", repo)

        # ✅ CORRECT API URL
        api_url = f"https://api.github.com/repos/{user}/{repo}"

        response = requests.get(api_url)

        print("GitHub Status:", response.status_code)
        print("GitHub Response:", response.text)

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