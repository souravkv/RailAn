from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class Announcement(models.Model):
    """Main announcement model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Basic information
    text = models.TextField(help_text="Original announcement text")
    detected_language = models.CharField(max_length=10, default='en', help_text="Auto-detected language code")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Priority and display
    priority = models.IntegerField(default=5, help_text="Priority level (1-10, higher = more important)")
    is_active = models.BooleanField(default=True, help_text="Whether this announcement is currently active")
    is_urgent = models.BooleanField(default=False, help_text="Whether this is an urgent announcement")
    
    # Error tracking
    error_message = models.TextField(blank=True, null=True, help_text="Error message if processing failed")
    
    # Email notification tracking
    email_sent = models.BooleanField(default=False, help_text="Whether email notifications were sent")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['is_active', '-priority', '-created_at']),
        ]
    
    def __str__(self):
        return f"Announcement #{self.id} - {self.text[:50]}..."


class Translation(models.Model):
    """Stores translations of announcements in different languages"""
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='translations')
    language_code = models.CharField(max_length=10, help_text="Target language code (hi, ta, te, bn, kn, en)")
    translated_text = models.TextField(help_text="Translated text")
    
    # Translation metadata
    created_at = models.DateTimeField(default=timezone.now)
    translation_service = models.CharField(max_length=50, default='libretranslate', help_text="Service used for translation")
    
    class Meta:
        unique_together = ['announcement', 'language_code']
        indexes = [
            models.Index(fields=['announcement', 'language_code']),
        ]
    
    def __str__(self):
        return f"{self.announcement.id} -> {self.language_code}: {self.translated_text[:50]}..."


class AudioFile(models.Model):
    """Stores generated audio files for announcements"""
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='audio_files')
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE, related_name='audio_files', null=True, blank=True)
    language_code = models.CharField(max_length=10, help_text="Language of the audio")
    
    # Audio file
    audio_file = models.FileField(upload_to='audio/%Y/%m/%d/', help_text="Generated audio file")
    duration_seconds = models.FloatField(null=True, blank=True, help_text="Duration of audio in seconds")
    
    # TTS metadata
    tts_service = models.CharField(max_length=50, default='coqui', help_text="TTS service used (coqui, pyttsx3)")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['announcement', 'language_code']
        indexes = [
            models.Index(fields=['announcement', 'language_code']),
        ]
    
    def __str__(self):
        return f"Audio: {self.announcement.id} - {self.language_code}"


class DisplayBoard(models.Model):
    """Manages display boards for showing announcements"""
    name = models.CharField(max_length=100, help_text="Display board name/identifier")
    location = models.CharField(max_length=200, blank=True, help_text="Physical location of the board")
    is_active = models.BooleanField(default=True, help_text="Whether this board is currently active")
    current_announcement = models.ForeignKey(
        Announcement, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='active_boards'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"Display Board: {self.name}"
