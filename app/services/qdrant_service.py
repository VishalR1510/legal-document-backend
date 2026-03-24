from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from app.core.config import settings
from typing import List
from app.models.schemas import SourceChunk
import uuid

class QdrantService:
    def __init__(self):
        # Use cloud Qdrant if URL and API key are configured
        if settings.QDRANT_URL and settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
        elif settings.QDRANT_HOST == "localhost":
            self.client = QdrantClient(path=settings.QDRANT_PATH)
        else:
            self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        self.collection_name = "legal_documents"
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure the collection exists. If not, create it."""
        try:
            collections = self.client.get_collections().collections
            if not any(c.name == self.collection_name for c in collections):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=384,  # Default for all-MiniLM-L6-v2
                        distance=qmodels.Distance.COSINE
                    )
                )
        except Exception as e:
            print(f"Error ensuring Qdrant collection: {e}")

    def store_chunks(self, chunks: List[SourceChunk], embeddings: List[List[float]]):
        """Store document chunks and their embeddings in Qdrant."""
        if not chunks or not embeddings or len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must be non-empty and of the same length.")
            
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid4())
            points.append(
                qmodels.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "doc_id": chunk.doc_id,
                        "page_number": chunk.page_number,
                        "text": chunk.text
                    }
                )
            )
            
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_embedding: List[float], doc_id: str = None, top_k: int = 3) -> List[SourceChunk]:
        """Search for the most relevant chunks given a query embedding."""
        query_filter = None
        if doc_id:
            query_filter = qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="doc_id",
                        match=qmodels.MatchValue(value=doc_id)
                    )
                ]
            )
            
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=query_filter,
            limit=top_k
        )
        
        points = search_result.points if hasattr(search_result, "points") else search_result
        
        results = []
        for scored_point in points:
            results.append(SourceChunk(
                doc_id=scored_point.payload.get("doc_id"),
                page_number=scored_point.payload.get("page_number"),
                text=scored_point.payload.get("text")
            ))
        return results

qdrant_service = QdrantService()
