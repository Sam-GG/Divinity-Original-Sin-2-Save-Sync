from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import time
from datetime import datetime

print("Checking path")
with open('path.txt', 'r') as f:
    path = f.read()
print("Path: " + path)

# formatting help
if path[-1] == '\n':
    path = path[:-1]
if path[-1] != '/':
    path += '/'

print("performing auth setup")
#Auth and DRIVE service setup
SCOPES = ['https://www.googleapis.com/auth/drive']
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

def update_all(files):
    for f in files:
        if f['mimeType'] != 'application/vnd.google-apps.folder':
            media_content = MediaFileUpload(path+f['name'], mimetype=f['mimeType'])
            DRIVE.files().update(fileId=f['id'], media_body=media_content).execute()
            with open('last_download.txt', 'w') as fi:
                fi.write(str(DRIVE.files().get(fileId=f['id'], fields="modifiedTime").execute()['modifiedTime']))

divin_folder_id = '19c_E1naS7KQ_JE0RfBKXq-8srxaB13GZ'

# get all files from divin_folder
files = DRIVE.files().list(q="'" + divin_folder_id + "' in parents").execute().get('files', [])
print("uploading files..")
update_all(files)
print('updated all files. done.')
time.sleep(2)
exit()
