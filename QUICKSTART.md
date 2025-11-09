# RailAnnounce Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
cd /home/zourv/Documents/PROJEX/Django_project
pip install -r requirements.txt
```

### 2. Setup Database

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 3. Start Services

You need **4 terminals** running simultaneously:

#### Terminal 1: LibreTranslate Server
```bash
# Clone and start LibreTranslate (one-time setup)
git clone https://github.com/LibreTranslate/LibreTranslate.git
cd LibreTranslate
pip install -r requirements.txt
python -m libretranslate --update-models  # Download models (one-time)
python main.py --host 127.0.0.1 --port 5000
```

#### Terminal 2: Redis Server
```bash
redis-server
```

#### Terminal 3: Celery Worker
```bash
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```

#### Terminal 4: Django Server
```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py runserver
```

### 4. Access Application

- **Home**: http://127.0.0.1:8000/
- **Create Announcement**: http://127.0.0.1:8000/create/
- **Display Board**: http://127.0.0.1:8000/display/

## 📝 Creating Your First Announcement

1. Go to http://127.0.0.1:8000/create/
2. Enter text: "The train to Mumbai will arrive at platform 3"
3. Set priority: 5
4. Click "Create and Process Announcement"

The system will:
- ✅ Detect language (English)
- ✅ Translate to Hindi, Tamil, Telugu, Bengali, Kannada
- ✅ Generate audio files
- ✅ Show on display board

## 🎯 Testing Without LibreTranslate

If LibreTranslate is not running, the system will still work but translations will be the original text. You can test the TTS and display board features.

## 🔧 Troubleshooting

### "LibreTranslate connection failed"
- Make sure LibreTranslate is running on http://127.0.0.1:5000
- Check Terminal 1 for errors

### "Redis connection failed"
- Make sure Redis is running: `redis-server`
- Check Terminal 2

### "Celery worker not processing"
- Make sure Celery worker is running
- Check Terminal 3 for errors
- Make sure Redis is running

### "WebSocket not connecting"
- Make sure Redis is running (required for WebSocket)
- Check browser console for errors

## 💡 Tips

1. **First run**: TTS models download automatically (may take time)
2. **Offline mode**: Once models are downloaded, works offline
3. **Performance**: Processing is async (non-blocking)
4. **Multiple languages**: System supports 6 languages

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

---

**Happy announcing! 🚂📢**

