from fastapi import FastAPI, HTTPException

from app.services.github_service import (
    get_repository_info,
    get_repository_files,
    get_file_content
)

from app.services.review_service import review_code

from app.schemas.review_schema import CodeReviewRequest


app = FastAPI(
    title="AI Autonomous Code Review Agent",
    description="AI-powered autonomous code review system",
    version="1.0.0"
)


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Autonomous Code Review Agent"
    }


# --------------------------------------------------
# GitHub Repository Information
# --------------------------------------------------

@app.get("/github/{owner}/{repo}")
def github_repository_info(owner: str, repo: str):

    data = get_repository_info(owner, repo)

    return data


# --------------------------------------------------
# GitHub Repository Files
# --------------------------------------------------

@app.get("/github/{owner}/{repo}/files")
def github_repository_files(owner: str, repo: str):

    data = get_repository_files(owner, repo)

    return data


# --------------------------------------------------
# Direct Code Review
# --------------------------------------------------

@app.post("/review")
def review(request: CodeReviewRequest):

    try:

        result = review_code(request.code)

        return {
            "review": result
        }

    except Exception as e:

        error_message = str(e)

        print("Code review error:", error_message)

        import traceback
        traceback.print_exc()

        if "quota" in error_message.lower():

            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again after the quota resets."
            )

        raise HTTPException(
            status_code=500,
            detail="AI code review service failed."
        )


# --------------------------------------------------
# Get GitHub File Content
# --------------------------------------------------

@app.get("/github/{owner}/{repo}/file")
def github_file_content(
    owner: str,
    repo: str,
    path: str
):

    try:

        content = get_file_content(
            owner,
            repo,
            path
        )

        return {
            "repository": f"{owner}/{repo}",
            "file": path,
            "content": content
        }

    except Exception as e:

        print("GitHub file error:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch GitHub file."
        )


# --------------------------------------------------
# Review Individual GitHub File
# --------------------------------------------------

@app.post("/github/{owner}/{repo}/review-file")
def review_github_file(
    owner: str,
    repo: str,
    path: str
):

    try:

        code = get_file_content(
            owner,
            repo,
            path
        )

        result = review_code(code)

        return {
            "repository": f"{owner}/{repo}",
            "file": path,
            "review": result
        }

    except Exception as e:

        error_message = str(e)

        print("GitHub file review error:", error_message)

        import traceback
        traceback.print_exc()

        if "quota" in error_message.lower():

            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again after the quota resets."
            )

        raise HTTPException(
            status_code=500,
            detail="AI file review service failed."
        )


# --------------------------------------------------
# Review Entire GitHub Repository
# --------------------------------------------------

@app.post("/github/{owner}/{repo}/review")
def review_github_repository(
    owner: str,
    repo: str
):

    try:

        # Get repository files
        data = get_repository_files(
            owner,
            repo
        )

        # Store Python files
        python_files = []

        for item in data.get("tree", []):

            path = item.get("path", "")

            if (
                item.get("type") == "blob"
                and path.endswith(".py")
                and "_pycache_" not in path
            ):

                python_files.append(path)

        # Limit the number of files reviewed
        python_files = python_files[:5]

        # Combine source code
        source_code = ""

        for path in python_files:

            code = get_file_content(
                owner,
                repo,
                path
            )

            source_code += f"""
====================================
FILE: {path}
====================================

{code}
"""

        # Send combined source code to Gemini
        repository_review = review_code(
            source_code
        )

        return {
            "repository": f"{owner}/{repo}",
            "files_reviewed": len(python_files),
            "review": repository_review
        }

    except Exception as e:

        error_message = str(e)

        print(
            "Repository review error:",
            error_message
        )

        import traceback
        traceback.print_exc()

        # Gemini quota error
        if "quota" in error_message.lower():

            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again after the quota resets."
            )

        # Other errors
        raise HTTPException(
            status_code=500,
            detail="AI repository review service failed."
        )