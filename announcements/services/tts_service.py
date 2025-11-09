"""
Text-to-Speech service using Coqui TTS (primary) and pyttsx3 (fallback)
"""
import os
import logging
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)


class TTSService:
    """Service for generating speech from text"""
    
    def __init__(self):
        self.coqui_available = False
        self.pyttsx3_available = False
        self._init_coqui()
        self._init_pyttsx3()
    
    def _init_coqui(self):
        """Initialize Coqui TTS"""
        try:
            # Try to import TTS (may not be installed)
            try:
                from TTS.api import TTS
            except ImportError:
                logger.info("Coqui TTS not installed. Using pyttsx3 as fallback.")
                self.coqui_available = False
                return
            
            self.coqui_available = True
            # Initialize TTS model (lazy loading)
            self.coqui_tts = None
            self._current_model = None
            logger.info("Coqui TTS available")
        except Exception as e:
            logger.warning(f"Error initializing Coqui TTS: {e}. Using pyttsx3 as fallback.")
            self.coqui_available = False
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 as fallback"""
        try:
            import pyttsx3
            self.pyttsx3_available = True
            self.pyttsx3_engine = pyttsx3.init()
            # Configure pyttsx3
            self.pyttsx3_engine.setProperty('rate', 150)  # Speech rate
            self.pyttsx3_engine.setProperty('volume', 0.9)  # Volume
            logger.info("pyttsx3 TTS available")
        except Exception as e:
            logger.warning(f"pyttsx3 not available: {e}")
            self.pyttsx3_available = False
    
    def _get_coqui_model(self, language_code):
        """Get appropriate Coqui TTS model for language"""
        if not self.coqui_available:
            return None
        
        try:
            from TTS.api import TTS
            
            # Map language codes to Coqui TTS models
            model_map = {
                'en': 'tts_models/en/ljspeech/tacotron2-DDC',
                'hi': 'tts_models/hi/cv/vits',  # Common Voice Hindi
                'ta': 'tts_models/ta/cv/vits',  # Common Voice Tamil
                'te': 'tts_models/te/cv/vits',  # Common Voice Telugu
                'bn': 'tts_models/bn/cv/vits',  # Common Voice Bengali
                'kn': 'tts_models/kn/cv/vits',  # Common Voice Kannada
            }
            
            model_name = model_map.get(language_code, 'tts_models/en/ljspeech/tacotron2-DDC')
            
            if self.coqui_tts is None or getattr(self, '_current_model', None) != model_name:
                self.coqui_tts = TTS(model_name)
                self._current_model = model_name
            
            return self.coqui_tts
        except Exception as e:
            logger.error(f"Error getting Coqui model: {e}")
            return None
    
    def _language_to_pyttsx3_voice(self, language_code):
        """Map language code to pyttsx3 voice"""
        # pyttsx3 voice selection varies by system
        # This is a basic implementation
        voice_map = {
            'en': 'english',
            'hi': 'hindi',
            'ta': 'tamil',
            'te': 'telugu',
            'bn': 'bengali',
            'kn': 'kannada',
        }
        return voice_map.get(language_code, 'english')
    
    def generate_audio_coqui(self, text, language_code, output_path):
        """Generate audio using Coqui TTS"""
        try:
            tts = self._get_coqui_model(language_code)
            if tts is None:
                return False
            
            # Ensure output directory exists
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate audio
            tts.tts_to_file(text=text, file_path=str(output_path))
            logger.info(f"Generated audio with Coqui TTS: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Coqui TTS generation failed: {e}")
            return False
    
    def generate_audio_pyttsx3(self, text, language_code, output_path):
        """Generate audio using pyttsx3 (fallback)"""
        try:
            if not self.pyttsx3_available:
                return False
            
            # Ensure output directory exists
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Try to set voice (may not work on all systems)
            try:
                voices = self.pyttsx3_engine.getProperty('voices')
                # Simple voice selection (implementation varies by OS)
                # For now, use default voice
            except Exception:
                pass
            
            # Save to file
            self.pyttsx3_engine.save_to_file(text, str(output_path))
            self.pyttsx3_engine.runAndWait()
            
            logger.info(f"Generated audio with pyttsx3: {output_path}")
            return True
        except Exception as e:
            logger.error(f"pyttsx3 TTS generation failed: {e}")
            return False
    
    def generate_audio(self, text, language_code, output_path):
        """
        Generate audio file from text.
        
        Args:
            text: Text to convert to speech
            language_code: Language code (hi, ta, te, bn, kn, en)
            output_path: Path to save audio file
            
        Returns:
            tuple: (success: bool, service_used: str)
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for TTS")
            return False, None
        
        # Try Coqui TTS first
        if self.coqui_available:
            if self.generate_audio_coqui(text, language_code, output_path):
                return True, 'coqui'
        
        # Fallback to pyttsx3
        if self.pyttsx3_available:
            if self.generate_audio_pyttsx3(text, language_code, output_path):
                return True, 'pyttsx3'
        
        logger.error("No TTS service available")
        return False, None
    
    def get_audio_duration(self, audio_path):
        """Get duration of audio file in seconds"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # Convert milliseconds to seconds
        except Exception as e:
            logger.warning(f"Could not get audio duration: {e}")
            return None

