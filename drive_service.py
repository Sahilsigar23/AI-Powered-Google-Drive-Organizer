
import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import config

class DriveService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticates the user with Google Drive API."""
        if os.path.exists(config.TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, config.SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(config.CREDENTIALS_FILE):
                    raise FileNotFoundError(f"Credentials file '{config.CREDENTIALS_FILE}' not found. Please download it from Google Cloud Console.")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.CREDENTIALS_FILE, config.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(config.TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('drive', 'v3', credentials=self.creds)
        except HttpError as error:
            print(f"An error occurred: {error}")
            self.service = None

    def list_files(self, page_size=100):
        """Lists files in the root directory."""
        if not self.service:
            return []
        
        results = self.service.files().list(
            pageSize=page_size,
            fields="nextPageToken, files(id, name, mimeType, parents)",
            q="'root' in parents and trashed=false" 
        ).execute()
        return results.get('files', [])

    def create_folder(self, folder_name, parent_id=None):
        """Creates a folder if it doesn't exist."""
        if not self.service:
            return None
            
        # Check if folder exists
        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        existing = self.service.files().list(q=query, fields='files(id)').execute()
        files = existing.get('files', [])
        
        if files:
            return files[0]['id']
        
        # Create new folder
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
            
        file = self.service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

    def move_file(self, file_id, folder_id):
        """Moves a file to a specific folder."""
        if not self.service:
            return False

        if config.DRY_RUN:
            file = self.service.files().get(fileId=file_id, fields='name').execute()
            print(f"[DRY RUN] Would move file '{file.get('name')}' ({file_id}) to folder ID {folder_id}")
            return True

        try:
            # Retrieve the existing parents to remove
            file = self.service.files().get(fileId=file_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            
            # Move the file by adding the new parent and removing the old one
            self.service.files().update(
                fileId=file_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
            return True
        except HttpError as error:
            print(f"An error occurred moving file: {error}")
            return False

    def export_file(self, file_id, mime_type):
        """Exports a Google Doc/Sheet to a readable format."""
        if not self.service:
            return None
        
        try:
            request = self.service.files().export_media(fileId=file_id, mimeType=mime_type)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            return file.getvalue()
        except HttpError as error:
            print(f"Error exporting file: {error}")
            return None

    def download_file(self, file_id):
        """Downloads a binary file (PDF, Image)."""
        if not self.service:
            return None
            
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            return file.getvalue()
        except HttpError as error:
            print(f"Error downloading file: {error}")
            return None
