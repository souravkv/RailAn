# RailAnnounce – AI-Powered Multilingual Railway Announcement System

**Cloud-Based Translation | Real-Time Updates | Scalable Architecture**

> **📋 Current Status**: ✅ SYSTEM IS FULLY FUNCTIONAL - See `PROJECT_STATUS.md` for current state  
> **🚀 Quick Start**: See `QUICK_RESTART.md` for quick restart instructions  
> **🐛 Issues**: See `TROUBLESHOOTING.md` for troubleshooting guide  
> **🔑 Setup**: See `GEMINI_SETUP.md` for Gemini API configuration

## 🎯 Goal

Staff types announcement → AI auto-detects language → Google Gemini API translates to Hindi, Tamil, Telugu, Bengali, Kannada → generates **audio files** → displays on **live display board** → pushes via **WebSocket** in real-time

## 🛠 Tech Stack

### Backend Framework
- **Django 5.0.4** - High-performance Python web framework
- **Django Channels 4.0** - WebSocket support for real-time communication
- **ASGI** - Asynchronous Server Gateway Interface

### Database & Caching
- **SQLite/PostgreSQL** - Relational database (SQLite for dev, PostgreSQL for production)
- **Redis 5.0** - In-memory data structure store (message broker & cache)

### AI & Machine Learning Services
- **Google Gemini 2.5 Flash API** - Advanced AI translation service
- **langdetect 1.0.9** - Automatic language detection using statistical models
- **google-generativeai** - Official Google AI SDK

### Asynchronous Task Processing
- **Celery 5.3.4** - Distributed task queue for async processing
- **Redis** - Message broker for Celery workers

### Text-to-Speech
- **pyttsx3** - Cross-platform TTS engine
- **pydub** - Audio manipulation library
- **Coqui TTS** (optional) - High-quality neural TTS

### Frontend Technologies
- **Bootstrap 5** - Responsive CSS framework
- **HTMX** - Dynamic HTML without JavaScript framework
- **WebSocket** - Real-time bidirectional communication
- **JavaScript** - Client-side interactivity

### Additional Tools
- **python-decouple** - Environment variable management
- **Pillow** - Image processing
- **requests** - HTTP library

## 📋 Prerequisites

- Python 3.10+
- Redis server
- Google Gemini API key (free tier available)

## 🚀 Setup Instructions

### Step 1: Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

**Note:** Free tier is available with generous usage limits for development.

### Step 2: Set Gemini API Key

```bash
# Set as environment variable (recommended)
export GEMINI_API_KEY="your-api-key-here"

# Or add to ~/.bashrc for permanent setup
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

See `GEMINI_SETUP.md` for detailed setup instructions.

### Step 3: Install Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server
# Or run: redis-server
```

### Step 4: Setup Django Project

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

### Step 5: Start Celery Worker (in a separate terminal)

```bash
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```

### Step 6: Start Django Development Server

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py runserver
```

### Step 7: Access the Application

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
│   │   ├── language_detector.py  # AI language detection
│   │   ├── translator.py        # Gemini API integration
│   │   └── tts_service.py        # Text-to-Speech service
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

You can set these environment variables:

```bash
export GEMINI_API_KEY="your-api-key-here"  # Required for translations
export DJANGO_SETTINGS_MODULE=railannounce.settings
```

### Settings

Key settings in `railannounce/settings.py`:

- `GEMINI_API_KEY`: Google Gemini API key (required for translations)
- `CELERY_BROKER_URL`: Redis URL for Celery (default: redis://127.0.0.1:6379/0)
- `CHANNEL_LAYERS`: Redis configuration for WebSocket
- `SUPPORTED_LANGUAGES`: Supported language codes (hi, ta, te, bn, kn, en)

## 🎮 Usage

### Creating an Announcement

1. Go to http://127.0.0.1:8000/create/
2. Enter your announcement text
3. Set priority (1-10, higher = more important)
4. Click "Create and Process Announcement"

The system will:
- Auto-detect the language using AI (langdetect)
- Translate to Hindi, Tamil, Telugu, Bengali, Kannada using Google Gemini API
- Generate audio files for each language (async processing)
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

- ✅ **AI-Powered Language Detection** - Automatic language identification
- ✅ **Google Gemini API Integration** - Advanced AI translation service
- ✅ **Multilingual Support** - 5+ Indian languages (Hindi, Tamil, Telugu, Bengali, Kannada)
- ✅ **Asynchronous Processing** - Celery workers for non-blocking operations
- ✅ **Real-Time WebSocket Updates** - Live display board synchronization
- ✅ **Text-to-Speech Generation** - Audio files for all languages
- ✅ **Scalable Architecture** - Redis-based message queue
- ✅ **Priority-Based Ordering** - Intelligent announcement prioritization
- ✅ **RESTful API** - JSON endpoints for integration
- ✅ **Admin Interface** - Django admin for management

## 🐛 Troubleshooting

### Gemini API not working

- Make sure `GEMINI_API_KEY` is set: `echo $GEMINI_API_KEY`
- Verify API key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Check API quota limits in Google Cloud Console
- See `GEMINI_SETUP.md` for detailed setup instructions

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

- **API Key Required**: Gemini API key is required for translations (free tier available)
- **Internet Required**: Gemini API requires internet connection
- **Performance**: Translation and TTS generation are async (non-blocking)
- **Scaling**: Can be deployed with multiple Celery workers for high throughput
- **Fallback Mode**: System works without API key but uses original text (no translation)

## 📄 License

This project is free and open-source. Use it however you want!

## 🤝 Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Improving documentation

## 🙏 Credits

- **Google Gemini API** - Advanced AI translation service
- **Django** - High-performance web framework
- **Django Channels** - WebSocket support
- **Celery** - Distributed task queue
- **Redis** - In-memory data store

---

**Enjoy your FREE multilingual railway announcement system! 🚂📢**

