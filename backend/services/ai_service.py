"""
AI Service - Smart YouTube Analyzer
Handles Gemini AI processing for summaries, chapters, and notes
"""

import os
import json
import logging
from typing import List, Dict
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIService:
    """
    Manages AI-powered analysis using Google Gemini 2.0 Flash.
    Generates summaries, chapters, and key notes from video transcripts.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the AI service with Gemini API.
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-3-flash-preview"  # Latest Flash model
        logger.info(f"AI Service initialized with model: {self.model_name}")
    
    def generate_summary(self, transcript: List[Dict]) -> str:
        """
        Generate a concise summary of the video content.
        
        Args:
            transcript: List of transcript segments
            
        Returns:
            Text summary of the video
        """
        # Combine transcript into full text
        full_text = self._combine_transcript(transcript)
        
        prompt = f"""You are an expert at summarizing video content. 
Analyze the following video transcript and provide a concise, well-structured summary 
that captures the main ideas, key points, and overall message.

**Instructions:**
- Write in clear, professional language
- Highlight the most important information
- Keep it between 150-300 words
- Use bullet points for key takeaways if appropriate

**Transcript:**
{full_text}

**Summary:**"""
        
        try:
            logger.info("Generating summary with Gemini...")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            summary = response.text.strip()
            logger.info(f"Summary generated successfully ({len(summary)} characters)")
            return summary
            
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            raise
    
    def generate_analysis(self, transcript: List[Dict]) -> Dict:
        """
        Generate structured analysis with chapters and key notes.
        
        Args:
            transcript: List of transcript segments
            
        Returns:
            Dict containing 'chapters' and 'key_notes'
        """
        full_text = self._combine_transcript_with_timestamps(transcript)
        
        prompt = f"""You are an expert video content analyzer. Analyze this transcript and create:

1. **CHAPTERS**: A timeline of main topics/sections with timestamps
2. **KEY NOTES**: Important points, facts, or insights with their timestamps

**Output Format** (STRICT JSON):
{{
    "chapters": [
        {{"timestamp": "0:00", "title": "Introduction"}},
        {{"timestamp": "2:30", "title": "Main Topic Begins"}},
        {{"timestamp": "5:45", "title": "Key Concept Explained"}}
    ],
    "key_notes": [
        {{"time": "0:15", "note": "Speaker introduces the main theme"}},
        {{"time": "3:20", "note": "Important statistic: 85% growth"}},
        {{"time": "6:10", "note": "Key takeaway: Always test before deployment"}}
    ]
}}

**Guidelines:**
- Create 5-10 chapters (major sections only)
- Create 8-15 key notes (most valuable insights)
- Use exact timestamp format: "M:SS" or "H:MM:SS"
- Keep titles/notes concise but descriptive
- Return ONLY valid JSON, no markdown or extra text

**Transcript with Timestamps:**
{full_text}

**JSON Output:**"""
        
        try:
            logger.info("Generating analysis with Gemini...")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Clean markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            analysis = json.loads(response_text.strip())
            
            # Validate structure
            if "chapters" not in analysis or "key_notes" not in analysis:
                raise ValueError("Invalid analysis structure")
            
            logger.info(f"Analysis generated: {len(analysis['chapters'])} chapters, "
                       f"{len(analysis['key_notes'])} notes")
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response_text[:500]}")
            # Return fallback structure
            return {
                "chapters": [{"timestamp": "0:00", "title": "Full Video"}],
                "key_notes": [{"time": "0:00", "note": "Analysis unavailable"}]
            }
        except Exception as e:
            logger.error(f"Analysis generation failed: {e}")
            raise
    
    def _combine_transcript(self, transcript: List[Dict]) -> str:
        """
        Combine transcript segments into a single text.
        
        Args:
            transcript: List of transcript segments
            
        Returns:
            Combined text
        """
        return " ".join([seg["text"] for seg in transcript])
    
    def _combine_transcript_with_timestamps(self, transcript: List[Dict]) -> str:
        """
        Combine transcript with timestamps for analysis.
        
        Args:
            transcript: List of transcript segments
            
        Returns:
            Formatted text with timestamps
        """
        lines = []
        for seg in transcript:
            timestamp = self._format_timestamp(seg["start"])
            lines.append(f"[{timestamp}] {seg['text']}")
        
        return "\n".join(lines)
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Convert seconds to timestamp format (M:SS or H:MM:SS).
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted timestamp
        """
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"


# Singleton instance
_ai_service = None

def get_ai_service() -> AIService:
    """Get or create the AI service singleton."""
    global _ai_service
    if _ai_service is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        _ai_service = AIService(api_key=api_key)
    return _ai_service
