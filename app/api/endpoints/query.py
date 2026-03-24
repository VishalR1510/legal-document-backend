from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query the indexed legal documents using RAG.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")
    
    try:
        response = rag_service.generate_answer(
            query=request.query,
            doc_id=request.doc_id,
            top_k=request.top_k
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
