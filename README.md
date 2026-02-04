# Gmail Attachment Downloader (Python)

A Python automation script that downloads email attachments from a specified Gmail sender and saves them locally.  
Designed for scheduled or interval-based execution (cron, Task Scheduler, etc.).

## 🚀 Features

- Downloads attachments from a specific sender
- Automatically authenticates using Gmail OAuth 2.0
- Prevents duplicate downloads
- Adds timestamp to filenames
- Logs errors to a file
- Suitable for automation and scheduling

## 📁 How It Works

1. Authenticates with Gmail using OAuth 2.0
2. Searches emails from a specified sender containing attachments
3. Downloads attachments to a local directory
4. Appends email timestamp to filenames
5. Skips files that already exist

## 🔧 Requirements

- Python 3.7+
- Gmail API enabled
- Google OAuth credentials

Install dependencies:
```bash
pip install -r requirements.txt
