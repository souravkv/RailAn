# Installation Fixes & Notes

## ✅ Fixed: LibreTranslate Package Issue

### Problem
The `libretranslate` Python package was trying to install `pyicu` which requires ICU system libraries, causing installation errors.

### Solution
**We don't need the `libretranslate` Python package!** 

LibreTranslate runs as a **separate server** (either via Docker or from source), and our Django app connects to it via HTTP using the `requests` library.

### What Changed
- ✅ Removed `libretranslate==1.2.9` from `requirements.txt`
- ✅ Our `Translator` service uses `requests` to make HTTP calls to LibreTranslate server
- ✅ LibreTranslate should be run separately (see README.md)

## 🔧 System Dependencies

### For pyttsx3 (TTS Fallback)

If you see this error:
```
pyttsx3 not available: libespeak.so.1: cannot open shared object file
```

Install system libraries:

```bash
# Ubuntu/Debian
sudo apt-get install espeak espeak-data libespeak1 libespeak-dev

# Or for better quality (festival)
sudo apt-get install festival festival-dev
```

### For LibreTranslate (if installing from source)

If installing LibreTranslate from source, you may need:

```bash
# Ubuntu/Debian
sudo apt-get install pkg-config libicu-dev

# Then install LibreTranslate
pip install libretranslate
```

**However, we recommend using Docker instead** (see README.md).

## 📦 Current Dependencies

Our Django project only needs:
- Django 5.0.4
- channels (WebSocket)
- celery (async tasks)
- redis (message broker)
- requests (HTTP client for LibreTranslate)
- langdetect (language detection)
- pyttsx3 (TTS fallback)
- pydub (audio manipulation)

**No LibreTranslate Python package needed!**

## ✅ Verification

After installation, verify:

```bash
# Check Django setup
python3 manage.py check

# Create migrations
python3 manage.py makemigrations

# Run migrations
python3 manage.py migrate
```

## 🚀 Next Steps

1. **Start LibreTranslate server** (separate terminal):
   ```bash
   docker run -ti --rm -p 5000:5000 libretranslate/libretranslate
   ```

2. **Start Redis** (separate terminal):
   ```bash
   redis-server
   ```

3. **Start Celery worker** (separate terminal):
   ```bash
   celery -A railannounce worker --loglevel=info
   ```

4. **Start Django server**:
   ```bash
   python3 manage.py runserver
   ```

## 📝 Notes

- LibreTranslate runs on http://127.0.0.1:5000 by default
- Django app connects to it via HTTP (no package needed)
- All dependencies should now install without errors
- System libraries (espeak, ICU) are optional - only needed for specific features

---

**Everything should work now! 🎉**


