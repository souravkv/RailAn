# Gemini API Setup Guide

## ✅ Migration Complete: LibreTranslate → Gemini API

The translation service has been migrated from LibreTranslate (Docker) to Google Gemini API. This eliminates the need for Docker and reduces system resource usage.

## 🔑 Getting Your Gemini API Key

1. **Visit Google AI Studio**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Create a new API key** (or use an existing one)
4. **Copy the API key**

## ⚙️ Configuration

### Option 1: Environment Variable (Recommended)

Set the API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

To make it permanent, add it to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Option 2: Django Settings

You can also set it directly in `railannounce/settings.py`:

```python
GEMINI_API_KEY = 'your-api-key-here'
```

**Note:** This is less secure and not recommended for production.

## 📦 Install Dependencies

Install the required package:

```bash
pip install google-generativeai
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## ✅ Verification

After setting up the API key, test the translation:

1. Start your Django server
2. Create an announcement
3. Check the logs to see if translation is working

## 🚀 Benefits

- ✅ **No Docker required** - No need to run LibreTranslate container
- ✅ **Lower resource usage** - No local models or heavy dependencies
- ✅ **Better translations** - Gemini provides high-quality translations
- ✅ **Cloud-based** - No local storage needed for translation models

## ⚠️ Important Notes

- **Internet required**: Gemini API requires internet connection
- **API limits**: Free tier has usage limits (check Google's pricing)
- **Fallback mode**: If API key is not configured, system uses original text (fallback mode)

## 🔄 What Changed

- `announcements/services/translator.py` - Now uses Gemini API
- `railannounce/settings.py` - Uses `GEMINI_API_KEY` instead of `LIBRETRANSLATE_URL`
- `requirements.txt` - Added `google-generativeai` package
- `announcements/tasks.py` - Updated to use Gemini API

## 📝 Language Support

The following languages are supported:
- Hindi (hi)
- Tamil (ta)
- Telugu (te)
- Bengali (bn)
- Kannada (kn)
- English (en)

## 🐛 Troubleshooting

### "GEMINI_API_KEY not configured" warning
- Make sure you've set the environment variable or configured it in settings
- Restart your Django server after setting the environment variable

### Translation not working
- Check if your API key is valid
- Verify internet connection
- Check Django logs for error messages

### API quota exceeded
- Check your Google Cloud Console for API usage
- Consider upgrading your plan if needed

