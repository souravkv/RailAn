# Gmail SMTP Setup Guide

## Overview
RailAnnounce now supports sending email notifications when announcements are created. This uses Gmail's SMTP service.

## Setup Instructions

### 1. Enable 2-Factor Authentication
- Go to your Google Account settings
- Enable 2-Factor Authentication if not already enabled

### 2. Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Enter "RailAnnounce" as the name
4. Click "Generate"
5. Copy the 16-character password (you'll need this)

### 3. Set Environment Variables
Set these environment variables before running the Django server:

```bash
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-16-char-app-password"
```

Or add them to your `.env` file if you're using one.

### 4. Test Email Configuration
The email will be sent automatically when:
- An announcement is created
- Email recipients are provided in the form
- EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are set

## Usage

When creating an announcement:
1. Fill in the announcement details
2. In the "Send Email Notification To" field, enter email addresses separated by commas
   - Example: `user1@example.com, user2@example.com`
3. Submit the form
4. Emails will be sent to all recipients with announcement details

## Email Content

The email includes:
- Announcement title (or ID)
- Description (if provided)
- Full announcement text
- Handler name
- Location
- Time
- Contact number
- Priority
- Status
- Language
- Link to view full details

## Troubleshooting

### Email not sending?
1. Check that EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are set
2. Verify the App Password is correct (16 characters, no spaces)
3. Check that 2FA is enabled on your Google account
4. Check Django logs for error messages

### "Authentication failed" error?
- Make sure you're using an App Password, not your regular Gmail password
- Verify the email address is correct

### "Connection refused" error?
- Check your internet connection
- Verify Gmail SMTP settings (smtp.gmail.com:587)

