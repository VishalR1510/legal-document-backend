import google.generativeai as genai
from app.core.config import settings
from app.services.qdrant_service import qdrant_service
from app.services.embedding_service import embedding_service
from app.models.schemas import QueryResponse
from typing import Optional

class RagService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-flash-latest')
        
    def generate_answer(self, query: str, doc_id: Optional[str] = None, top_k: int = 3) -> QueryResponse:
        """
        Embed the query, search Qdrant for context, and prompt Gemini for an answer.
        """
        # 1. Embed query
        query_embedding = embedding_service.generate_embedding(query)
        
        # 2. Search Qdrant
        relevant_chunks = qdrant_service.search(
            query_embedding=query_embedding,
            doc_id=doc_id,
            top_k=top_k
        )
        
        # 3. Prepare context
        context_parts = []
        for i, chunk in enumerate(relevant_chunks):
            context_parts.append(f"--- Chunk {i+1} (Page {chunk.page_number}) ---\n{chunk.text}")
            
        context_str = "\n\n".join(context_parts)
        
        # 4. Prompt Gemini
        prompt = f"""
You are a helpful legal assistant. Answer the user's question based ONLY on the provided context from a legal document.
If the answer cannot be found in the context, state that you cannot answer the question based on the provided documents.

Context:
{context_str}

Question:
{query}

Answer:"""
        
        response = self.model.generate_content(prompt)
        answer_text = response.text if response.text else "No response generated."
        
        return QueryResponse(
            answer=answer_text,
            sources=relevant_chunks
        )

rag_service = RagService()
