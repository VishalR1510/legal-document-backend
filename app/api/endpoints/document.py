from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.schemas import UploadResponse
import uuid
from app.services.document_processor import document_processor
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a legal document (PDF) for processing and indexing.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        content = await file.read()
        doc_id = str(uuid.uuid4())
        
        # Process PDF and chunk
        chunks = document_processor.process_pdf(content, doc_id)
        if not chunks:
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF.")
            
        # Generate embeddings
        texts = [chunk.text for chunk in chunks]
        embeddings = embedding_service.generate_embeddings(texts)
        
        # Store in Qdrant
        qdrant_service.store_chunks(chunks, embeddings)
        
        return UploadResponse(
            message="Document uploaded and indexed successfully",
            doc_id=doc_id,
            chunks_processed=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
