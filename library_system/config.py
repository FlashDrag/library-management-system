'''
This file contains all the configuration variables for the application.
'''
import os


LOGTAIL_TOKEN = os.getenv('LOGTAIL_TOKEN')

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

SHEET_NAME = 'library-management-system'
CREDS_PATH = 'creds.json'
