from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# Document Models
class DocumentUpload(BaseModel):
    filename: str
    content: str
    file_type: str
    file_size: int
    metadata: Optional[Dict[str, Any]] = None

class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    file_type: str
    file_size: int
    upload_date: datetime
    processed: bool
    metadata: Optional[str] = None

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int

# Chat Models
class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[UUID] = None

class ChatMessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    timestamp: datetime
    metadata: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: UUID
    session_name: str
    created_at: datetime
    last_activity: datetime
    is_active: bool

class ChatResponse(BaseModel):
    message: ChatMessageResponse
    session_id: UUID
    sources: Optional[List[Dict[str, Any]]] = None

# Text Processing Models
class TextSummarizeRequest(BaseModel):
    text: str
    max_length: Optional[int] = 150
    min_length: Optional[int] = 30

class TextSummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int

class SentimentAnalysisRequest(BaseModel):
    text: str

class SentimentAnalysisResponse(BaseModel):
    sentiment: str  # positive, negative, neutral
    confidence: float
    scores: Dict[str, float]

# Error Models
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
