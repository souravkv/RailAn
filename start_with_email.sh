#!/bin/bash

# Start Django server with email configuration check

cd "$(dirname "$0")"

echo "=========================================="
echo "RailAnnounce - Starting with Email Check"
echo "=========================================="
echo ""

# Check if email variables are set
if [ -z "$EMAIL_HOST_USER" ] || [ -z "$EMAIL_HOST_PASSWORD" ]; then
    echo "⚠️  Email variables not set in this terminal!"
    echo ""
    echo "Please set them first:"
    echo "  export EMAIL_HOST_USER='your-email@gmail.com'"
    echo "  export EMAIL_HOST_PASSWORD='your-app-password'"
    echo ""
    echo "Or run: ./setup_email.sh"
    echo ""
    read -p "Continue without email? (y/n): " continue
    if [ "$continue" != "y" ]; then
        exit 1
    fi
    echo ""
else
    echo "✓ Email variables detected:"
    echo "  EMAIL_HOST_USER: $EMAIL_HOST_USER"
    echo "  EMAIL_HOST_PASSWORD: [SET - ${#EMAIL_HOST_PASSWORD} characters]"
    echo ""
fi

echo "Starting Django server..."
echo "To check email status, run in another terminal:"
echo "  python3 manage.py check_email"
echo ""

python3 manage.py runserver

