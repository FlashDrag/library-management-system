from typing import TypedDict
from gspread import Worksheet
from enum import Enum
from library_system.models.book import BookFields, BorrowFields


class WorksheetSet(TypedDict):
    '''
    :param title: title of worksheet
    :param fields: list of header titles for the worksheet header row and for `Book` model,
    from `BookFields` enum or `BorrowFields` enum.
    e.g. ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies']
    e.g. ['isbn', 'title', 'author', 'genre', 'year', 'borrower', 'borrow_date', 'due_date']
    :param w_sheet: gspread Worksheet instance
    '''
    title: str
    fields: list[str]
    w_sheet: None | Worksheet


class WorksheetSets(Enum):
    '''
    Enum of `WorksheetSet` instances.
    Each `WorksheetSet` contains: worksheet `title`, `fields` and `w_sheet`(gspread `Worksheet` instance).

    Example. To get `Worksheet` instance of `stock` google worksheet by title:
    use `WorksheetSets.stock.value['w_sheet']`:
        >>> WorksheetSets.stock.value['w_sheet']
        <Worksheet 'stock' id:0>  # returns Worksheet instance or None
    '''
    stock = WorksheetSet(
        title='stock',
        fields=list(map(lambda field: field.name, BookFields)),
        w_sheet=None
    )
    borrowed = WorksheetSet(
        title='borrowed',
        fields=list(map(lambda field: field.name, BorrowFields)),
        w_sheet=None
    )
