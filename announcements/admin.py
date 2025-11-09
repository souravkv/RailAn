from django.contrib import admin
from .models import Announcement, Translation, AudioFile, DisplayBoard


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_preview', 'detected_language', 'status', 'priority', 'is_active', 'created_at', 'created_by']
    list_filter = ['status', 'is_active', 'detected_language', 'created_at']
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status', 'is_active', 'priority']
    
    fieldsets = (
        ('Announcement Details', {
            'fields': ('text', 'detected_language', 'status', 'priority', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'language_code', 'translated_text_preview', 'translation_service', 'created_at']
    list_filter = ['language_code', 'translation_service', 'created_at']
    search_fields = ['translated_text', 'announcement__text']
    readonly_fields = ['created_at']
    
    def translated_text_preview(self, obj):
        return obj.translated_text[:50] + '...' if len(obj.translated_text) > 50 else obj.translated_text
    translated_text_preview.short_description = 'Translated Text'


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'language_code', 'audio_file', 'duration_seconds', 'tts_service', 'created_at']
    list_filter = ['language_code', 'tts_service', 'created_at']
    search_fields = ['announcement__text']
    readonly_fields = ['created_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['audio_file']
        return self.readonly_fields


@admin.register(DisplayBoard)
class DisplayBoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'is_active', 'current_announcement', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['name', 'location']
    list_editable = ['is_active']
