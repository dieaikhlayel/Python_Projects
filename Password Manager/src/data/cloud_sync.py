import os
import json
import pickle
from pathlib import Path
from typing import Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class CloudSyncManager:
    def __init__(self, config):
        self.config = config
        self.service = None
        self.credentials = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive"""
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = None
        
        token_file = Path('token.pickle')
        credentials_file = Path('credentials.json')
        
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not credentials_file.exists():
                    print("Google Drive credentials not found. Cloud sync disabled.")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.credentials = creds
        self.service = build('drive', 'v3', credentials=creds)
    
    def upload_backup(self, db_path: str, description: str = "Password manager backup"):
        """Upload database backup to Google Drive"""
        if not self.service:
            return False
        
        try:
            # Create backup filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"password_manager_backup_{timestamp}.db"
            
            file_metadata = {
                'name': backup_name,
                'description': description,
                'mimeType': 'application/x-sqlite3'
            }
            
            media = MediaFileUpload(db_path, mimetype='application/x-sqlite3')
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            
            print(f"Backup uploaded successfully: {file.get('id')}")
            return True
            
        except Exception as e:
            print(f"Backup upload failed: {e}")
            return False
    
    def list_backups(self) -> list:
        """List available backups in Google Drive"""
        if not self.service:
            return []
        
        try:
            results = self.service.files().list(
                q="mimeType='application/x-sqlite3' and name contains 'password_manager_backup'",
                pageSize=10,
                fields="files(id, name, createdTime, size)"
            ).execute()
            
            return results.get('files', [])
        except Exception as e:
            print(f"Failed to list backups: {e}")
            return []
    
    def download_backup(self, file_id: str, download_path: str) -> bool:
        """Download a backup from Google Drive"""
        if not self.service:
            return False
        
        try:
            request = self.service.files().get_media(fileId=file_id)
            with open(download_path, 'wb') as f:
                f.write(request.execute())
            return True
        except Exception as e:
            print(f"Backup download failed: {e}")
            return False