from fastapi import APIRouter, HTTPException
from app.models import (
    TextSummarizeRequest, 
    TextSummarizeResponse,
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
    ErrorResponse
)
from app.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/text", tags=["text-processing"])

@router.post("/summarize", response_model=TextSummarizeResponse)
async def summarize_text(request: TextSummarizeRequest):
    """Summarize text using AI"""
    try:
        summary = llm_service.summarize_text(
            request.text, 
            request.max_length, 
            request.min_length
        )
        
        return TextSummarizeResponse(
            summary=summary,
            original_length=len(request.text),
            summary_length=len(summary)
        )
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sentiment", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """Analyze sentiment of text using AI"""
    try:
        result = llm_service.analyze_sentiment(request.text)
        
        return SentimentAnalysisResponse(
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            scores=result["scores"]
        )
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))
