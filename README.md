# Divinity-Original-Sin-2-Save-Sync
- **This tool syncs a shared folder in a specified place for all users added to the folder. This was not something we could accomplish using the Google Drive desktop app.**
- **This uses the Google cloud platform, but I was unable to make a publicly accessible version, meaning if you wish to use this you need to setup a project yourself.**
### **This is an extremely tedious setup, you may be better off just using a shared drive folder and manually updating saves lol.**
# Tutorial to do so:
- Navigate to https://console.cloud.google.com/
- Create a cloud project (This process need only be done by one person, anyone else can simply connect to the project)

![google cloud create project](https://user-images.githubusercontent.com/48575634/156899745-8c96b481-3bd0-400e-8346-905a539973da.PNG)
- Navigate to the home page, you should see your project selected at the top, if not, select it.

![project created google](https://user-images.githubusercontent.com/48575634/156899773-2dc53955-6a0c-48fb-928b-5f99903d05ed.PNG)
- Find the APIs and services page and select the credentials tab

![create credentials](https://user-images.githubusercontent.com/48575634/156899792-6cc4df25-a099-41d4-9da8-b8654cfccc52.PNG)
- We need to create credentials, but first it should ask you to configure the OAuth consent screen. Follow the link to do so.

![configure consent screen](https://user-images.githubusercontent.com/48575634/156899809-37cf58af-1147-410c-8da7-862b1c0a07dc.PNG)
- Select External and hit create.
- Now you should be tasked with filling out a short form, you need only fill out the require fields and add test users.

![fill out oauth info](https://user-images.githubusercontent.com/48575634/156899837-5e9a8144-2533-439d-943c-3cbe4185b49c.PNG)

- You should see this somewhere, select add users.

![test users](https://user-images.githubusercontent.com/48575634/156900326-a8bb87d7-c8f5-4610-9173-c79938d82b8e.PNG)

- Test users are the people that will be allowed to use the app. This means adding the google accounts of anyone who wishes to be part of the app.
- Once that's done, head back to the credentials page and select create credentials. You should see a drop down, pick OAuth client ID

![create oauth id](https://user-images.githubusercontent.com/48575634/156899850-c605e913-473c-439d-8fa4-a50533d66720.PNG)
- Choose desktop app, name it whatever you like

![create oauth cred](https://user-images.githubusercontent.com/48575634/156899855-26c835e0-d76c-4657-a744-41ebe389bb6e.PNG)
- Upon creation, go back to the credentials page if it hasn't taken you their itself.
- You should see your newly generated OAuth Client ID, (Though may take up to five minutes) click the download button on the far right

![download json](https://user-images.githubusercontent.com/48575634/156899912-50210b33-8c08-41e3-8805-ddd54b093071.PNG)
- Don't alter the fields, and click Download JSON
- Rename this file to client_secret and drop it in the root directory of the project

![client_secret](https://user-images.githubusercontent.com/48575634/156899930-f377e4d6-5495-4566-becb-5536178f1baa.PNG)

**All users should have the identical client_secret.json file in their root folder**
## Onto Python (This part needs to be done by all users)
- Make sure you have Python 3.7 or newer installed.
- Install the neccesary google libraries:
``` pip install -U pip google-api-python-client oauth2client --user ```
- If you run into a pip error, its likely because python is incorrectly setup as a System Path variable. There are plenty of short tutorials online as to how to fix this if you are unfamiliar.
- run drive_share.py for the first time, and it should open up a page in your web browser asking you to authorize the app. Do so.
- you should notice a newly created file called storage.json in the root directory
## Configure files
- There should be 2 text files you need to configure
- **path.txt** should contain the path to the save file you are syncing.
- For instance mine contains ```C:\Users\Sam\Documents\Larian Studios\Divinity Original Sin 2 Definitive Edition\PlayerProfiles\BigManGang\Savegames\Story\MainSave\```
Where \MainSave\ is the directory that contains the two relevant save files. **In the current version of the app, the name is require to be consistent with the name that is present on google drive. Divinity dyanmically chooses names based on location and time, so whenever any of us ends a session, we manually save over the "MainSave" so that it remains the same.**
- Replace the path file that is arleady in there
- There should also be a file called **folder_id.txt**. This should contain the id of the shared drive folder.
- This can be found in the URL when you visit the folder in Google Drive, replace the id that's already in the file

![drive folder id](https://user-images.githubusercontent.com/48575634/156900554-18841bf1-5465-4da8-ad47-f2261f2345f8.PNG)

**Make sure everyone has edit access to the folder**

Now, The next time you run drive_share.py it should continuously check for updated saves, downloading them when necessary.
You can also run drive_share_no_terminal.py for a version that runs in the background. While running you should python process in task manager consuming around 20-30mb, this is likely that. I personally set this to run on startup, so I never need to think about opening it.

## Uploading Saves
- Uploading is done by running upload_save.py
- This should be the only part of this tool that is not fully automated (if drive_share_no_terminal.py launches on startup)
- You need only double click and it should handle everything and then close.
- I considered automating this, but was concerened with accidental overwrites.
