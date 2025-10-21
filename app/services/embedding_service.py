from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.model = None
        self.model_name = settings.embedding_model
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text"""
        try:
            if self.model is None:
                self._load_model()
            
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts"""
        try:
            if self.model is None:
                self._load_model()
            
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def get_model_dimension(self) -> int:
        """Get the dimension of the embedding model"""
        if self.model is None:
            self._load_model()
        return self.model.get_sentence_embedding_dimension()

# Global instance
embedding_service = EmbeddingService()
