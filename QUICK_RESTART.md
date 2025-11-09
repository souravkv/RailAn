# ⚡ Quick Restart Guide

**After PC restart, follow these steps to get RailAnnounce running:**

---

## 🚀 Quick Start (4 Steps)

### 1. Start Redis
```bash
redis-server
```
*Usually already running as service*

### 2. Start LibreTranslate (OPTIONAL - for real translations)
```bash
# Run in background
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en

# Or use script
./start_libretranslate.sh
```
*Note: First run takes 5-15 minutes to download models. System works without it.*

### 3. Start Celery Worker (OPTIONAL - for async processing)
```bash
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```
*Tasks can be processed manually if Celery is not running.*

### 4. Start Django Server
```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py runserver
```

---

## ✅ Verify Everything is Running

```bash
# Check Redis
redis-cli ping
# Should return: PONG

# Check LibreTranslate (if started)
curl http://127.0.0.1:5000/languages
# Should return JSON with languages

# Check Django
# Open browser: http://127.0.0.1:8000/
```

---

## 🎯 Access Application

- **Home**: http://127.0.0.1:8000/
- **Create Announcement**: http://127.0.0.1:8000/create/
- **Display Board**: http://127.0.0.1:8000/display/
- **Admin**: http://127.0.0.1:8000/admin/

---

## 🔧 Process Pending Announcements

If you have pending announcements:

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py process_pending --sync
```

---

## 📝 Current Status

- ✅ **Database**: Ready (migrations applied)
- ✅ **Redis**: Running (port 6379)
- ⚠️ **LibreTranslate**: Not running (system works in fallback mode)
- ⚠️ **TTS**: Not available (system works without audio)
- ✅ **Django**: Ready to start

---

## 🐛 If Something Doesn't Work

1. **Check Redis**: `redis-cli ping`
2. **Check Database**: `ls db.sqlite3`
3. **Check Dependencies**: `pip install -r requirements.txt`
4. **Check Logs**: Look at terminal output
5. **See TROUBLESHOOTING.md** for detailed help

---

## 📚 For More Information

- **PROJECT_STATUS.md** - Complete project status
- **README.md** - Full documentation
- **TROUBLESHOOTING.md** - Troubleshooting guide
- **RUN_NOW.md** - Detailed run instructions

---

**That's it! The system is ready to use.** 🚂📢


