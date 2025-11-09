"""
Management command to process pending announcements
"""
from django.core.management.base import BaseCommand
from announcements.models import Announcement
from announcements.tasks import process_announcement


class Command(BaseCommand):
    help = 'Process pending announcements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sync',
            action='store_true',
            help='Process synchronously (without Celery)',
        )
        parser.add_argument(
            '--id',
            type=int,
            help='Process specific announcement ID',
        )

    def handle(self, *args, **options):
        if options['id']:
            # Process specific announcement
            try:
                announcement = Announcement.objects.get(id=options['id'])
                self.stdout.write(f'Processing announcement #{announcement.id}...')
                if options['sync']:
                    # Process synchronously (call the function directly)
                    process_announcement(announcement.id)
                    self.stdout.write(self.style.SUCCESS(f'Successfully processed announcement #{announcement.id}'))
                else:
                    # Process via Celery
                    process_announcement.delay(announcement.id)
                    self.stdout.write(self.style.SUCCESS(f'Successfully queued announcement #{announcement.id}'))
            except Announcement.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Announcement #{options["id"]} not found'))
        else:
            # Process all pending announcements
            pending = Announcement.objects.filter(status='pending')
            count = pending.count()
            
            if count == 0:
                self.stdout.write(self.style.WARNING('No pending announcements found'))
                return
            
            self.stdout.write(f'Found {count} pending announcement(s)')
            
            for announcement in pending:
                self.stdout.write(f'Processing announcement #{announcement.id}...')
                if options['sync']:
                    # Process synchronously (for testing)
                    try:
                        process_announcement(announcement.id)
                        self.stdout.write(self.style.SUCCESS(f'Successfully processed announcement #{announcement.id}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error processing announcement #{announcement.id}: {e}'))
                else:
                    # Process via Celery
                    process_announcement.delay(announcement.id)
                    self.stdout.write(self.style.SUCCESS(f'Queued announcement #{announcement.id} for processing'))

