import os
import datetime
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# SETTINGS
SENDER_EMAIL = 'example@mail adress'
SAVE_DIR = r' local directory path'  # Use raw string (r'...') for Windows paths
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    creds = None

    # Always use absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))  # directory where your script is
    credentials_path = os.path.join(base_dir, 'credentials.json')
    token_path = os.path.join(base_dir, 'token.json')
    
    # Check if token.json already exists
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If no valid credentials or expired, we need to authenticate via OAuth2
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use the credentials.json to initiate the OAuth2 process
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the obtained tokens (access and refresh) in token.json for future use
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)


def save_attachment(service, msg, parts):
    for part in parts:
        filename = part.get('filename')
        body = part.get('body', {})
        if 'attachmentId' in body:
            att_id = body['attachmentId']

            # Get timestamp from the message
            internal_date = int(msg.get('internalDate')) / 1000  # Gmail returns milliseconds
            date_str = datetime.datetime.fromtimestamp(internal_date).strftime('%Y-%m-%d %H-%M-%S')

            # Inject timestamp into filename
            name, ext = os.path.splitext(filename)
            filename_with_time = f"{name}_{date_str}{ext}"

            filepath = os.path.join(SAVE_DIR, filename_with_time)
            if os.path.exists(filepath):
                print(f"Skipped (already exists): {filename_with_time}")
                continue

            att = service.users().messages().attachments().get(
                userId='me', messageId=msg['id'], id=att_id).execute()
            data = base64.urlsafe_b64decode(att['data'].encode('UTF-8'))
            os.makedirs(SAVE_DIR, exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"Saved: {filename_with_time}")


def download_attachments():
    service = authenticate()
    query = f"from:{SENDER_EMAIL} has:attachment"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        parts = msg.get('payload', {}).get('parts', [])
        save_attachment(service, msg, parts)

if __name__ == '__main__':
    try:
        download_attachments()
    except Exception as e:
        with open('error_log.txt', 'a') as f:
            f.write(f"{datetime.datetime.now()} - {str(e)}\n")
