"""
Celery tasks for async processing of announcements
"""
import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import Announcement, Translation, AudioFile
from .services import LanguageDetector, Translator, TTSService
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Initialize services
language_detector = LanguageDetector()
translator = Translator()
tts_service = TTSService()


@shared_task(bind=True, max_retries=3)
def process_announcement(self, announcement_id):
    """
    Process an announcement: detect language, translate, generate audio.
    
    Args:
        announcement_id: ID of the announcement to process
    """
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        announcement.status = 'processing'
        announcement.save()
        
        # Step 1: Detect language if not already detected
        if not announcement.detected_language or announcement.detected_language == 'en':
            detected_lang = language_detector.detect_language(announcement.text)
            announcement.detected_language = detected_lang
            announcement.save()
            logger.info(f"Detected language: {detected_lang} for announcement {announcement_id}")
        
        # Step 2: Translate to all target languages
        target_languages = ['hi', 'ta', 'te', 'bn', 'kn']
        # Also include English if source is not English
        if announcement.detected_language != 'en':
            target_languages.append('en')
        
        # Translate to all target languages using Gemini API
        # If Gemini API is not available, it will return original text
        translations_dict = translator.translate_multiple(
            announcement.text,
            source_lang=announcement.detected_language,
            target_languages=target_languages
        )
        
        # Step 3: Save translations (even if translation failed, we save the original text)
        for lang_code, translated_text in translations_dict.items():
            # Only save if we got a translation (not empty)
            if translated_text and translated_text.strip():
                Translation.objects.update_or_create(
                    announcement=announcement,
                    language_code=lang_code,
                    defaults={
                        'translated_text': translated_text,
                        'translation_service': 'gemini' if translator.is_available() else 'fallback'
                    }
                )
            else:
                # Fallback: use original text if translation is empty
                Translation.objects.update_or_create(
                    announcement=announcement,
                    language_code=lang_code,
                    defaults={
                        'translated_text': announcement.text,
                        'translation_service': 'fallback'
                    }
                )
        
        # Step 4: Generate audio for all languages (including original)
        # Try to generate audio, but don't fail if TTS is not available
        all_languages = list(set([announcement.detected_language] + target_languages))
        audio_generated = False
        
        for lang_code in all_languages:
            try:
                # Get translation text or original text
                if lang_code == announcement.detected_language:
                    text_to_speak = announcement.text
                else:
                    translation = Translation.objects.filter(
                        announcement=announcement,
                        language_code=lang_code
                    ).first()
                    if translation:
                        text_to_speak = translation.translated_text
                    else:
                        text_to_speak = announcement.text
                
                # Generate audio file path
                audio_dir = Path(settings.MEDIA_ROOT) / 'audio' / timezone.now().strftime('%Y/%m/%d')
                audio_dir.mkdir(parents=True, exist_ok=True)
                audio_filename = f"announcement_{announcement_id}_{lang_code}.wav"
                audio_path = audio_dir / audio_filename
                
                # Generate audio (this may fail if TTS is not available, but we continue)
                success, service_used = tts_service.generate_audio(
                    text_to_speak,
                    lang_code,
                    str(audio_path)
                )
                
                if success:
                    # Get audio duration
                    duration = tts_service.get_audio_duration(str(audio_path))
                    
                    # Save audio file record
                    # Get translation if exists
                    translation = Translation.objects.filter(
                        announcement=announcement,
                        language_code=lang_code
                    ).first()
                    
                    AudioFile.objects.update_or_create(
                        announcement=announcement,
                        language_code=lang_code,
                        defaults={
                            'translation': translation,
                            'audio_file': f"audio/{timezone.now().strftime('%Y/%m/%d')}/{audio_filename}",
                            'duration_seconds': duration,
                            'tts_service': service_used,
                        }
                    )
                    logger.info(f"Generated audio for {lang_code}: {audio_path}")
                    audio_generated = True
                else:
                    logger.warning(f"Failed to generate audio for {lang_code} - TTS service may not be available")
            except Exception as e:
                logger.warning(f"Error generating audio for {lang_code}: {e}")
                # Continue with other languages even if one fails
        
        # Step 5: Mark as completed (even if audio generation failed)
        # We mark as completed if we have translations, even if audio failed
        announcement.status = 'completed'
        announcement.save()
        logger.info(f"Marked announcement {announcement_id} as completed")
        
        # Step 6: Notify via WebSocket
        notify_announcement_ready.delay(announcement_id)
        
        logger.info(f"Successfully processed announcement {announcement_id}")
        return f"Announcement {announcement_id} processed successfully"
        
    except Announcement.DoesNotExist:
        logger.error(f"Announcement {announcement_id} not found")
        return f"Announcement {announcement_id} not found"
    except Exception as e:
        logger.error(f"Error processing announcement {announcement_id}: {e}", exc_info=True)
        announcement.status = 'failed'
        announcement.error_message = str(e)
        announcement.save()
        # Retry the task
        raise self.retry(exc=e, countdown=60)


@shared_task
def notify_announcement_ready(announcement_id):
    """
    Notify all connected clients via WebSocket that an announcement is ready.
    
    Args:
        announcement_id: ID of the announcement
    """
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        channel_layer = get_channel_layer()
        
        # Prepare announcement data
        translations = {}
        for trans in announcement.translations.all():
            translations[trans.language_code] = {
                'text': trans.translated_text,
                'audio_url': None
            }
            # Get audio URL if available
            audio = AudioFile.objects.filter(
                announcement=announcement,
                language_code=trans.language_code
            ).first()
            if audio:
                translations[trans.language_code]['audio_url'] = audio.audio_file.url
        
        message = {
            'type': 'announcement_ready',
            'announcement': {
                'id': announcement.id,
                'text': announcement.text,
                'detected_language': announcement.detected_language,
                'status': announcement.status,
                'translations': translations,
                'created_at': announcement.created_at.isoformat(),
            }
        }
        
        # Send to all display board channels
        async_to_sync(channel_layer.group_send)(
            'display_boards',
            message
        )
        
        logger.info(f"Notified clients about announcement {announcement_id}")
        
    except Exception as e:
        logger.error(f"Error notifying about announcement {announcement_id}: {e}")

