#!/bin/bash

# Script to set Gemini API key

echo "🔑 Setting Gemini API Key"
echo "========================="
echo ""
echo "Get your API key from: https://makersuite.google.com/app/apikey"
echo ""

read -p "Enter your Gemini API key: " api_key

if [ -n "$api_key" ]; then
    # Export for current session
    export GEMINI_API_KEY="$api_key"
    echo ""
    echo "✅ API key set for current session!"
    echo ""
    echo "To make it permanent, add this to your ~/.bashrc:"
    echo "export GEMINI_API_KEY=\"$api_key\""
    echo ""
    echo "Or run:"
    echo "echo 'export GEMINI_API_KEY=\"$api_key\"' >> ~/.bashrc"
    echo "source ~/.bashrc"
else
    echo "❌ No API key provided"
fi

