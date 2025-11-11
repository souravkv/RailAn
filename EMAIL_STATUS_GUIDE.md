# Email Status Guide - How to Know If Emails Are Sent

## Quick Status Check

### 1. Check Email Configuration Status
When you visit the **Create Announcement** page (`/announcements/create/`), you'll see:

- **✅ Green Alert**: "Email configured: Ready to send emails from your-email@gmail.com"
  - This means email is properly configured
  
- **⚠️ Yellow Alert**: "Email not configured: Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD..."
  - This means you need to set up email credentials

### 2. Test Email Feature
On the Create Announcement page, there's a **"Test Email Configuration"** section:
1. Enter your email address
2. Click "Send Test Email"
3. Check your inbox (and spam folder)
4. If you receive the test email, your configuration is working!

### 3. After Creating Announcement
When you create an announcement with email recipients:

**Success Messages:**
- ✅ "Announcement #X created and email sent to N recipient(s): email1@example.com, email2@example.com"
  - This confirms emails were sent successfully

**Error Messages:**
- ⚠️ "Email not sent: Email configuration not set"
  - Email credentials are missing
  
- ❌ "Email sending failed: [error message]"
  - There was an error sending the email (check the error message)

### 4. Check Announcement Detail Page
Visit any announcement detail page (`/announcements/announcement/X/`):
- Look for a **"📧 Email Sent"** badge in the header
- This badge only appears if `email_sent = True` in the database

### 5. Check Django Logs
The system now logs all email activity. Check your Django console/logs for:

```
INFO: Attempting to send email to: ['user@example.com']
INFO: From: your-email@gmail.com
INFO: Email send result: 1
INFO: Email sent successfully to 1 recipient(s)
```

Or error messages:
```
ERROR: Email sending failed: [authentication failed / connection refused / etc.]
```

## Troubleshooting

### Email Not Configured
**Problem**: You see "Email not configured" warning

**Solution**:
```bash
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-16-char-app-password"
```

Then restart your Django server.

### Test Email Not Received
1. **Check Spam/Junk folder** - Gmail sometimes filters test emails
2. **Verify App Password** - Make sure you're using a Gmail App Password, not your regular password
3. **Check Logs** - Look for error messages in Django console
4. **Verify Email Address** - Make sure you entered the correct email

### Email Sent But Not Received
1. **Check Spam/Junk folder**
2. **Wait a few minutes** - Sometimes emails are delayed
3. **Verify recipient email** - Make sure the email address is correct
4. **Check Gmail account** - Make sure your sending account isn't blocked

### Common Error Messages

**"Authentication failed"**
- Wrong App Password
- Using regular password instead of App Password
- Email address incorrect

**"Connection refused"**
- Internet connection issue
- Gmail SMTP server issue
- Firewall blocking port 587

**"Email configuration not set"**
- Environment variables not set
- Server not restarted after setting variables

## How to Set Up Email (Quick Steps)

1. **Enable 2FA on Gmail**
2. **Generate App Password**: https://myaccount.google.com/apppasswords
3. **Set Environment Variables**:
   ```bash
   export EMAIL_HOST_USER="your-email@gmail.com"
   export EMAIL_HOST_PASSWORD="xxxx xxxx xxxx xxxx"  # 16-char app password
   ```
4. **Restart Django Server**
5. **Test with Test Email feature**
6. **Create announcement with email recipients**

## Verification Checklist

- [ ] Environment variables set (`EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`)
- [ ] Django server restarted after setting variables
- [ ] Green "Email configured" message on Create page
- [ ] Test email received successfully
- [ ] Success message after creating announcement
- [ ] "Email Sent" badge appears on announcement detail page
- [ ] No error messages in Django logs

If all checkboxes are checked, emails should be working! 🎉

