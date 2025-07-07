from pydantic import BaseModel
from typing import List

class RAGQueryRequest(BaseModel):
    user_id: str
    question: str

class RAGQueryResponse(BaseModel):
    answer: str
    sources: List[str]