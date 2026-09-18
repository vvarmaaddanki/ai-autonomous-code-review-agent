import requests


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