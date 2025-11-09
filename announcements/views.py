"""
Views for RailAnnounce application
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Announcement, Translation, AudioFile, DisplayBoard
from .tasks import process_announcement
from .services import LanguageDetector

language_detector = LanguageDetector()


def home(request):
    """Home page"""
    return render(request, 'announcements/home.html')


def create_announcement(request):
    """Create a new announcement"""
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        priority = int(request.POST.get('priority', 5))
        
        if not text:
            messages.error(request, 'Please enter announcement text')
            return redirect('announcements:create_announcement')
        
        # Create announcement
        announcement = Announcement.objects.create(
            text=text,
            detected_language=language_detector.detect_language(text),
            priority=priority,
            created_by=request.user if request.user.is_authenticated else None,
            status='pending'
        )
        
        # Start async processing
        process_announcement.delay(announcement.id)
        
        messages.success(request, f'Announcement #{announcement.id} created and is being processed')
        return redirect('announcements:announcement_detail', announcement_id=announcement.id)
    
    return render(request, 'announcements/create_announcement.html')


def announcement_detail(request, announcement_id):
    """View announcement details"""
    announcement = get_object_or_404(Announcement, id=announcement_id)
    translations = announcement.translations.all()
    audio_files = announcement.audio_files.all()
    
    context = {
        'announcement': announcement,
        'translations': translations,
        'audio_files': audio_files,
    }
    return render(request, 'announcements/announcement_detail.html', context)


def announcement_list(request):
    """List all announcements"""
    announcements = Announcement.objects.all().order_by('-created_at')[:50]
    context = {
        'announcements': announcements,
    }
    return render(request, 'announcements/announcement_list.html', context)


def display_board(request, board_id=None):
    """Display board view for showing announcements"""
    if board_id:
        board = get_object_or_404(DisplayBoard, id=board_id)
    else:
        # Get first active board or create default
        board = DisplayBoard.objects.filter(is_active=True).first()
        if not board:
            board = DisplayBoard.objects.create(name='Default Board', is_active=True)
    
    # Get active announcements (show all statuses except failed)
    # Order by: completed first, then by priority and date
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
    
    context = {
        'board': board,
        'announcements': announcements,
    }
    return render(request, 'announcements/display_board.html', context)


@require_http_methods(["GET"])
def api_announcement_status(request, announcement_id):
    """API endpoint to check announcement status"""
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    translations = {}
    for trans in announcement.translations.all():
        translations[trans.language_code] = {
            'text': trans.translated_text,
            'audio_url': None
        }
        audio = AudioFile.objects.filter(
            announcement=announcement,
            language_code=trans.language_code
        ).first()
        if audio:
            translations[trans.language_code]['audio_url'] = audio.audio_file.url
    
    return JsonResponse({
        'id': announcement.id,
        'text': announcement.text,
        'detected_language': announcement.detected_language,
        'status': announcement.status,
        'translations': translations,
        'created_at': announcement.created_at.isoformat(),
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_create_announcement(request):
    """API endpoint to create announcement (for HTMX)"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        priority = int(data.get('priority', 5))
        
        if not text:
            return JsonResponse({'error': 'Text is required'}, status=400)
        
        # Create announcement
        announcement = Announcement.objects.create(
            text=text,
            detected_language=language_detector.detect_language(text),
            priority=priority,
            status='pending'
        )
        
        # Start async processing
        process_announcement.delay(announcement.id)
        
        return JsonResponse({
            'id': announcement.id,
            'status': 'pending',
            'message': 'Announcement created and is being processed'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
