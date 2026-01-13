"""
Transcript Service - Smart YouTube Analyzer
Handles transcript extraction with fallback mechanisms
"""

import os
import tempfile
from typing import List, Dict, Optional
import importlib
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import yt_dlp
import whisper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TranscriptService:
    """
    Manages transcript extraction with a two-tier approach:
    1. Primary: YouTube's official transcript API
    2. Fallback: Audio download + Whisper transcription
    """
    
    def __init__(self, whisper_model_size: str = "base"):
        """
        Initialize the transcript service.
        
        Args:
            whisper_model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.whisper_model_size = whisper_model_size
        self.whisper_model = None  # Lazy loading
        
    def get_transcript(self, video_id: str) -> Dict:
        """
        Get transcript for a YouTube video with fallback strategy.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dict with 'transcript' (list) and 'source' (str)
        """
        # Try primary method first
        try:
            logger.info(f"Attempting primary transcript fetch for video: {video_id}")
            transcript = self._fetch_youtube_transcript(video_id)
            return {
                "transcript": transcript,
                "source": "youtube_api",
                "success": True
            }
        except Exception as e:
            # Catch any error from the primary method and fall back to Whisper
            logger.warning(f"Primary method failed: {type(e).__name__}: {e}. Trying fallback...")
            
        # Fallback to Whisper
        try:
            logger.info(f"Using Whisper fallback for video: {video_id}")
            transcript = self._transcribe_with_whisper(video_id)
            return {
                "transcript": transcript,
                "source": "whisper",
                "success": True
            }
        except Exception as e:
            logger.error(f"Fallback transcription failed: {e}")
            return {
                "transcript": [],
                "source": "error",
                "success": False,
                "error": str(e)
            }
    
    def _fetch_youtube_transcript(self, video_id: str) -> List[Dict]:
        """
        Fetch transcript using YouTube's official API.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            List of transcript segments in normalized format
        """
        # Fetch transcript - try multiple call patterns to support different library versions
        transcript_list = None
        yta = importlib.import_module('youtube_transcript_api')

        # 1) Module-level helper (get_transcript)
        try:
            if hasattr(yta, 'get_transcript'):
                transcript_list = yta.get_transcript(video_id, languages=['en'])
        except Exception:
            transcript_list = None

        # 2) Class method or callable on YouTubeTranscriptApi
        if transcript_list is None:
            try:
                YT = getattr(yta, 'YouTubeTranscriptApi', None)
                if YT is not None and hasattr(YT, 'get_transcript'):
                    transcript_list = YT.get_transcript(video_id, languages=['en'])
                else:
                    # Try instance method
                    instance = YT()
                    if hasattr(instance, 'get_transcript'):
                        transcript_list = instance.get_transcript(video_id, languages=['en'])
            except Exception:
                transcript_list = None

        # 3) As a last resort, try calling without language constraints
        if transcript_list is None:
            try:
                if hasattr(yta, 'get_transcript'):
                    transcript_list = yta.get_transcript(video_id)
            except Exception:
                transcript_list = None

        if transcript_list is None:
            raise RuntimeError('Unable to obtain transcript via youtube_transcript_api')
        
        # Normalize format
        normalized = []
        for segment in transcript_list:
            normalized.append({
                "text": segment["text"],
                "start": segment["start"],
                "duration": segment.get("duration", 0)
            })
        
        logger.info(f"Successfully fetched {len(normalized)} transcript segments")
        return normalized
    
    def _transcribe_with_whisper(self, video_id: str) -> List[Dict]:
        """
        Transcribe video using Whisper (fallback method).
        
        Steps:
        1. Download audio with yt-dlp
        2. Transcribe with Whisper
        3. Format to normalized output
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            List of transcript segments
        """
        # Step 1: Download audio
        audio_path = self._download_audio(video_id)
        
        try:
            # Step 2: Load Whisper model (lazy loading)
            if self.whisper_model is None:
                logger.info(f"Loading Whisper model: {self.whisper_model_size}")
                self.whisper_model = whisper.load_model(self.whisper_model_size)
            
            # Step 3: Transcribe
            logger.info(f"Transcribing audio file: {audio_path}")
            result = self.whisper_model.transcribe(audio_path, verbose=False)
            
            # Step 4: Format output
            normalized = []
            for segment in result["segments"]:
                normalized.append({
                    "text": segment["text"].strip(),
                    "start": segment["start"],
                    "duration": segment["end"] - segment["start"]
                })
            
            logger.info(f"Whisper transcription complete: {len(normalized)} segments")
            return normalized
            
        finally:
            # Cleanup: Remove temporary audio file
            if os.path.exists(audio_path):
                os.remove(audio_path)
                logger.info(f"Cleaned up audio file: {audio_path}")
    
    def _download_audio(self, video_id: str) -> str:
        """
        Download audio from YouTube using yt-dlp.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Path to downloaded audio file
        """
        temp_dir = os.getenv("TEMP_DIR", "./temp_audio")
        os.makedirs(temp_dir, exist_ok=True)
        
        output_path = os.path.join(temp_dir, f"{video_id}.mp3")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(temp_dir, f"{video_id}.%(ext)s"),
            'quiet': True,
            'no_warnings': True
        }
        
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        logger.info(f"Downloading audio for video: {video_id}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Audio file not found after download: {output_path}")
        
        logger.info(f"Audio downloaded successfully: {output_path}")
        return output_path


# Singleton instance
_transcript_service = None

def get_transcript_service() -> TranscriptService:
    """Get or create the transcript service singleton."""
    global _transcript_service
    if _transcript_service is None:
        whisper_model = os.getenv("WHISPER_MODEL", "base")
        _transcript_service = TranscriptService(whisper_model_size=whisper_model)
    return _transcript_service
