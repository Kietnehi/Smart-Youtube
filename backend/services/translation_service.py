"""
Translation Service - Smart YouTube Analyzer
Handles text translation to Vietnamese and other languages
Updated for googletrans 4.0.2 (Async Support)
"""

import logging
import asyncio
import time
from typing import List, Dict, Optional
from googletrans import Translator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported languages for translation
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}


class TranslationService:
    """
    Manages text translation using Google Translate (googletrans library).
    Supports batch translation of transcript segments.
    """
    
    def __init__(self):
        """Initialize the translation service."""
        # Khởi tạo Translator (4.0.2 hỗ trợ tốt nhất khi dùng trong async)
        self.translator = Translator()
        self.batch_size = 15  # Tăng lên 15 để tối ưu tốc độ cho 4.0.2
        logger.info("Translation service initialized with googletrans 4.0.2 (Async)")
    
    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """Get all supported languages."""
        return LANGUAGES.copy()
    
    @staticmethod
    def validate_language(lang_code: str) -> bool:
        """Validate if a language code is supported."""
        return lang_code.lower() in LANGUAGES
    
    async def detect_language(self, text: str) -> Optional[Dict]:
        """
        Detect the language of a text.
        
        Args:
            text: Text to detect language from
            
        Returns:
            Dictionary with 'lang' and 'confidence' keys, or None if detection fails
        """
        if not text or not text.strip():
            return None
        
        try:
            detected = await self.translator.detect(text)
            return {
                'lang': detected.lang,
                'confidence': detected.confidence,
                'language_name': LANGUAGES.get(detected.lang, 'Unknown')
            }
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return None
    
    async def translate_text(self, text: str, target_lang: str = "vi", max_retries: int = 3) -> str:
        """
        Translate a single text string using googletrans library.
        """
        if not text or not text.strip():
            return text
            
        for attempt in range(max_retries):
            try:
                # Sử dụng await cho bản 4.0.2
                result = await self.translator.translate(
                    text, 
                    src='auto', 
                    dest=target_lang
                )
                
                if result and result.text:
                    return result.text
                else:
                    logger.warning(f"Empty translation result")
                    return text
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Translation error, retrying ({attempt + 1}/{max_retries}): {e}")
                    await asyncio.sleep(1) # Dùng asyncio.sleep thay cho time.sleep
                    self.translator = Translator()
                else:
                    logger.error(f"Translation failed after {max_retries} attempts: {e}")
                    return text
        
        return text 

    async def translate_batch(self, texts: List[str], target_lang: str = "vi") -> List[str]:
        """
        Translate multiple texts efficiently using googletrans bulk feature.
        """
        if not texts:
            return []
        
        try:
            # TỐI ƯU: Truyền cả List vào translator.translate thay vì chạy vòng lặp
            # Đây là cách nhanh nhất và ít bị chặn IP nhất
            results = await self.translator.translate(texts, dest=target_lang)
            
            # results sẽ là một list các object Translated
            return [res.text for res in results]
            
        except Exception as e:
            logger.error(f"Batch translation failed: {e}")
            # Fallback: Nếu lỗi bulk, thử dịch từng câu (hoặc trả về bản gốc)
            return texts
    
    async def translate_transcript(self, transcript: List[Dict], target_lang: str = "vi") -> List[Dict]:
        """
        Translate all segments in a transcript using batch processing.
        """
        logger.info(f"Translating {len(transcript)} segments to {target_lang}")
        
        translated = []
        
        # Sử dụng async context manager của googletrans 4.0.2
        async with Translator() as translator:
            self.translator = translator # Gán để dùng trong các hàm phụ nếu cần
            
            for i in range(0, len(transcript), self.batch_size):
                batch = transcript[i:i + self.batch_size]
                batch_texts = [seg["text"] for seg in batch]
                
                # Gọi hàm dịch batch (đã được tối ưu)
                translated_texts = await self.translate_batch(batch_texts, target_lang)
                
                # Combine với original metadata
                for j, segment in enumerate(batch):
                    translated.append({
                        "text": translated_texts[j],
                        "start": segment["start"],
                        "duration": segment["duration"],
                        # Preserve existing original if present; otherwise use incoming text
                        "original": segment.get("original", segment.get("text", ""))
                    })
                
                # Log progress
                progress = min(i + self.batch_size, len(transcript))
                logger.info(f"Translation progress: {progress}/{len(transcript)} segments")
                
                # Chờ một chút để tránh bị Google giới hạn (Rate limit)
                if i + self.batch_size < len(transcript):
                    await asyncio.sleep(0.5)
        
        logger.info(f"Translation complete: {len(translated)} segments")
        return translated
    
    # Synchronous wrappers for non-async contexts
    def translate_text_sync(self, text: str, target_lang: str = "vi", max_retries: int = 3) -> str:
        """Synchronous wrapper for translate_text."""
        return asyncio.run(self.translate_text(text, target_lang, max_retries))
    
    def translate_batch_sync(self, texts: List[str], target_lang: str = "vi") -> List[str]:
        """Synchronous wrapper for translate_batch."""
        return asyncio.run(self.translate_batch(texts, target_lang))
    
    def translate_transcript_sync(self, transcript: List[Dict], target_lang: str = "vi") -> List[Dict]:
        """Synchronous wrapper for translate_transcript."""
        return asyncio.run(self.translate_transcript(transcript, target_lang))
    
    def detect_language_sync(self, text: str) -> Optional[Dict]:
        """Synchronous wrapper for detect_language."""
        return asyncio.run(self.detect_language(text))


# Singleton instance
_translation_service = None

def get_translation_service() -> TranslationService:
    """Get or create the translation service singleton."""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service