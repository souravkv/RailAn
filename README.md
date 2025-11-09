# RailAnnounce – FREE Offline Multilingual Railway Announcement System

**100% FREE | NO API KEYS | NO PAYMENTS | FULLY OFFLINE-CAPABLE**

> **📋 Current Status**: ✅ SYSTEM IS FUNCTIONAL - See `PROJECT_STATUS.md` for current state  
> **🚀 Quick Start**: See `QUICK_RESTART.md` for quick restart instructions  
> **🐛 Issues**: See `TROUBLESHOOTING.md` for troubleshooting guide

## 🎯 Goal

Staff types announcement → auto-detect language → translate to Hindi, Tamil, Telugu, Bengali, Kannada → generate **offline voice** → show on **live display board** → push via **WebSocket**

## 🛠 Tech Stack (ALL FREE)

- **Django 5.x** - Web framework
- **SQLite/PostgreSQL** - Database
- **LibreTranslate** - Self-hosted translation server (FREE)
- **Coqui TTS** - Offline TTS (best quality)
- **pyttsx3** - Fallback offline TTS
- **Django Channels** - WebSocket support
- **Redis** - Message broker and cache
- **Celery** - Async task processing
- **HTMX + Bootstrap** - Frontend (no React needed)

## 📋 Prerequisites

- Python 3.10+
- Redis server
- LibreTranslate server (instructions below)

## 🚀 Setup Instructions

### Step 1: Setup LibreTranslate Server (Separate Service)

**Important:** LibreTranslate runs as a **separate server**, NOT as a Python package in this project. You need to run it in a **separate terminal/process**.

#### Option A: Using Docker (Recommended - Easiest)

```bash
# Run LibreTranslate using Docker
docker run -ti --rm -p 5000:5000 libretranslate/libretranslate

# Or with specific languages pre-loaded
docker run -ti --rm -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en
```

#### Option B: From Source (Advanced)

```bash
# Clone LibreTranslate
git clone https://github.com/LibreTranslate/LibreTranslate.git
cd LibreTranslate

# Install dependencies (may require system libraries like ICU)
pip install -r requirements.txt

# Download models for Indian languages (one-time, may take time)
python -m libretranslate --update-models

# Start server (runs on http://127.0.0.1:5000)
python main.py --host 127.0.0.1 --port 5000
```

**Note:** 
- The first time you run this, it will download language models which may take some time
- Make sure you have internet connection for the initial setup
- If installing from source fails due to missing system libraries (like ICU), use Docker instead
- Our Django app connects to LibreTranslate via HTTP (using `requests` library), so it doesn't need the `libretranslate` Python package

### Step 2: Install Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server
# Or run: redis-server
```

### Step 3: Setup Django Project

```bash
# Navigate to project directory
cd /home/zourv/Documents/PROJEX/Django_project

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p media/audio static staticfiles

# Run migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser (optional, for admin access)
python3 manage.py createsuperuser
```

### Step 4: Start Celery Worker (in a separate terminal)

```bash
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```

### Step 5: Start Django Development Server

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py runserver
```

### Step 6: Access the Application

- **Home**: http://127.0.0.1:8000/
- **Create Announcement**: http://127.0.0.1:8000/create/
- **Display Board**: http://127.0.0.1:8000/display/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
Django_project/
├── announcements/          # Main app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── tasks.py           # Celery tasks
│   ├── consumers.py       # WebSocket consumers
│   ├── services/          # Business logic services
│   │   ├── language_detector.py
│   │   ├── translator.py
│   │   └── tts_service.py
│   └── admin.py           # Admin interface
├── railannounce/          # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL config
│   ├── asgi.py            # ASGI config (WebSocket)
│   └── celery.py          # Celery config
├── templates/             # HTML templates
├── static/                # Static files
├── media/                 # Media files (audio)
└── requirements.txt       # Python dependencies
```

## 🔧 Configuration

### Environment Variables

You can set these environment variables (optional):

```bash
export LIBRETRANSLATE_URL=http://127.0.0.1:5000
export DJANGO_SETTINGS_MODULE=railannounce.settings
```

### Settings

Key settings in `railannounce/settings.py`:

- `LIBRETRANSLATE_URL`: LibreTranslate server URL (default: http://127.0.0.1:5000)
- `CELERY_BROKER_URL`: Redis URL for Celery (default: redis://127.0.0.1:6379/0)
- `CHANNEL_LAYERS`: Redis configuration for WebSocket
- `SUPPORTED_LANGUAGES`: Supported language codes

## 🎮 Usage

### Creating an Announcement

1. Go to http://127.0.0.1:8000/create/
2. Enter your announcement text
3. Set priority (1-10, higher = more important)
4. Click "Create and Process Announcement"

The system will:
- Auto-detect the language
- Translate to Hindi, Tamil, Telugu, Bengali, Kannada
- Generate audio files for each language
- Update display boards in real-time via WebSocket

### Display Board

1. Go to http://127.0.0.1:8000/display/
2. View live announcements
3. Switch between languages using tabs
4. Audio files are automatically loaded

### Admin Panel

Access admin at http://127.0.0.1:8000/admin/ to:
- View all announcements
- Manage translations
- View audio files
- Manage display boards

## 🌐 Supported Languages

- **English** (en)
- **Hindi** (hi)
- **Tamil** (ta)
- **Telugu** (te)
- **Bengali** (bn)
- **Kannada** (kn)

## 🔍 Features

- ✅ Auto language detection
- ✅ Multilingual translation (5+ languages)
- ✅ Offline TTS (Coqui TTS + pyttsx3 fallback)
- ✅ Real-time WebSocket updates
- ✅ Async processing with Celery
- ✅ Display board with live updates
- ✅ Audio playback for all languages
- ✅ Priority-based announcement ordering
- ✅ 100% free and open-source

## 🐛 Troubleshooting

### LibreTranslate not working

- Make sure LibreTranslate server is running on http://127.0.0.1:5000
- Check if models are downloaded: `python -m libretranslate --update-models`
- Check LibreTranslate logs for errors

### Redis connection error

- Make sure Redis is running: `redis-server` or `sudo systemctl start redis-server`
- Check Redis connection: `redis-cli ping` (should return PONG)

### Celery worker not processing tasks

- Make sure Celery worker is running: `celery -A railannounce worker --loglevel=info`
- Check Redis connection
- Check Celery logs for errors

### TTS not working

- Coqui TTS requires models to be downloaded (automatic on first use)
- If Coqui fails, pyttsx3 will be used as fallback
- Check TTS service logs for errors

### WebSocket not connecting

- Make sure Django Channels is properly configured
- Check Redis is running (required for Channels)
- Check browser console for WebSocket errors
- Make sure ASGI application is being used (not WSGI)

## 📝 Notes

- **First run**: TTS models will be downloaded automatically (may take time)
- **Offline mode**: Once models are downloaded, everything works offline
- **Performance**: Translation and TTS generation are async (non-blocking)
- **Scaling**: Can be deployed with multiple Celery workers

## 📄 License

This project is free and open-source. Use it however you want!

## 🤝 Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Improving documentation

## 🙏 Credits

- **LibreTranslate** - Free translation service
- **Coqui TTS** - High-quality TTS
- **Django Channels** - WebSocket support
- **Celery** - Async task processing

---

**Enjoy your FREE multilingual railway announcement system! 🚂📢**

