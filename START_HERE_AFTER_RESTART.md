# 🚀 START HERE - After PC Restart

**Welcome back! This file will help you get RailAnnounce running again.**

---

## ⚡ Quick Start (Copy & Paste)

### Terminal 1: Redis (if not already running)
```bash
redis-server
```

### Terminal 2: Django Server
```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py runserver
```

### Terminal 3: LibreTranslate (OPTIONAL - for real translations)
```bash
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en
```

### Terminal 4: Celery Worker (OPTIONAL - for async processing)
```bash
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```

---

## ✅ Verify

1. **Open browser**: http://127.0.0.1:8000/
2. **You should see**: RailAnnounce home page
3. **Create announcement**: http://127.0.0.1:8000/create/
4. **View display board**: http://127.0.0.1:8000/display/

---

## 📋 Important Files

- **PROJECT_STATUS.md** - Complete project status and what's been done
- **QUICK_RESTART.md** - Quick restart instructions
- **TROUBLESHOOTING.md** - If something doesn't work
- **README.md** - Full documentation

---

## 🔧 Process Pending Announcements

If you have pending announcements:

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py process_pending --sync
```

---

## 🎯 Current Status

- ✅ **System is functional**
- ✅ **Database ready** (migrations applied)
- ✅ **Works in fallback mode** (even without LibreTranslate/TTS)
- ⚠️ **LibreTranslate**: Not running (optional - system works without it)
- ⚠️ **TTS**: Not available (optional - system works without audio)

---

## 🐛 Problems?

See **TROUBLESHOOTING.md** for solutions to common issues.

---

**That's it! The system is ready to use.** 🚂📢


