from sentence_transformers import SentenceTransformer
from typing import List
from app.core.config import settings
import os

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Set HF token if available
        if settings.HF_TOKEN:
            os.environ["HF_TOKEN"] = settings.HF_TOKEN
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate vector embeddings for a list of texts.
        """
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
        
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate vector embedding for a single text.
        """
        embedding = self.model.encode([text])[0]
        return embedding.tolist()

embedding_service = EmbeddingService()
