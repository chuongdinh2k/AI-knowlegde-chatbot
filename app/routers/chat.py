from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import (
    ChatMessageRequest, 
    ChatResponse, 
    ChatSessionResponse,
    ErrorResponse
)
from app.services.chat_service import chat_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_name: str = "New Chat",
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    try:
        session = chat_service.create_session(db, session_name)
        return session
    except Exception as e:
        logger.error(f"Error creating chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def list_chat_sessions(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all chat sessions"""
    try:
        sessions = chat_service.get_sessions(db, limit)
        return sessions
    except Exception as e:
        logger.error(f"Error listing chat sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific chat session"""
    try:
        session = chat_service.get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}/messages")
async def get_chat_messages(
    session_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get messages for a chat session"""
    try:
        messages = chat_service.get_messages(db, session_id, limit)
        return {"messages": messages}
    except Exception as e:
        logger.error(f"Error getting chat messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """Send a message and get AI response"""
    try:
        response = chat_service.send_message(db, request)
        return response
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Delete a chat session and all its messages"""
    try:
        success = chat_service.delete_session(db, session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found or could not be deleted")
        
        return {"message": "Session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
