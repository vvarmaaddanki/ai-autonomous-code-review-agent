import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

class CodeReview(BaseModel):
    bugs: list[str] = Field(description="Bugs found in the code")
    security_issues: list[str] = Field(description="Security issues found")
    performance_issues: list[str] = Field(description="Performance problems found")
    code_quality: list[str] = Field(description="Code quality issues found")
    recommendations: list[str] = Field(description="Recommended improvements")
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

def structured_review(prompt: str) -> dict:
    llm = get_llm().with_structured_output(CodeReview)

    response = llm.invoke(prompt)

    return response.model_dump()