# Troubleshooting Guide

## ✅ Fixed Issues

### 1. Translations Not Showing
**Problem:** Announcements were stuck in "pending" status and translations weren't being created.

**Solution:**
- Added fallback mechanism: If LibreTranslate is not available, system uses original text for all languages
- Made task completion more robust: Announcements are marked as "completed" even if translation/TTS fails
- Created management command to manually process pending announcements

### 2. Display Board Empty
**Problem:** Display board only showed "completed" announcements.

**Solution:**
- Updated display board to show all announcements (pending, processing, completed)
- Added status badges to show announcement status
- Prioritized completed announcements but also show processing/pending ones

### 3. LibreTranslate Not Running
**Problem:** LibreTranslate server was not running, causing translation failures.

**Solution:**
- System now works in fallback mode when LibreTranslate is not available
- Translations are created using original text when translation service is unavailable
- System continues to function even without LibreTranslate (just without actual translations)

---

## 🔧 How to Fix Current Issues

### Issue: Translations Show Original Text (Not Translated)

**This is expected behavior when LibreTranslate is not running.**

To get real translations:

1. **Start LibreTranslate Server:**
   ```bash
   # Option 1: Using Docker (Easiest)
   docker run -ti --rm -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en
   
   # Option 2: From source
   cd LibreTranslate
   python main.py --host 127.0.0.1 --port 5000
   ```

2. **Reprocess Existing Announcements:**
   ```bash
   # Process all pending announcements
   python3 manage.py process_pending --sync
   
   # Or process specific announcement
   python3 manage.py process_pending --sync --id 2
   ```

### Issue: Audio Files Not Generated

**This is expected when TTS services are not available.**

To enable audio generation:

1. **Install TTS System Libraries:**
   ```bash
   # For pyttsx3 (fallback TTS)
   sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
   
   # Or for better quality
   sudo apt-get install festival festival-dev
   ```

2. **Or Install Coqui TTS (Optional, better quality):**
   ```bash
   pip install TTS
   # Note: This requires PyTorch (~2GB download)
   ```

3. **Reprocess Announcements:**
   ```bash
   python3 manage.py process_pending --sync
   ```

### Issue: Celery Worker Not Processing Tasks

**Check if Celery worker is running:**

```bash
# Check if Celery worker is running
ps aux | grep celery

# Start Celery worker if not running
cd /home/zourv/Documents/PROJEX/Django_project
celery -A railannounce worker --loglevel=info
```

**Process tasks manually (without Celery):**

```bash
# Process all pending announcements synchronously
python3 manage.py process_pending --sync

# Process specific announcement
python3 manage.py process_pending --sync --id 2
```

---

## 🚀 Quick Fixes

### Process All Pending Announcements

```bash
cd /home/zourv/Documents/PROJEX/Django_project
python3 manage.py process_pending --sync
```

### Check Announcement Status

```bash
python3 manage.py shell -c "from announcements.models import Announcement; print('Pending:', Announcement.objects.filter(status='pending').count()); print('Completed:', Announcement.objects.filter(status='completed').count())"
```

### Check Translations

```bash
python3 manage.py shell -c "from announcements.models import Announcement, Translation; a = Announcement.objects.first(); print('Translations:', a.translations.count() if a else 0)"
```

---

## 📋 Service Status Checklist

- [ ] **Redis**: Running (`redis-cli ping` should return "PONG")
- [ ] **LibreTranslate**: Running (http://127.0.0.1:5000 should be accessible)
- [ ] **Celery Worker**: Running (check terminal or `ps aux | grep celery`)
- [ ] **Django Server**: Running (http://127.0.0.1:8000 should be accessible)

---

## 🔍 Common Errors

### "LibreTranslate server not available"
**Solution:** Start LibreTranslate server or use fallback mode (system will use original text)

### "No TTS service available"
**Solution:** Install TTS system libraries or use fallback mode (system works without audio)

### "Celery worker not processing"
**Solution:** Make sure Celery worker is running, or use `--sync` flag to process manually

### "Display board is empty"
**Solution:** Process pending announcements using `python3 manage.py process_pending --sync`

---

## ✅ Current Status

The system is now working with fallback mode:
- ✅ Translations are created (using original text when LibreTranslate is unavailable)
- ✅ Announcements are marked as completed
- ✅ Display board shows all announcements
- ⚠️ Real translations require LibreTranslate server
- ⚠️ Audio generation requires TTS services

**The system is functional but works in limited mode without external services.**

---

## 🎯 Next Steps

1. **Start LibreTranslate** for real translations
2. **Install TTS libraries** for audio generation
3. **Start Celery worker** for async processing
4. **Process pending announcements** using management command

---

**For more help, see README.md and QUICKSTART.md**


