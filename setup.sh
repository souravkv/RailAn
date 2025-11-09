#!/bin/bash

# RailAnnounce Setup Script

echo "🚂 RailAnnounce Setup Script"
echo "=============================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment (optional)
read -p "Do you want to create a virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Virtual environment activated!"
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create directories
echo ""
echo "Creating necessary directories..."
mkdir -p media/audio
mkdir -p static
mkdir -p staticfiles
mkdir -p tts_models

# Run migrations
echo ""
echo "Running database migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser
echo ""
read -p "Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 manage.py createsuperuser
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start LibreTranslate server (see README.md)"
echo "2. Start Redis: redis-server"
echo "3. Start Celery worker: celery -A railannounce worker --loglevel=info"
echo "4. Start Django server: python3 manage.py runserver"
echo ""
echo "For detailed instructions, see README.md"

