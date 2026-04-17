from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

@router.post("/analyze")
def analyze(data: dict):
    try:
        repo_url = data.get("repo_url")

        print("RAW INPUT:", repo_url)

        if not repo_url:
            raise HTTPException(status_code=400, detail="Repo URL required")

        # ✅ CLEAN URL
        repo_url = repo_url.strip().replace(".git", "")

        if "github.com" not in repo_url:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        # ✅ EXTRACT USER + REPO
        repo_path = repo_url.split("github.com/")[-1]
        parts = repo_path.split("/")

        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="Invalid GitHub URL")

        user = parts[0].strip()
        repo = parts[1].strip()

        print("USER:", user)
        print("REPO:", repo)

        # ✅ GITHUB API URL
        api_url = f"https://api.github.com/repos/{user}/{repo}"
        print("API URL:", api_url)

        # ✅ TOKEN PART (THIS WAS MISSING BEFORE)
        token = os.getenv("GITHUB_TOKEN")

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "MyApp"
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        print("TOKEN:", token)

        # ✅ REQUEST WITH HEADERS
        response = requests.get(api_url, headers=headers)

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail=f"Repo not found OR GitHub blocked request ({response.status_code})"
            )

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