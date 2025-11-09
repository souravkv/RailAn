#!/bin/bash

# Quick Setup Script for Gemini API
# This script helps you set up Gemini API for translation

echo "🚀 Gemini API Setup for RailAnnounce"
echo "======================================"
echo ""

# Step 1: Install the package
echo "📦 Step 1: Installing google-generativeai package..."
pip install google-generativeai

echo ""
echo "✅ Package installed!"
echo ""

# Step 2: Get API key
echo "🔑 Step 2: Get your Gemini API key"
echo "-----------------------------------"
echo "1. Visit: https://makersuite.google.com/app/apikey"
echo "2. Sign in with your Google account"
echo "3. Create a new API key"
echo "4. Copy the API key"
echo ""

# Step 3: Set API key
read -p "Enter your Gemini API key (or press Enter to skip): " api_key

if [ -n "$api_key" ]; then
    # Add to .bashrc
    if ! grep -q "GEMINI_API_KEY" ~/.bashrc 2>/dev/null; then
        echo "export GEMINI_API_KEY=\"$api_key\"" >> ~/.bashrc
        echo "✅ API key added to ~/.bashrc"
    else
        echo "⚠️  GEMINI_API_KEY already exists in ~/.bashrc"
        echo "   You can update it manually or export it for this session:"
        echo "   export GEMINI_API_KEY=\"$api_key\""
    fi
    
    # Export for current session
    export GEMINI_API_KEY="$api_key"
    echo "✅ API key set for current session"
else
    echo "⚠️  No API key provided. You can set it later with:"
    echo "   export GEMINI_API_KEY=\"your-api-key-here\""
fi

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo ""
echo "📝 Next steps:"
echo "1. If you added the API key, restart your terminal or run:"
echo "   source ~/.bashrc"
echo ""
echo "2. Start your Django server:"
echo "   python manage.py runserver"
echo ""
echo "3. Test by creating an announcement"
echo ""
echo "💡 Note: If API key is not set, system will work in fallback mode"
echo "   (using original text instead of translations)"

