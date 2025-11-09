# Quick Fix: Get Real Translations Working

## ✅ Current Status
- ✅ Celery worker is running
- ✅ Announcements are being processed
- ⚠️ **Using fallback mode** (original text, not translated)

## 🔑 To Get Real Translations:

### Step 1: Get Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy the key

### Step 2: Set API Key
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Step 3: Restart Celery Worker
```bash
# Stop current worker
pkill -f "celery.*worker"

# Start new worker (in a new terminal)
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```

### Step 4: Reprocess Pending Announcements
```bash
python3 manage.py shell
>>> from announcements.models import Announcement
>>> from announcements.tasks import process_announcement
>>> for a in Announcement.objects.filter(status='completed'):
...     a.status = 'pending'
...     a.save()
...     process_announcement.delay(a.id)
```

## 🎯 Quick Test
After setting up, create a new announcement and check if translations are different from the original text.

