from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import time
from datetime import datetime

with open('path.txt', 'r') as f:
    path = f.read()

if path is None:
    exit()
# formatting help
if path[-1] == '\n':
    path = path[:-1]
if path[-1] != '/':
    path += '/'

#Auth and DRIVE service setup
SCOPES = ['https://www.googleapis.com/auth/drive']
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))


# Helper functions
def download_file(id, filename):
    request = DRIVE.files().get_media(fileId=id)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        time.sleep(2)

def download_all(files, folder_id):
    for f in files:
        if f['mimeType'] != 'application/vnd.google-apps.folder':
            download_file(f['id'], path+f['name'])
            with open('last_download.txt', 'w') as f:
                f.write(str(DRIVE.files().get(fileId=files[0]['id'], fields="modifiedTime").execute()['modifiedTime']))

divin_folder_id = '19c_E1naS7KQ_JE0RfBKXq-8srxaB13GZ'

# save folder metadata
divin_folder = DRIVE.files().get(fileId='19c_E1naS7KQ_JE0RfBKXq-8srxaB13GZ').execute()

# get all files from divin_folder
files = DRIVE.files().list(q="'" + divin_folder_id + "' in parents").execute().get('files', [])

while True:
    with open('last_download.txt', 'r') as f:
        last_mod_download = f.read()
    if DRIVE.files().get(fileId=files[0]['id'], fields="modifiedTime").execute()['modifiedTime'] > last_mod_download:
        download_all(files, divin_folder_id)
    time.sleep(10)

