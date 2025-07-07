from fastapi import APIRouter
from models.schemas import RAGQueryRequest, RAGQueryResponse
from services.rag import run_rag_pipeline

router = APIRouter()

@router.post("/rag-query", response_model=RAGQueryResponse)
async def rag_query(data: RAGQueryRequest):
    answer, sources = run_rag_pipeline(data.question)
    return RAGQueryResponse(answer=answer, sources=sources)