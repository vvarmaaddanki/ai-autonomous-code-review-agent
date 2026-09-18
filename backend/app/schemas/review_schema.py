from pydantic import BaseModel


class CodeReviewRequest(BaseModel):
    code: str