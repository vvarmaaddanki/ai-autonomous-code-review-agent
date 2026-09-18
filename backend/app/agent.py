from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.services.review_service import review_with_prompt


class ReviewState(TypedDict):
    code: str
    prompt: str
    review: str
    final_review: str


def prepare_code(state: ReviewState):
    code = state["code"].strip()

    return {
        "code": code
    }


def build_review_prompt(state: ReviewState):
    prompt = f"""
You are an expert software code reviewer.

Review the following source code.

Analyze:
1. Bugs
2. Security vulnerabilities
3. Performance issues
4. Code quality
5. Best-practice improvements

Provide a clear and structured review.

SOURCE CODE:
{state["code"]}
"""

    return {
        "prompt": prompt
    }


def analyze_code(state: ReviewState):
    review = review_with_prompt(state["prompt"])

    return {
        "review": review
    }


def format_review(state: ReviewState):
    return {
        "final_review": state["review"]
    }


builder = StateGraph(ReviewState)

builder.add_node("prepare_code", prepare_code)
builder.add_node("build_review_prompt", build_review_prompt)
builder.add_node("analyze_code", analyze_code)
builder.add_node("format_review", format_review)

builder.add_edge(START, "prepare_code")
builder.add_edge("prepare_code", "build_review_prompt")
builder.add_edge("build_review_prompt", "analyze_code")
builder.add_edge("analyze_code", "format_review")
builder.add_edge("format_review", END)

review_graph = builder.compile()