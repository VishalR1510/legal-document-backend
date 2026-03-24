from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    message: str
    doc_id: str
    chunks_processed: int

class QueryRequest(BaseModel):
    query: str
    doc_id: Optional[str] = None
    top_k: int = 3

class SourceChunk(BaseModel):
    doc_id: str
    page_number: int
    text: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
