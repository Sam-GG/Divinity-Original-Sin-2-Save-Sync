from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import time
from datetime import datetime
global DRIVE

print("Checking path")
with open('path.txt', 'r') as f:
    path = f.read()
print("Path: " + path)
if path is None:
    print("No path specified")
    exit()
# formatting help
if path[-1] == '\n':
    path = path[:-1]
if path[-1] != '/':
    path += '/'


def auth():
    """
        summary: Authenticates with Google Drive and returns a Drive service object.
    """
    print("performing auth setup")
    SCOPES = ['https://www.googleapis.com/auth/drive']
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return discovery.build('drive', 'v3', http=creds.authorize(Http()))


# Helper functions
def download_file(id, filename):
    request = DRIVE.files().get_media(fileId=id)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

def download_all(files, folder_id):
    for f in files:
        if f['mimeType'] != 'application/vnd.google-apps.folder':
            download_file(f['id'], path+f['name'])
            with open('last_download.txt', 'w') as f:
                f.write(str(DRIVE.files().get(fileId=files[0]['id'], fields="modifiedTime").execute()['modifiedTime']))


# perform auth and get drive service object
DRIVE = auth()

# folder id's can be found in the url of the drive folder webpage
print("Checking folder id")
with open('folder_id.txt', 'r') as f:
    divin_folder_id = f.read()
print("Folder id: " + divin_folder_id)

# save folder metadata
divin_folder = DRIVE.files().get(fileId='19c_E1naS7KQ_JE0RfBKXq-8srxaB13GZ').execute()

# get all files from divin_folder
files = DRIVE.files().list(q="'" + divin_folder_id + "' in parents").execute().get('files', [])

while True:
    print("checking for new saves every 10 seconds..")
    try:
        with open('last_download.txt', 'r') as f:
            last_mod_download = f.read()

        # need to make sure non-folder. G Drive does not update modified time for parent folders, only files.
        i = 0
        some_file = DRIVE.files().get(fileId=files[i]['id']).execute()

        while some_file['mimeType'] == 'application/vnd.google-apps.folder':
            i += 1
            some_file = DRIVE.files().get(fileId=files[i]['id']).execute()

        print(DRIVE.files().get(fileId=files[i]['id'], fields="modifiedTime").execute()['modifiedTime'])
        if DRIVE.files().get(fileId=files[i]['id'], fields="modifiedTime").execute()['modifiedTime'] > last_mod_download:
            download_all(files, divin_folder_id)
            print('downloaded newer save')
        # elif DRIVE.files().get(fileId=divin_folder_id, fields="modifiedTime").execute()['modifiedTime'] < last_mod_download:
        #     update_all(files)
        #     print('uploaded newer save') 
        else:
            print('no changes')
    except Exception as e:
        print(e)
        print("attempting re-authentication")
        DRIVE = auth()
    time.sleep(10)

