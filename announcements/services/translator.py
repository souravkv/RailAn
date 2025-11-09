"""
Translation service using Google Gemini API
"""
import logging
import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger(__name__)


class Translator:
    """Service for translating text using Google Gemini API"""
    
    # Language code mapping to full language names for Gemini
    LANGUAGE_NAMES = {
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'bn': 'Bengali',
        'kn': 'Kannada',
        'en': 'English',
    }
    
    def __init__(self, api_key=None):
        self.api_key = api_key or getattr(settings, 'GEMINI_API_KEY', None)
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY not configured. Translation will use fallback.")
    
    def translate(self, text, source_lang='auto', target_lang='hi'):
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            source_lang: Source language code (default: 'auto' for auto-detection)
            target_lang: Target language code (hi, ta, te, bn, kn, en)
            
        Returns:
            str: Translated text or original text if translation fails
        """
        if not text or not text.strip():
            return text
        
        # If source and target are the same, return original
        if source_lang != 'auto' and source_lang == target_lang:
            return text
        
        # If API key not configured, return original text
        if not self.model:
            logger.warning("Gemini API not configured. Returning original text.")
            return text
        
        try:
            # Get target language name
            target_language = self.LANGUAGE_NAMES.get(target_lang, 'English')
            
            # Build prompt for translation
            if source_lang == 'auto':
                prompt = f"Translate the following text to {target_language}. Only return the translated text, nothing else:\n\n{text}"
            else:
                source_language = self.LANGUAGE_NAMES.get(source_lang, 'English')
                prompt = f"Translate the following text from {source_language} to {target_language}. Only return the translated text, nothing else:\n\n{text}"
            
            # Generate translation
            response = self.model.generate_content(prompt)
            translated_text = response.text.strip()
            
            logger.info(f"Translated {source_lang} -> {target_lang}: {text[:50]}...")
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation request failed: {e}")
            # Return original text if translation fails
            return text
    
    def translate_multiple(self, text, source_lang='auto', target_languages=None):
        """
        Translate text to multiple languages.
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_languages: List of target language codes
            
        Returns:
            dict: Dictionary mapping language codes to translated texts
        """
        if target_languages is None:
            target_languages = ['hi', 'ta', 'te', 'bn', 'kn']
        
        translations = {}
        for lang in target_languages:
            translations[lang] = self.translate(text, source_lang, lang)
        
        return translations
    
    def is_available(self):
        """Check if Gemini API is available (checks if API key is configured)"""
        return self.model is not None and self.api_key is not None

