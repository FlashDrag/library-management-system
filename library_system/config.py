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

SHEET_NAME: str = 'library-management-system'
CREDS_PATH: str = 'creds.json'
WORKSHEETS = {
    'stock': {
        'headers': ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies'],
        'wsheet': None
    },
    'borrowed': {
        'headers': ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies', 'Borrower', 'Borrowed Date', 'Due Date'],
        'wsheet': None
    }
}
