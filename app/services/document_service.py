import os
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import Document, DocumentChunk
from app.services.embedding_service import embedding_service
from app.services.llm_service import llm_service
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        self.embedding_service = embedding_service
        self.llm_service = llm_service
    
    def process_document(self, db: Session, document_id: str, content: str) -> bool:
        """Process a document by chunking it and creating embeddings"""
        try:
            # Get the document
            document = db.query(Document).filter(Document.id == document_id).first()
            if not document:
                raise ValueError("Document not found")
            
            # Split text into chunks
            chunks = self.llm_service.text_splitter.split_text(content)
            
            # Create embeddings for each chunk
            embeddings = self.embedding_service.get_embeddings(chunks)
            
            # Delete existing chunks for this document
            db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
            
            # Create new chunks with embeddings
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_record = DocumentChunk(
                    document_id=document_id,
                    chunk_index=i,
                    content=chunk,
                    embedding=embedding,
                    metadata=f'{{"chunk_size": {len(chunk)}, "chunk_index": {i}}}'
                )
                db.add(chunk_record)
            
            # Mark document as processed
            document.processed = True
            db.commit()
            
            logger.info(f"Processed document {document_id} with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")
            db.rollback()
            return False
    
    def search_similar_chunks(self, db: Session, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar chunks using vector similarity"""
        try:
            # Get query embedding
            query_embedding = self.embedding_service.get_embedding(query)
            
            # Search for similar chunks using pgvector
            # Note: This is a simplified version. In production, you'd want to use proper vector search
            chunks = db.query(DocumentChunk).all()
            
            # Calculate similarities (in production, use pgvector's built-in similarity functions)
            similarities = []
            for chunk in chunks:
                if chunk.embedding:
                    # Simple cosine similarity calculation
                    similarity = self._cosine_similarity(query_embedding, chunk.embedding)
                    similarities.append({
                        'chunk': chunk,
                        'similarity': similarity
                    })
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            results = []
            for item in similarities[:limit]:
                chunk = item['chunk']
                results.append({
                    'id': str(chunk.id),
                    'content': chunk.content,
                    'document_id': str(chunk.document_id),
                    'chunk_index': chunk.chunk_index,
                    'similarity': item['similarity'],
                    'metadata': chunk.metadata
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching similar chunks: {e}")
            return []
    
    def get_document_chunks(self, db: Session, document_id: str) -> List[DocumentChunk]:
        """Get all chunks for a specific document"""
        return db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document_id
        ).order_by(DocumentChunk.chunk_index).all()
    
    def delete_document(self, db: Session, document_id: str) -> bool:
        """Delete a document and all its chunks"""
        try:
            # Delete chunks first
            db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
            
            # Delete document
            db.query(Document).filter(Document.id == document_id).delete()
            
            db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            db.rollback()
            return False
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        import numpy as np
        
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)

# Global instance
document_service = DocumentService()
