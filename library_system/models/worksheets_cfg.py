from typing import TypedDict
from gspread import Worksheet
from enum import Enum


class WorksheetSet(TypedDict):
    '''
    :param title: title of worksheet
    :param headers: list of header titles for the worksheet header row
    :param w_sheet: gspread Worksheet instance
    '''
    title: str
    headers: list[str]
    w_sheet: None | Worksheet


class WorksheetSets(Enum):
    '''
    Headers must match the `Book` model fields.
    Enum of `WorksheetSet` instances.
    Each `WorksheetSet` contains: worksheet `title`, `headers` and `w_sheet`(gspread `Worksheet` instance).

    Example. To get `Worksheet` instance of `stock` google worksheet by title:
    use `WorksheetSets.stock.value['w_sheet']`:
        >>> WorksheetSets.stock.value['w_sheet']
        <Worksheet 'stock' id:0>  # returns Worksheet instance or None
    '''
    stock = WorksheetSet(
        title='stock',
        headers=['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies'],
        w_sheet=None
    )
    borrowed = WorksheetSet(
        title='borrowed',
        headers=['ISBN', 'Title', 'Author', 'Genre', 'Year',
                 'Copies', 'Borrower', 'Borrowed Date', 'Due Date'],
        w_sheet=None
    )
