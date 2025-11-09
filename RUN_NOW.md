# 🚀 RUN NOW - Quick Start Guide

## Step-by-Step Instructions to Start Everything

### ✅ Step 1: Prepare Database (Run Once)

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py migrate
```

**This is done! ✅** Database is ready.

---

### 🔴 Step 2: Open 4 Terminals

You need **4 separate terminal windows**. Open them now:

- **Terminal 1** - LibreTranslate Server
- **Terminal 2** - Redis Server  
- **Terminal 3** - Celery Worker
- **Terminal 4** - Django Server

---

### 🟢 Terminal 1: LibreTranslate Server

**Copy and paste this command:**

```bash
docker run -ti --rm -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en
```

**OR if you don't have Docker:**

```bash
# First time only - install LibreTranslate
git clone https://github.com/LibreTranslate/LibreTranslate.git
cd LibreTranslate
pip install -r requirements.txt
python -m libretranslate --update-models

# Then start server
python main.py --host 127.0.0.1 --port 5000
```

**✅ You'll know it's working when you see:** Server running on http://127.0.0.1:5000

**Keep this terminal open!**

---

### 🟢 Terminal 2: Redis Server

**Copy and paste this command:**

```bash
redis-server
```

**✅ You'll know it's working when you see:** `Ready to accept connections`

**Keep this terminal open!**

**Note:** If Redis is not installed:
```bash
sudo apt-get install redis-server
```

---

### 🟢 Terminal 3: Celery Worker

**Copy and paste this command:**

```bash
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```

**✅ You'll know it's working when you see:** `celery@... ready`

**Keep this terminal open!**

---

### 🟢 Terminal 4: Django Server

**Copy and paste this command:**

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py runserver
```

**✅ You'll know it's working when you see:** `Starting development server at http://127.0.0.1:8000/`

**Keep this terminal open!**

---

## 🎯 Access the Application

Once all 4 terminals show their services are running:

1. **Open your browser**
2. **Go to:** http://127.0.0.1:8000/
3. **You should see the RailAnnounce home page!**

---

## 🧪 Test It!

1. Click **"Create New"** or go to http://127.0.0.1:8000/create/
2. Enter text: `The train to Mumbai will arrive at platform 3`
3. Click **"Create and Process Announcement"**
4. Wait a few seconds
5. You'll see the announcement being processed!
6. Go to http://127.0.0.1:8000/display/ to see it on the display board

---

## ✅ Quick Checklist

Before starting, make sure you have:

- [x] Python 3.10+ installed
- [x] Django project dependencies installed (`pip install -r requirements.txt`)
- [ ] Docker installed (for LibreTranslate) OR LibreTranslate installed
- [ ] Redis installed (`sudo apt-get install redis-server`)
- [ ] 4 terminal windows ready

---

## 🛑 Stopping Services

To stop everything:

1. Go to each terminal
2. Press **`Ctrl+C`**
3. Stop in this order:
   - Terminal 4 (Django)
   - Terminal 3 (Celery)
   - Terminal 2 (Redis)
   - Terminal 1 (LibreTranslate)

---

## 🐛 Troubleshooting

### "Connection refused" errors
- Make sure all 4 services are running
- Check each terminal for error messages

### "Redis connection failed"
- Make sure Redis is running in Terminal 2
- Check: `redis-cli ping` (should return "PONG")

### "LibreTranslate not working"
- Make sure LibreTranslate is running in Terminal 1
- Check: Open http://127.0.0.1:5000 in browser

### "Celery worker not processing"
- Make sure Redis is running
- Make sure Celery worker is running in Terminal 3

---

## 📋 Command Quick Reference

| Service | Command |
|---------|---------|
| **LibreTranslate** | `docker run -ti --rm -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en` |
| **Redis** | `redis-server` |
| **Celery** | `cd /home/zourv/Documents/PROJEX/Django_project && celery -A railannounce worker --loglevel=info` |
| **Django** | `cd /home/zourv/Documents/PROJEX/Django_project && python3 manage.py runserver` |

---

## 🎉 That's It!

Once all 4 terminals are running, your RailAnnounce system is ready!

**Happy announcing! 🚂📢**


