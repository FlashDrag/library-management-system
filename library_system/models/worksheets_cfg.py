from typing import TypedDict
from gspread import Worksheet


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