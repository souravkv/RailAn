# ✅ Service Status Check

## Current Status

### ✅ Redis Server - RUNNING
- **Status**: Already running on port 6379
- **PID**: 14380
- **Response**: PONG ✅
- **Action**: **SKIP Terminal 2** - Redis is ready!

### ⏳ Other Services - Need to Start

---

## 🚀 Start Remaining Services

Since Redis is already running, you only need to start **3 services** in **3 terminals**:

---

### 🟢 Terminal 1: LibreTranslate Server

```bash
docker run -ti --rm -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en
```

**OR if you don't have Docker:**

```bash
# If LibreTranslate is not installed yet:
git clone https://github.com/LibreTranslate/LibreTranslate.git
cd LibreTranslate
pip install -r requirements.txt
python -m libretranslate --update-models

# Then start:
python main.py --host 127.0.0.1 --port 5000
```

---

### 🟢 Terminal 2: Celery Worker

```bash
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```

---

### 🟢 Terminal 3: Django Server

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py runserver
```

---

## ✅ Quick Check Commands

Check if services are running:

```bash
# Check Redis (should return PONG)
redis-cli ping

# Check if LibreTranslate is running
curl http://127.0.0.1:5000/languages

# Check if Django is running
curl http://127.0.0.1:8000/
```

---

## 🎯 Once All 3 Services Are Running

1. Open browser: http://127.0.0.1:8000/
2. Start creating announcements!

---

## 📝 Summary

- ✅ **Redis**: Already running (Terminal 2 - SKIP)
- ⏳ **LibreTranslate**: Start in Terminal 1
- ⏳ **Celery Worker**: Start in Terminal 2 (instead of Redis)
- ⏳ **Django Server**: Start in Terminal 3

**You only need 3 terminals now!**


