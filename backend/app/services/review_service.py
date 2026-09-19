import os

from google import genai


def review_code(code: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not configured")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert software code reviewer.

Review the following source code.

Identify:

1. Bugs
2. Security issues
3. Performance problems
4. Code quality issues
5. Recommended improvements

Give a clear, structured review.

SOURCE CODE:

{code}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )

    return response.text