from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.github_service import (
    get_repository_info,
    get_repository_files,
    get_file_content,
)

from app.services.review_service import review_code
from app.agent import review_graph


app = FastAPI(
    title="AI Autonomous Code Review Agent",
    description="AI-powered autonomous code review system",
    version="1.0.0",
)


class CodeReviewRequest(BaseModel):
    code: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Autonomous Code Review Agent",
    }


@app.get("/github/{owner}/{repo}")
def github_repository(owner: str, repo: str):
    return get_repository_info(owner, repo)


@app.get("/github/{owner}/{repo}/files")
def github_repository_files(owner: str, repo: str):
    return get_repository_files(owner, repo)


@app.post("/review")
def review(request: CodeReviewRequest):
    try:
        result = review_graph.invoke({
            "code": request.code,
            "prompt": "",
            "review": "",
            "final_review": ""
        })

        return {
            "review": result["final_review"]
        }

    except Exception as e:
        error_message = str(e).lower()

        if "quota" in error_message or "429" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again after the quota resets."
            )

        raise HTTPException(
            status_code=500,
            detail="Code review failed."
        )


@app.get("/github/{owner}/{repo}/file")
def github_file_content(
    owner: str,
    repo: str,
    path: str,
):
    content = get_file_content(owner, repo, path)

    return {
        "repository": f"{owner}/{repo}",
        "file": path,
        "content": content,
    }


@app.post("/github/{owner}/{repo}/review-file")
def review_github_file(
    owner: str,
    repo: str,
    path: str,
):
    try:
        code = get_file_content(owner, repo, path)

        result = review_code(code)

        return {
            "repository": f"{owner}/{repo}",
            "file": path,
            "review": result,
        }

    except Exception as e:
        error_message = str(e)

        if "quota" in error_message.lower() or "429" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later.",
            )

        raise HTTPException(
            status_code=500,
            detail="AI code review service failed.",
        )


@app.post("/github/{owner}/{repo}/review")
def review_github_repository(
    owner: str,
    repo: str,
):
    try:
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
====================================
FILE: {path}
====================================

{code}
"""

        result = review_graph.invoke(
            {
                "code": source_code,
                "prompt": "",
                "review": "",
                "final_review": "",
            }
        )

        repository_review = result["final_review"]

        return {
            "repository": f"{owner}/{repo}",
            "files_reviewed": len(python_files),
            "review": repository_review,
        }

    except Exception as e:
        error_message = str(e)

        if "quota" in error_message.lower() or "429" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later.",
            )

        raise HTTPException(
            status_code=500,
            detail="AI repository review service failed.",
        )