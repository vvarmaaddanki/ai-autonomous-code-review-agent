from fastapi import FastAPI
from app.services.github_service import (
    get_repository_info,
    get_repository_files
)

app = FastAPI(
    title="AI Autonomous Code Review Agent",
    description="AI-powered autonomous code review system",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Autonomous Code Review Agent"
    }


@app.get("/github/{owner}/{repo}")
def github_repository(owner: str, repo: str):
    repository = get_repository_info(owner, repo)

    return {
        "name": repository["name"],
        "full_name": repository["full_name"],
        "description": repository["description"],
        "stars": repository["stargazers_count"],
        "language": repository["language"]
    }


@app.get("/github/{owner}/{repo}/files")
def github_repository_files(owner: str, repo: str):
    data = get_repository_files(owner, repo)

    files = []

    for item in data.get("tree", []):
        if item["type"] == "blob":
            files.append({
                "path": item["path"],
                "type": item["type"]
            })

    return {
        "repository": f"{owner}/{repo}",
        "file_count": len(files),
        "files": files
    }