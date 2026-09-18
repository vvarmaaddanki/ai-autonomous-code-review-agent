import requests
import base64


def get_repository_info(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()


def get_repository_files(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()




def get_file_content(owner: str, repo: str, path: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    content = data.get("content", "")
    encoding = data.get("encoding")

    if encoding == "base64":
        return base64.b64decode(content).decode("utf-8")

    return content