'''
This file contains all the configuration variables for the application.
'''
import os
from typing import TypedDict
from gspread import Worksheet

LOGTAIL_TOKEN = os.getenv('LOGTAIL_TOKEN')

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

SHEET_NAME = 'library-management-system'
CREDS_PATH = 'creds.json'


class WorksheetSet(TypedDict):
    '''
    :param title: title of worksheet
    :param headers: list of header titles for the worksheet header row
    :param w_sheet: gspread Worksheet instance
    '''
    title: str
    headers: list[str]
    w_sheet: None | Worksheet


WORKSHEETS: list[WorksheetSet] = [
    {
        'title': 'stock',
        'headers': ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies'],
        'w_sheet': None
    },
    {
        'title': 'borrowed',
        'headers': ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies', 'Borrower', 'Borrowed Date', 'Due Date'],
        'w_sheet': None
    }
]
