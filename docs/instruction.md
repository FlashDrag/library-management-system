# How to connect to Google Spreadsheet API and get creadentials

1. Create a spreadsheet with Google Sheets
2. Activate API credentials:
- Open Google Cloud Platform: https://console.cloud.google.com/
- Create `New Project`
- Enable 2 APIs (`APIs & Services` > `Library`):
    1. `Google Drive API` > `Enable`
        - Generate credentials:
            * `Google Drive API` > `Create Credentials` > (Service account)
            * API: Google Drive API;
            * Application data;
            * I'm not using this API with Compute Engine, Kubernetes Engine, App Engine, or Cloud Functions
            * Service acc name and service acc ID - can be same as project name
            * Role: Editor
        - Load a file with credentials:
            * `APIs & Services` > `Credentials` > `Service Accounts` > select your acc
            * In your service acc select `KEYS` > `ADD KEY` > `Create new Key` > `JSON`
    2. Google Sheets
        - Select `APIs & Services` > `Library` > `Google Sheets API` > Enable
3. Share access to Google sheets for service account:
- Open your sheet in google and click `Share` green button
- Copy client email from downloaded credits json file and paste in sheet access:
    * Make sure `Editor` is selected
    * Untick `Notify People`
4. Move the json credentials file to repo and rename it to creds.json
    * Hide the file, adding to .gitignore
5. Install:
- google auth - to set up the authentication needed to access the google cloud project
- gspread - library for acccesing and updating data in the spreadsheet

    **pip install --upgrade gspread google_auth**


[Back to Readme](https://github.com/FlashDrag/library-management-system/blob/main/README.md)