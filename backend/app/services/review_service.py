import os

from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not configured")

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key,
        temperature=0,
    )


def review_code(code: str) -> str:
    llm = get_llm()

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

    response = llm.invoke(prompt)

    return response.content


def review_with_prompt(prompt: str) -> str:
    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content