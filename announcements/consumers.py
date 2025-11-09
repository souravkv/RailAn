"""
WebSocket consumers for real-time announcement updates
"""
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Announcement, Translation, AudioFile

logger = logging.getLogger(__name__)


class DisplayBoardConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for display board updates"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.group_name = 'display_boards'
        
        # Join display board group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"Display board connected: {self.channel_name}")
        
        # Send current active announcements
        await self.send_current_announcements()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave display board group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"Display board disconnected: {self.channel_name}")
    
    async def receive(self, text_data):
        """Handle messages from WebSocket client"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'get_current':
                # Send current active announcements
                await self.send_current_announcements()
            elif message_type == 'subscribe':
                # Subscribe to specific announcement
                announcement_id = data.get('announcement_id')
                if announcement_id:
                    await self.subscribe_to_announcement(announcement_id)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received from WebSocket")
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
    
    async def announcement_ready(self, event):
        """Handle announcement_ready event from channel layer"""
        announcement_data = event.get('announcement', {})
        
        # Send announcement data to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'announcement_ready',
            'announcement': announcement_data
        }))
    
    async def send_current_announcements(self):
        """Send current active announcements to client"""
        announcements = await self.get_active_announcements()
        
        await self.send(text_data=json.dumps({
            'type': 'current_announcements',
            'announcements': announcements
        }))
    
    @database_sync_to_async
    def get_active_announcements(self):
        """Get active announcements from database"""
        from django.db.models import Case, When, IntegerField
        
        announcements = Announcement.objects.filter(
            is_active=True
        ).exclude(status='failed').annotate(
            status_order=Case(
                When(status='completed', then=1),
                When(status='processing', then=2),
                When(status='pending', then=3),
                default=4,
                output_field=IntegerField()
            )
        ).order_by('status_order', '-priority', '-created_at')[:10]
        
        result = []
        for ann in announcements:
            translations = {}
            for trans in ann.translations.all():
                translations[trans.language_code] = {
                    'text': trans.translated_text,
                    'audio_url': None
                }
                # Get audio URL
                audio = AudioFile.objects.filter(
                    announcement=ann,
                    language_code=trans.language_code
                ).first()
                if audio:
                    translations[trans.language_code]['audio_url'] = audio.audio_file.url
            
            result.append({
                'id': ann.id,
                'text': ann.text,
                'detected_language': ann.detected_language,
                'translations': translations,
                'priority': ann.priority,
                'created_at': ann.created_at.isoformat(),
            })
        
        return result
    
    async def subscribe_to_announcement(self, announcement_id):
        """Subscribe to updates for a specific announcement"""
        # Add to announcement-specific group
        await self.channel_layer.group_add(
            f'announcement_{announcement_id}',
            self.channel_name
        )

