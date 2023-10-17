import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the SCOPES for Google Drive API.
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_and_build_service():
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and it is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def getFileList(N):
    service = authenticate_and_build_service()

    # Define the MIME types for the text formats you want to filter.
    text_formats = [
        "application/pdf", 
        # "text/plain", 
        # "application/msword"
    ]
    
    # Build the query string to filter by MIME type
    mime_query = " or ".join([f"mimeType='{format}'" for format in text_formats])
    
    # Remove files which are deleted 
    query = f"({mime_query}) and trashed=false"

    result = service.files().list(
        pageSize=N, 
        fields="files(id, name, webViewLink)",
        q=query
        ).execute()
    return result

# Get list of first 5 files or folders from your Google Drive Storage
result_dict = getFileList(10)

# Extract the list from the dictionary
file_list = result_dict.get('files')

# Print every file's name
for file in file_list:
    print(file['name'] + ": " + file['id'])

def get_file_id_list():
    return [file['id'] for file in file_list]