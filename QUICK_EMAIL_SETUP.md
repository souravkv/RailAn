# Quick Email Setup Guide

## Option 1: Run Export Commands (Temporary - Current Session Only)

**In the terminal where you'll run Django server:**

```bash
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-16-char-app-password"
```

**⚠️ Important:**
- These variables only last for the current terminal session
- You must run these commands **BEFORE** starting Django server
- If Django is already running, you need to **restart it** after setting variables

## Option 2: Use the Setup Script (Recommended)

```bash
cd /home/zourv/Documents/PROJEX/Django_project
./setup_email.sh
```

This script will:
- Prompt you for email and password
- Set the environment variables
- Show you how to make them permanent

## Option 3: Make It Permanent

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-16-char-app-password"
```

Then reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

## Verify It's Working

1. **Check if variables are set:**
   ```bash
   echo $EMAIL_HOST_USER
   echo $EMAIL_HOST_PASSWORD
   ```

2. **Start/Restart Django server:**
   ```bash
   python3 manage.py runserver
   ```

3. **Visit Create Announcement page:**
   - Go to: http://localhost:8000/announcements/create/
   - You should see: **"✓ Email configured: Ready to send emails from your-email@gmail.com"**

4. **Test Email:**
   - Use the "Test Email Configuration" section
   - Enter your email and click "Send Test Email"
   - Check your inbox!

## Common Issues

### "Email not configured" still showing?
- Make sure you **restarted Django server** after setting variables
- Check variables are set: `echo $EMAIL_HOST_USER`
- Make sure you're in the same terminal session

### Variables disappear after closing terminal?
- Use Option 3 to make them permanent
- Or use the setup script each time

### Still not working?
- Check you're using Gmail App Password (not regular password)
- Verify App Password is 16 characters (remove spaces if any)
- Check Django console for error messages

