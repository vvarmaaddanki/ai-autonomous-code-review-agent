from fastapi import FastAPI
from app.agent import review_graph

from app.services.github_service import (
    get_repository_info,
    get_repository_files,
    get_file_content
)

from app.services.review_service import review_code


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


from pydantic import BaseModel


class CodeReviewRequest(BaseModel):
    code: str


@app.post("/review")
def review(request: CodeReviewRequest):
    result = review_graph.invoke({
        "code": request.code,
        "final_review": ""
    })

    return {
        "review": result["final_review"]
    }

@app.get("/github/{owner}/{repo}/file")
def github_file_content(owner: str, repo: str, path: str):
    content = get_file_content(owner, repo, path)

    return {
        "repository": f"{owner}/{repo}",
        "file": path,
        "content": content
    }

@app.post("/github/{owner}/{repo}/review-file")
def review_github_file(owner: str, repo: str, path: str):
    code = get_file_content(owner, repo, path)
    result = review_code(code)

    return {
        "repository": f"{owner}/{repo}",
        "file": path,
        "review": result
    }


@app.post("/github/{owner}/{repo}/review")
def review_github_repository(owner: str, repo: str):
    data = get_repository_files(owner, repo)

    python_files = []

    for item in data.get("tree", []):
        path = item.get("path", "")

        if (
            item.get("type") == "blob"
            and path.endswith(".py")
            and "_pycache_" not in path
        ):
            python_files.append(path)

    python_files = python_files[:5]

    source_code = ""

    for path in python_files:
        code = get_file_content(owner, repo, path)

        source_code += f"""
        
==============================
FILE: {path}
==============================

{code}

"""

    result = review_graph.invoke({
    "code": source_code,
    "prompt": "",
    "review": "",
    "final_review": ""
})

repository_review = result["final_review"]

    return {
        "repository": f"{owner}/{repo}",
        "files_reviewed": len(python_files),
        "review": repository_review
    }