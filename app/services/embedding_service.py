from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
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
