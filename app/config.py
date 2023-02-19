'''
This file contains all the configuration variables for the application.
'''

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

SHEET_NAME: str = 'library-management-system'
CREDS_PATH: str = 'creds.json'
WORKSHEETS = [
    {
        'title': 'stock',
        'headers': ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies']
    },
    {
        'title': 'borrowed',
        'headers': ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies', 'Borrower', 'Borrowed Date', 'Due Date']
    },
]
