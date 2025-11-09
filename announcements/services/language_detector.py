"""
Language detection service using langdetect
"""
from langdetect import detect, LangDetectException
import logging

logger = logging.getLogger(__name__)


class LanguageDetector:
    """Service for detecting the language of text"""
    
    LANGUAGE_MAPPING = {
        'hi': 'hi',  # Hindi
        'ta': 'ta',  # Tamil
        'te': 'te',  # Telugu
        'bn': 'bn',  # Bengali
        'kn': 'kn',  # Kannada
        'en': 'en',  # English
    }
    
    @staticmethod
    def detect_language(text):
        """
        Detect the language of the given text.
        
        Args:
            text: Text to detect language for
            
        Returns:
            str: Language code (defaults to 'en' if detection fails)
        """
        if not text or not text.strip():
            return 'en'
        
        try:
            detected = detect(text)
            # Map to our supported languages or default to English
            return LanguageDetector.LANGUAGE_MAPPING.get(detected, 'en')
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}. Defaulting to 'en'")
            return 'en'
        except Exception as e:
            logger.error(f"Unexpected error in language detection: {e}. Defaulting to 'en'")
            return 'en'

