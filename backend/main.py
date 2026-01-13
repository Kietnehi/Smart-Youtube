"""
Smart YouTube Analyzer - FastAPI Backend
Main application entry point
"""

import os
import re
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Import services
from services.transcript_service import get_transcript_service
from services.ai_service import get_ai_service
from services.translation_service import get_translation_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Smart YouTube Analyzer API",
    description="AI-powered YouTube video analysis with transcription and summarization",
    version="1.0.0"
)

# CORS Configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Request/Response Models ====================

class VideoRequest(BaseModel):
    """Request model for video URL/ID"""
    video_url: str
    
    @validator('video_url')
    def extract_video_id(cls, v):
        """Extract video ID from URL or validate ID format"""
        # Pattern for YouTube URLs
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'^([a-zA-Z0-9_-]{11})$'  # Direct video ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, v)
            if match:
                return match.group(1)
        
        raise ValueError("Invalid YouTube URL or video ID")


class TranscriptResponse(BaseModel):
    """Response model for transcript data"""
    video_id: str
    transcript: List[Dict]
    source: str
    success: bool
    error: Optional[str] = None


class SummaryRequest(BaseModel):
    """Request model for summary generation"""
    transcript: List[Dict]


class SummaryResponse(BaseModel):
    """Response model for summary"""
    summary: str
    success: bool


class AnalysisRequest(BaseModel):
    """Request model for detailed analysis"""
    transcript: List[Dict]


class AnalysisResponse(BaseModel):
    """Response model for analysis"""
    chapters: List[Dict]
    key_notes: List[Dict]
    success: bool


class TranslationRequest(BaseModel):
    """Request model for translation"""
    transcript: List[Dict]
    target_lang: str = "vi"


class TranslationResponse(BaseModel):
    """Response model for translation"""
    translated_transcript: List[Dict]
    success: bool


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Smart YouTube Analyzer API",
        "version": "1.0.0"
    }


@app.post("/api/transcript", response_model=TranscriptResponse)
async def get_transcript(request: VideoRequest):
    """
    Extract transcript from YouTube video.
    
    **Process:**
    1. Try youtube-transcript-api (fast, official)
    2. Fallback to yt-dlp + Whisper (slower, reliable)
    
    **Returns:**
    - transcript: List of segments [{text, start, duration}]
    - source: "youtube_api" or "whisper"
    """
    try:
        video_id = request.video_url
        logger.info(f"Transcript request for video: {video_id}")
        
        # Get transcript service
        service = get_transcript_service()
        result = service.get_transcript(video_id)
        
        return TranscriptResponse(
            video_id=video_id,
            transcript=result["transcript"],
            source=result["source"],
            success=result["success"],
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Transcript endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summary", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest):
    """
    Generate AI-powered summary of video content.
    
    **Uses:** Google Gemini 2.0 Flash
    
    **Returns:**
    - Concise summary (150-300 words)
    - Key takeaways
    """
    try:
        logger.info("Summary generation request received")
        
        if not request.transcript:
            raise ValueError("Transcript cannot be empty")
        
        # Get AI service
        ai_service = get_ai_service()
        summary = ai_service.generate_summary(request.transcript)
        
        return SummaryResponse(
            summary=summary,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Summary endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_video(request: AnalysisRequest):
    """
    Generate structured analysis with chapters and key notes.
    
    **Uses:** Google Gemini 2.0 Flash
    
    **Returns:**
    - chapters: Timeline of main topics [{timestamp, title}]
    - key_notes: Important points [{time, note}]
    """
    try:
        logger.info("Analysis request received")
        
        if not request.transcript:
            raise ValueError("Transcript cannot be empty")
        
        # Get AI service
        ai_service = get_ai_service()
        analysis = ai_service.generate_analysis(request.transcript)
        
        return AnalysisResponse(
            chapters=analysis["chapters"],
            key_notes=analysis["key_notes"],
            success=True
        )
        
    except Exception as e:
        logger.error(f"Analysis endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/translate", response_model=TranslationResponse)
async def translate_transcript(request: TranslationRequest):
    """
    Translate transcript to target language (default: Vietnamese).
    
    **Supports:** All Google Translate languages
    
    **Returns:**
    - Translated transcript with original timestamps
    """
    try:
        logger.info(f"Translation request: {len(request.transcript)} segments to {request.target_lang}")
        
        if not request.transcript:
            raise ValueError("Transcript cannot be empty")
        
        # Get translation service and await its async translate method
        translation_service = get_translation_service()
        translated = await translation_service.translate_transcript(
            request.transcript,
            request.target_lang
        )
        
        return TranslationResponse(
            translated_transcript=translated,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Translation endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/languages")
async def get_supported_languages():
    """Return supported translation languages."""
    try:
        translation_service = get_translation_service()
        langs = translation_service.get_supported_languages()
        return {"languages": langs}
    except Exception as e:
        logger.error(f"Languages endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Run Server ====================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
