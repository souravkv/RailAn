# LibreTranslate Stuck - Fix Guide

## 🔍 Why LibreTranslate Appears "Stuck"

When you run LibreTranslate for the first time, it needs to **download language models**, which can take **5-15 minutes** depending on your internet connection. During this time, it may appear "stuck" but it's actually downloading models in the background.

---

## ✅ Quick Fixes

### Option 1: Wait for Model Download (First Time Only)

**The first run downloads models - this is normal and takes time!**

1. **Let it run** - It may take 5-15 minutes on first run
2. **Watch for progress** - You should see download messages
3. **Don't interrupt** - Let it finish downloading models

### Option 2: Check If It's Actually Running

```bash
# Check if Docker container is running
docker ps

# Check Docker logs to see progress
docker logs <container_id>

# Check if port 5000 is accessible
curl http://127.0.0.1:5000/languages
```

### Option 3: Run in Background (Recommended)

Run LibreTranslate in **detached mode** so it doesn't block your terminal:

```bash
# Run in background (detached mode)
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en

# Check logs
docker logs -f libretranslate

# Stop it later
docker stop libretranslate
docker rm libretranslate
```

### Option 4: Use Pre-built Image with Models

Some Docker images come with models pre-downloaded:

```bash
# Try this version (may have models pre-loaded)
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate
```

### Option 5: Run Without Language Restriction (Faster Startup)

```bash
# Don't specify languages - loads faster
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate
```

---

## 🐛 Common Issues

### Issue 1: Container Keeps Restarting

```bash
# Check why it's restarting
docker logs libretranslate

# Common causes:
# - Port 5000 already in use
# - Insufficient memory
# - Docker issue
```

**Fix:**
```bash
# Stop existing container
docker stop libretranslate
docker rm libretranslate

# Check if port 5000 is free
netstat -tulpn | grep 5000

# Try again with more memory (if needed)
docker run -d --name libretranslate -p 5000:5000 --memory="2g" libretranslate/libretranslate
```

### Issue 2: Models Not Downloading

**Fix:**
```bash
# Remove container and try again
docker stop libretranslate
docker rm libretranslate

# Run with verbose output to see download progress
docker run -ti --rm -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en
```

### Issue 3: Out of Memory

LibreTranslate needs at least 2GB RAM.

**Fix:**
```bash
# Check available memory
free -h

# Allocate more memory to Docker (if using Docker Desktop)
# Or use a smaller model set
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate --load-only hi,en
```

---

## 🚀 Recommended Setup (Production)

### Start LibreTranslate in Background

```bash
# Create a startup script
cat > start_libretranslate.sh << 'EOF'
#!/bin/bash
docker stop libretranslate 2>/dev/null
docker rm libretranslate 2>/dev/null
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en
echo "LibreTranslate starting... Check logs with: docker logs -f libretranslate"
EOF

chmod +x start_libretranslate.sh
./start_libretranslate.sh
```

### Check Status

```bash
# Check if it's running
docker ps | grep libretranslate

# Check logs
docker logs libretranslate

# Test if it's ready
curl http://127.0.0.1:5000/languages
```

---

## ⚡ Quick Test

Once LibreTranslate is running, test it:

```bash
# Test translation API
curl -X POST http://127.0.0.1:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello", "source": "en", "target": "hi", "format": "text"}'
```

---

## 📝 Alternative: Run Without Docker

If Docker is causing issues, run LibreTranslate directly:

```bash
# Install LibreTranslate
pip install libretranslate

# Run server
libretranslate --host 127.0.0.1 --port 5000
```

**Note:** This also downloads models on first run and may take time.

---

## 🎯 Summary

**Most Common Issue:** LibreTranslate is not stuck - it's downloading models (first time only, takes 5-15 minutes)

**Solution:**
1. **Wait** for model download to complete
2. **Run in detached mode** (`-d` flag) so it doesn't block terminal
3. **Check logs** to see progress: `docker logs -f libretranslate`
4. **Test when ready**: `curl http://127.0.0.1:5000/languages`

**The system works in fallback mode even without LibreTranslate** - you'll just get original text instead of translations until LibreTranslate is ready.

---

## 🔧 Current Workaround

**You can use the system RIGHT NOW without LibreTranslate:**

1. The system works in fallback mode
2. Translations use original text (not translated)
3. All other features work normally
4. Once LibreTranslate is ready, reprocess announcements:
   ```bash
   python3 manage.py process_pending --sync
   ```

---

**For more help, see TROUBLESHOOTING.md**


