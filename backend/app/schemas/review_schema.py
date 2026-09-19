from pydantic import BaseModel
from typing import List


class CodeReviewRequest(BaseModel):
    code: str


class CodeReviewResponse(BaseModel):
    summary: str
    bugs: List[str]
    security_issues: List[str]
    performance_issues: List[str]
    code_quality_issues: List[str]
    recommendations: List[str]