#!/bin/bash

# Email Configuration Setup Script for RailAnnounce
# This script helps you set up Gmail SMTP for email notifications

echo "=========================================="
echo "RailAnnounce Email Configuration Setup"
echo "=========================================="
echo ""

# Check if variables are already set
if [ -n "$EMAIL_HOST_USER" ] && [ -n "$EMAIL_HOST_PASSWORD" ]; then
    echo "✓ Email variables are already set!"
    echo "  EMAIL_HOST_USER: $EMAIL_HOST_USER"
    echo "  EMAIL_HOST_PASSWORD: [HIDDEN]"
    echo ""
    echo "If Django server is running, restart it to load these variables."
    exit 0
fi

echo "To set up email, you need:"
echo "1. Your Gmail address"
echo "2. A Gmail App Password (16 characters)"
echo ""
echo "Get App Password: https://myaccount.google.com/apppasswords"
echo ""

# Prompt for email
read -p "Enter your Gmail address: " email
if [ -z "$email" ]; then
    echo "Error: Email address is required"
    exit 1
fi

# Prompt for app password
read -sp "Enter your Gmail App Password (16 chars): " password
echo ""
if [ -z "$password" ]; then
    echo "Error: App Password is required"
    exit 1
fi

# Remove spaces from app password (Gmail app passwords sometimes have spaces)
password=$(echo "$password" | tr -d ' ')

# Export variables
export EMAIL_HOST_USER="$email"
export EMAIL_HOST_PASSWORD="$password"

echo ""
echo "✓ Environment variables set!"
echo ""
echo "To make these permanent, add to your ~/.bashrc or ~/.zshrc:"
echo "  export EMAIL_HOST_USER=\"$email\""
echo "  export EMAIL_HOST_PASSWORD=\"$password\""
echo ""
echo "Or run this script before starting Django server."
echo ""
echo "Current session variables:"
echo "  EMAIL_HOST_USER: $EMAIL_HOST_USER"
echo "  EMAIL_HOST_PASSWORD: [SET - ${#password} characters]"
echo ""
echo "⚠️  IMPORTANT: Restart your Django server for changes to take effect!"
echo ""
echo "To test email, visit: http://localhost:8000/announcements/create/"
echo "   and use the 'Test Email Configuration' section"

