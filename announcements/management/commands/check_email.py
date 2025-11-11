"""
Management command to check email configuration status
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Check email configuration status'

    def handle(self, *args, **options):
        self.stdout.write("=" * 50)
        self.stdout.write("Email Configuration Status")
        self.stdout.write("=" * 50)
        self.stdout.write("")
        
        # Check environment variables
        env_user = os.environ.get('EMAIL_HOST_USER', '')
        env_pass = os.environ.get('EMAIL_HOST_PASSWORD', '')
        
        self.stdout.write("Environment Variables (os.environ):")
        self.stdout.write(f"  EMAIL_HOST_USER: {env_user if env_user else 'NOT SET'}")
        self.stdout.write(f"  EMAIL_HOST_PASSWORD: {'SET' if env_pass else 'NOT SET'}")
        if env_pass:
            self.stdout.write(f"  Password length: {len(env_pass)} characters")
        self.stdout.write("")
        
        # Check Django settings
        self.stdout.write("Django Settings:")
        self.stdout.write(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER if settings.EMAIL_HOST_USER else 'NOT SET'}")
        self.stdout.write(f"  EMAIL_HOST_PASSWORD: {'SET' if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
        if settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(f"  Password length: {len(settings.EMAIL_HOST_PASSWORD)} characters")
        self.stdout.write("")
        
        # Check other email settings
        self.stdout.write("Email Settings:")
        self.stdout.write(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write("")
        
        # Status
        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(self.style.SUCCESS("✓ Email is CONFIGURED and ready to use!"))
        else:
            self.stdout.write(self.style.WARNING("⚠ Email is NOT CONFIGURED"))
            self.stdout.write("")
            self.stdout.write("To configure email:")
            self.stdout.write("  1. Set environment variables:")
            self.stdout.write("     export EMAIL_HOST_USER='your-email@gmail.com'")
            self.stdout.write("     export EMAIL_HOST_PASSWORD='your-app-password'")
            self.stdout.write("  2. Restart Django server")
            self.stdout.write("  3. Run this command again to verify")

