from typing import TypedDict
from gspread import Worksheet
from enum import Enum
from library_system.models.book import BookFields, BorrowerFields


class WorksheetSet(TypedDict):
    '''
    :param title: title of worksheet
    :param headers: list of header titles for the worksheet header row,
    from `BookFields` enum.
    e.g. ['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies']
    :param fields: list of fields of `Book` model, from `BookFields` enum.
    e.g. ['isbn', 'title', 'author', 'genre', 'year', 'copies', 'borrower', 'borrow_date', 'due_date']
    :param w_sheet: gspread Worksheet instance
    '''
    title: str
    headers: list[str]
    fields: list[str]
    w_sheet: None | Worksheet


class WorksheetSets(Enum):
    '''
    Enum of `WorksheetSet` instances.
    Each `WorksheetSet` contains: worksheet `title`, `headers` and `w_sheet`(gspread `Worksheet` instance).

    Example. To get `Worksheet` instance of `stock` google worksheet by title:
    use `WorksheetSets.stock.value['w_sheet']`:
        >>> WorksheetSets.stock.value['w_sheet']
        <Worksheet 'stock' id:0>  # returns Worksheet instance or None
    '''
    stock = WorksheetSet(
        title='stock',
        headers=list(map(lambda field: field.value, BookFields)),
        fields=list(map(lambda field: field.name, BookFields)),
        w_sheet=None
    )
    borrowed = WorksheetSet(
        title='borrowed',
        headers=list(map(lambda field: field.value, BorrowerFields)),
        fields=list(map(lambda field: field.name, BorrowerFields)),
        w_sheet=None
    )
