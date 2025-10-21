import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.database import ChatSession, ChatMessage
from app.services.llm_service import llm_service
from app.services.document_service import document_service
from app.models import ChatMessageRequest, ChatResponse, ChatSessionResponse
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.llm_service = llm_service
        self.document_service = document_service
    
    def create_session(self, db: Session, session_name: str = "New Chat") -> ChatSessionResponse:
        """Create a new chat session"""
        try:
            session = ChatSession(session_name=session_name)
            db.add(session)
            db.commit()
            db.refresh(session)
            
            return ChatSessionResponse(
                id=session.id,
                session_name=session.session_name,
                created_at=session.created_at,
                last_activity=session.last_activity,
                is_active=session.is_active
            )
        except Exception as e:
            logger.error(f"Error creating chat session: {e}")
            raise
    
    def get_session(self, db: Session, session_id: str) -> Optional[ChatSessionResponse]:
        """Get a chat session by ID"""
        try:
            session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if not session:
                return None
            
            return ChatSessionResponse(
                id=session.id,
                session_name=session.session_name,
                created_at=session.created_at,
                last_activity=session.last_activity,
                is_active=session.is_active
            )
        except Exception as e:
            logger.error(f"Error getting chat session: {e}")
            return None
    
    def get_sessions(self, db: Session, limit: int = 20) -> List[ChatSessionResponse]:
        """Get all chat sessions"""
        try:
            sessions = db.query(ChatSession).filter(
                ChatSession.is_active == True
            ).order_by(ChatSession.last_activity.desc()).limit(limit).all()
            
            return [
                ChatSessionResponse(
                    id=session.id,
                    session_name=session.session_name,
                    created_at=session.created_at,
                    last_activity=session.last_activity,
                    is_active=session.is_active
                )
                for session in sessions
            ]
        except Exception as e:
            logger.error(f"Error getting chat sessions: {e}")
            return []
    
    def get_messages(self, db: Session, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get messages for a chat session"""
        try:
            messages = db.query(ChatMessage).filter(
                ChatMessage.session_id == session_id
            ).order_by(ChatMessage.timestamp.asc()).limit(limit).all()
            
            return [
                {
                    "id": str(message.id),
                    "role": message.role,
                    "content": message.content,
                    "timestamp": message.timestamp,
                    "metadata": message.metadata
                }
                for message in messages
            ]
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            return []
    
    def send_message(self, db: Session, request: ChatMessageRequest) -> ChatResponse:
        """Send a message and get AI response"""
        try:
            # Get or create session
            if request.session_id:
                session = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
                if not session:
                    raise ValueError("Session not found")
            else:
                session = ChatSession(session_name="New Chat")
                db.add(session)
                db.commit()
                db.refresh(session)
            
            # Save user message
            user_message = ChatMessage(
                session_id=session.id,
                role="user",
                content=request.message,
                metadata='{"type": "user_message"}'
            )
            db.add(user_message)
            
            # Search for relevant document chunks
            relevant_chunks = self.document_service.search_similar_chunks(
                db, request.message, limit=3
            )
            
            # Build context from relevant chunks
            context = ""
            sources = []
            if relevant_chunks:
                context_parts = []
                for chunk in relevant_chunks:
                    context_parts.append(chunk['content'])
                    sources.append({
                        "document_id": chunk['document_id'],
                        "chunk_id": chunk['id'],
                        "similarity": chunk['similarity']
                    })
                context = "\n\n".join(context_parts)
            
            # Generate AI response
            ai_response = self.llm_service.generate_response(
                request.message, 
                context if context else None
            )
            
            # Save AI message
            ai_message = ChatMessage(
                session_id=session.id,
                role="assistant",
                content=ai_response,
                metadata=f'{{"type": "ai_response", "sources_count": {len(sources)}}}'
            )
            db.add(ai_message)
            
            # Update session last activity
            from datetime import datetime
            session.last_activity = datetime.utcnow()
            
            db.commit()
            db.refresh(ai_message)
            
            return ChatResponse(
                message={
                    "id": ai_message.id,
                    "role": ai_message.role,
                    "content": ai_message.content,
                    "timestamp": ai_message.timestamp,
                    "metadata": ai_message.metadata
                },
                session_id=session.id,
                sources=sources if sources else None
            )
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            db.rollback()
            raise
    
    def delete_session(self, db: Session, session_id: str) -> bool:
        """Delete a chat session and all its messages"""
        try:
            # Delete messages first
            db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
            
            # Delete session
            db.query(ChatSession).filter(ChatSession.id == session_id).delete()
            
            db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            db.rollback()
            return False

# Global instance
chat_service = ChatService()
