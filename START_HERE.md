# 🚀 How to Start RailAnnounce - Complete Guide

## Quick Start (4 Terminals Needed)

You need to run **4 services** in **4 separate terminals**. Follow the steps below:

---

## ✅ Step 1: Prepare Database

**Run this ONCE** (only the first time):

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py migrate
```

This creates the database tables.

---

## terminal 1: LibreTranslate Server

**Start LibreTranslate translation server:**

### Option A: Using Docker (Easiest - Recommended)

```bash
docker run -ti --rm -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en
```

### Option B: Using Python (If Docker not available)

```bash
# First, install LibreTranslate (one-time setup)
git clone https://github.com/LibreTranslate/LibreTranslate.git
cd LibreTranslate
pip install -r requirements.txt
python -m libretranslate --update-models

# Then start server
python main.py --host 127.0.0.1 --port 5000
```

**Keep this terminal open!** LibreTranslate should be running on http://127.0.0.1:5000

---

## terminal 2: Redis Server

**Start Redis (required for Celery and WebSocket):**

```bash
redis-server
```

**Keep this terminal open!** Redis should be running on port 6379

**Note:** If Redis is not installed:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
```

---

## terminal 3: Celery Worker

**Start Celery worker (processes announcements in background):**

```bash
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```

**Keep this terminal open!** You'll see task processing logs here.

---

## terminal 4: Django Server

**Start Django web server:**

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py runserver
```

**Keep this terminal open!** Django should be running on http://127.0.0.1:8000

---

## 🎯 Access the Application

Once all 4 services are running:

1. **Home Page**: http://127.0.0.1:8000/
2. **Create Announcement**: http://127.0.0.1:8000/create/
3. **Display Board**: http://127.0.0.1:8000/display/
4. **Admin Panel**: http://127.0.0.1:8000/admin/

---

## ✅ Verify Everything is Running

Check each service:

1. **LibreTranslate**: Open http://127.0.0.1:5000 in browser (should show LibreTranslate API page)
2. **Redis**: Run `redis-cli ping` in terminal (should return "PONG")
3. **Celery**: Check Terminal 3 for "celery@..." message
4. **Django**: Check Terminal 4 for "Starting development server at http://127.0.0.1:8000/"

---

## 🧪 Test the System

1. Go to http://127.0.0.1:8000/create/
2. Enter text: "The train to Mumbai will arrive at platform 3"
3. Click "Create and Process Announcement"
4. Wait a few seconds (processing happens in background)
5. Check the announcement detail page
6. Go to http://127.0.0.1:8000/display/ to see it on the display board

---

## 🛑 Stopping Services

To stop all services:

1. **Press `Ctrl+C` in each terminal** to stop that service
2. Stop in this order:
   - Django server (Terminal 4)
   - Celery worker (Terminal 3)
   - Redis (Terminal 2) - or just close terminal
   - LibreTranslate (Terminal 1)

---

## 🐛 Troubleshooting

### "LibreTranslate connection failed"
- Make sure LibreTranslate is running on http://127.0.0.1:5000
- Check Terminal 1 for errors

### "Redis connection failed"
- Make sure Redis is running: `redis-server`
- Check Terminal 2

### "Celery worker not processing"
- Make sure Redis is running
- Check Terminal 3 for errors
- Make sure Celery worker is running

### "WebSocket not connecting"
- Make sure Redis is running (required for WebSocket)
- Check browser console for errors

### "No module named 'channels'"
- Install dependencies: `pip install -r requirements.txt`

---

## 📝 Quick Reference

| Service | Terminal | Command | Port |
|---------|----------|---------|------|
| LibreTranslate | 1 | `docker run -ti --rm -p 5000:5000 libretranslate/libretranslate` | 5000 |
| Redis | 2 | `redis-server` | 6379 |
| Celery Worker | 3 | `celery -A railannounce worker --loglevel=info` | - |
| Django Server | 4 | `python3 manage.py runserver` | 8000 |

---

## 🎉 You're All Set!

Once all 4 terminals are running, your RailAnnounce system is ready to use!

**Happy announcing! 🚂📢**


