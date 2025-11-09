#!/bin/bash

# LibreTranslate Startup Script
# This script starts LibreTranslate in the background

echo "🚀 Starting LibreTranslate..."
echo ""

# Stop existing container if running
echo "Stopping existing LibreTranslate container (if any)..."
docker stop libretranslate 2>/dev/null
docker rm libretranslate 2>/dev/null

# Start LibreTranslate in detached mode (background)
echo "Starting LibreTranslate in background..."
docker run -d \
  --name libretranslate \
  -p 5000:5000 \
  libretranslate/libretranslate \
  --load-only hi,ta,te,bn,kn,en

echo ""
echo "✅ LibreTranslate container started!"
echo ""
echo "📊 To check status:"
echo "   docker logs -f libretranslate"
echo ""
echo "🔍 To check if it's ready:"
echo "   curl http://127.0.0.1:5000/languages"
echo ""
echo "⏳ Note: First run downloads models (5-15 minutes)."
echo "   The system works in fallback mode until LibreTranslate is ready."
echo ""
echo "🛑 To stop:"
echo "   docker stop libretranslate"
echo ""


