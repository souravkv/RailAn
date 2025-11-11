"""
Views for RailAnnounce application
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import json
import logging

logger = logging.getLogger(__name__)

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
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        text = request.POST.get('text', '').strip()
        handler = request.POST.get('handler', '').strip()
        announcement_time = request.POST.get('announcement_time', '').strip()
        location = request.POST.get('location', '').strip()
        contact_no = request.POST.get('contact_no', '').strip()
        priority = int(request.POST.get('priority', 5))
        email_recipients = request.POST.get('email_recipients', '').strip()
        
        if not text:
            messages.error(request, 'Please enter announcement text')
            return redirect('announcements:create_announcement')
        
        # Parse datetime if provided
        from django.utils.dateparse import parse_datetime
        parsed_time = None
        if announcement_time:
            parsed_time = parse_datetime(announcement_time)
        
        # Create announcement
        announcement = Announcement.objects.create(
            title=title,
            description=description,
            text=text,
            handler=handler,
            announcement_time=parsed_time,
            location=location,
            contact_no=contact_no,
            detected_language=language_detector.detect_language(text),
            priority=priority,
            created_by=request.user if request.user.is_authenticated else None,
            status='pending',
            email_sent=False,  # Set the default value for email_sent
            is_urgent=False  # Set the default value for is_urgent
        )
        
        # Send email notifications if recipients provided
        email_status = None
        if email_recipients:
            if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                email_status = "Email configuration not set. Please set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD environment variables."
                logger.warning("Email sending attempted but credentials not configured")
                messages.warning(request, f'Announcement #{announcement.id} created. Email not sent: Email configuration not set.')
            else:
                try:
                    # Parse email addresses (comma-separated)
                    email_list = [email.strip() for email in email_recipients.split(',') if email.strip()]
                    
                    if email_list:
                        subject = f'New Railway Announcement: {title or f"Announcement #{announcement.id}"}'
                        
                        # Create email body
                        email_body = f"""
New Railway Announcement Created

{'Title: ' + title if title else 'Announcement #' + str(announcement.id)}

{'Description: ' + description if description else ''}

Announcement Text:
{text}

{'Handler: ' + handler if handler else ''}
{'Location: ' + location if location else ''}
{'Time: ' + announcement_time if announcement_time else ''}
{'Contact: ' + contact_no if contact_no else ''}
Priority: {priority}

Status: {announcement.get_status_display()}
Language: {announcement.detected_language.upper()}

View full details: {request.build_absolute_uri(f'/announcements/{announcement.id}/')}

---
RailAnnounce System
"""
                        
                        logger.info(f"Attempting to send email to: {email_list}")
                        logger.info(f"From: {settings.DEFAULT_FROM_EMAIL}")
                        
                        result = send_mail(
                            subject=subject,
                            message=email_body,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=email_list,
                            fail_silently=False,
                        )
                        
                        logger.info(f"Email send result: {result}")
                        logger.info(f"Email sent successfully to {len(email_list)} recipient(s)")
                        
                        announcement.email_sent = True
                        announcement.save()
                        
                        messages.success(request, f'Announcement #{announcement.id} created and email sent to {len(email_list)} recipient(s): {", ".join(email_list)}')
                        email_status = f"Email sent successfully to {len(email_list)} recipient(s)"
                    else:
                        messages.success(request, f'Announcement #{announcement.id} created and is being processed')
                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"Email sending failed: {error_msg}", exc_info=True)
                    email_status = f"Email sending failed: {error_msg}"
                    messages.error(request, f'Announcement #{announcement.id} created but email sending failed: {error_msg}')
        else:
            messages.success(request, f'Announcement #{announcement.id} created and is being processed')
        
        # Start async processing
        process_announcement.delay(announcement.id)
        
        return redirect('announcements:announcement_detail', announcement_id=announcement.id)
    
    # Pass email configuration status to template
    context = {
        'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
        'EMAIL_HOST_PASSWORD': '***' if settings.EMAIL_HOST_PASSWORD else None,
    }
    return render(request, 'announcements/create_announcement.html', context)


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
    # Order by priority (highest first), then by created_at (newest first)
    announcements = Announcement.objects.all().order_by('-priority', '-created_at')[:50]
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


def test_email(request):
    """Test email configuration"""
    if request.method == 'POST':
        test_email_address = request.POST.get('test_email', '').strip()
        
        if not test_email_address:
            messages.error(request, 'Please enter an email address')
            return redirect('announcements:create_announcement')
        
        # Check if email is configured
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            messages.error(request, 'Email not configured. Please set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD environment variables.')
            return redirect('announcements:create_announcement')
        
        try:
            subject = 'RailAnnounce - Test Email'
            message = f"""
This is a test email from RailAnnounce system.

If you received this email, your email configuration is working correctly!

Email Configuration:
- SMTP Host: {settings.EMAIL_HOST}
- Port: {settings.EMAIL_PORT}
- From: {settings.DEFAULT_FROM_EMAIL}
- TLS: {settings.EMAIL_USE_TLS}

---
RailAnnounce System
"""
            result = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email_address],
                fail_silently=False,
            )
            
            logger.info(f"Test email sent to {test_email_address}, result: {result}")
            messages.success(request, f'Test email sent successfully to {test_email_address}! Check your inbox.')
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Test email failed: {error_msg}", exc_info=True)
            messages.error(request, f'Test email failed: {error_msg}')
        
        return redirect('announcements:create_announcement')
    
    return redirect('announcements:create_announcement')


@csrf_exempt
@require_http_methods(["POST"])
def api_create_announcement(request):
    """API endpoint to create announcement (for HTMX)"""
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        text = data.get('text', '').strip()
        handler = data.get('handler', '').strip()
        announcement_time = data.get('announcement_time', '').strip()
        location = data.get('location', '').strip()
        contact_no = data.get('contact_no', '').strip()
        priority = int(data.get('priority', 5))
        
        if not text:
            return JsonResponse({'error': 'Text is required'}, status=400)
        
        # Parse datetime if provided
        from django.utils.dateparse import parse_datetime
        parsed_time = None
        if announcement_time:
            parsed_time = parse_datetime(announcement_time)
        
        # Create announcement
        announcement = Announcement.objects.create(
            title=title,
            description=description,
            text=text,
            handler=handler,
            announcement_time=parsed_time,
            location=location,
            contact_no=contact_no,
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
