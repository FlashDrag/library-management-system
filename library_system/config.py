'''
This file contains all the configuration variables for the application.
'''

import os
import gspread as gs

LOGTAIL_TOKEN = os.getenv('LOGTAIL_TOKEN')

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

SHEET_NAME: str = 'library-management-system'
CREDS_PATH: str = 'creds.json'
WORKSHEETS: dict[str, dict[str, list[str] | None | gs.Worksheet]] = {
    'stock': {
        'headers': ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies'],
        'wsheet_obj': None
    },
    'borrowed': {
        'headers': ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies', 'Borrower', 'Borrowed Date', 'Due Date'],
        'wsheet_obj': None
    }
}
