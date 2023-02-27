import logging
import re

import gspread as gs
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError

from library_system.models.worksheets_cfg import WorksheetSets, WorksheetSet
from library_system.models.book import Book, BookFields

logger = logging.getLogger(__name__)


class Library:
    '''
    Library class that connects to a Google Sheet and provides methods to interact with it.

    Class attributes:
    :param `SCOPE`: Google API scope.

    Instance attributes:
    :param `sheet_name`: Name of the Google Sheet.
    :param `creds_path`: Path to credentials file.

    :param `_SHEET`: `Spreadsheet` instance.
    :param `isConnected`: indicates if the Library is connected to the Google Sheet.
    '''

    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, sheet_name: str, creds_path: str) -> None:
        self._sheet_name = sheet_name
        self._creds_path = creds_path

        self.s_sheet: gs.Spreadsheet | None = None
        self.isConnected: bool = False

    def connect(self) -> None:
        '''
        Connect to the Google Sheet specified in the `sheet_name` parameter,
        using the credentials in the file at `creds_path`.
        - Create `s_sheet` attr as a `Spreadsheet` instance of the Google Sheet
        - Set `isConnected` attr to `True` if the connection is successful
        '''
        try:
            scope = Credentials.from_service_account_file(
                self._creds_path, scopes=self.SCOPE)
            client = gs.authorize(scope)
            self.s_sheet = client.open(self._sheet_name)
            self.isConnected = True
        except FileNotFoundError:
            logger.error(f'Credentials file not found at {self._creds_path}.')
        except GoogleAuthError:
            logger.error(
                'GoogleAuthError: Check your credentials or try again later.')
        except gs.exceptions.SpreadsheetNotFound:
            logger.error(f'Spreadsheet {self._sheet_name} not found!')
        except gs.exceptions.GSpreadException as e:
            logger.error(e)
        except Exception as e:
            # catch-all Exception block is still included to handle any unexpected errors that may occur
            logger.error(f"An unexpected error occurred: {e}")

    def set_worksheets(self, w_sets: list[WorksheetSets]) -> None:
        '''
        Sets worksheets for the `Library` instance.
        Add new worksheets to the `Google Spreadsheet`
        if they don't exist based on `WorksheetSet` parameters of `w_sets` list.

        Creates `gspread.Worksheet` instances for each `Google Worksheet`
        and adds them to the apropriated `WorksheetSet` dicts as `w_sheet` parameter.

        :param w_sets: list of `WorksheetSets` enums containing the `WorksheetSet` dicts
        '''
        if self.s_sheet is None:
            raise gs.exceptions.GSpreadException(
                'Spreadsheet is not connected.')

        # get the list of worksheets titles from the google spreadsheet
        google_sheet_titles = list(
            map(lambda sheet: sheet.title, self.s_sheet.worksheets()))

        for w_set in w_sets:
            title = w_set.value['title']
            headers = w_set.value['headers']

            if title not in google_sheet_titles:
                worksheet = self.s_sheet.add_worksheet(
                    title, rows=100, cols=len(headers)
                )
            else:
                worksheet = self.s_sheet.worksheet(title)

            # update the first row with the headers
            worksheet.update('A1', [headers])
            # set gspread Google worksheet instance to `WorksheetSet` dict to `w_sheet` parameter
            w_set.value['w_sheet'] = worksheet

    def search_books(self, book_value: str, book_field: BookFields, w_set: WorksheetSet) -> list[dict]:
        # TODO: exlude worksheet header row from search
        '''
        Search a book value with the specified worksheet header - `book_field` and
        in the specified worksheet - `w_set`.

        :param `book_value`: validated book value search for.
        :param `book_field`: The worksheet header to search by.
        :param `w_set`: The worksheet to search in.

        :return: A list of dictionaries containing the book details.

        Example return:
        [{'ISBN': '9781449357351', 'Title': 'Python Cookbook', 'Author': 'David Beazley, Brian K. Jones',
         'Genre': 'Computers', 'Year': '2013', 'Copies': '16', 'cell_row': 84},]
        '''

        worksheet = w_set['w_sheet']
        # get the name of the enum value, which is the same as the header name
        field = book_field.name

        if worksheet is None:
            raise ValueError(
                f"Can't to find the worksheet <{w_set['title']}>"
            )

        # get the column number of the header
        header: gs.Cell | None = worksheet.find(
            field, in_row=1, case_sensitive=False
        )
        if header is None:
            raise ValueError(
                f"Can't to find the header <{field}> in the worksheet <{w_set['title']}>"
            )
        col_num = header.col

        # find all cells with the specified value in the column of the header
        if book_field in (BookFields.title, BookFields.author, BookFields.genre):
            # match the value substring
            regex = re.compile(rf'.*{book_value}.*', re.IGNORECASE)
        else:
            # match the exact value
            regex = re.compile(rf'^{book_value}$', re.IGNORECASE)
        matched_cells: list[gs.Cell] = worksheet.findall(
            regex, in_column=col_num, case_sensitive=False
        )

        # create a list of dictionaries containing the book details
        headers = w_set['headers'] + ['cell_row']
        result_list = []
        for cell in matched_cells:
            value_list = worksheet.row_values(cell.row) + [cell.row]
            value_dict = dict(zip(headers, value_list))
            result_list.append(value_dict)

        return result_list

    def add_book_copies(self, book_to_add: dict, copies: int) -> dict:
        '''
        Add copies to the existing book in the stock worksheet.

        :param book_to_add: A dictionary containing the book details.
        :param copies: The number of copies to add.
        :return: Dictionary containing a book with updated number of copies.
        '''
        cell_row = book_to_add['cell_row']
        current_copies = book_to_add['Copies']
        if not current_copies or not current_copies.isdigit():
            new_num_copies = copies
        else:
            new_num_copies = int(current_copies) + copies
        field = BookFields.copies.name
        w_set = WorksheetSets.stock
        if not w_set.value['w_sheet']:
            raise ValueError(
                f"Can't to find the worksheet <{w_set.name}>"
            )
        header = w_set.value['w_sheet'].find(
            field, in_row=1, case_sensitive=False
        )
        if not header:
            raise ValueError(
                f"Can't to find the header <{field}> in the worksheet <{w_set.name}>"
            )
        col_num = header.col

        w_set.value['w_sheet'].update_cell(cell_row, col_num, new_num_copies)
        book_to_add['Copies'] = new_num_copies
        return book_to_add

    def append_book(self, book: Book, w_set: WorksheetSets):
        '''
        Append a book to the worksheet.
        Will be added only the fields specified in the `WorksheetSet`.

        :param book: A `Book` model instance.
        :param w_set: The `WorksheetSet` enum to append the book to.
        :return: A dictionary containing the book details.
        '''
        fields = w_set.value['fields']
        # create a dictionary containing only the fields specified in the `WorksheetSet`
        book_to_add = book.dict(include=set(fields))
        w_sheet = w_set.value['w_sheet']
        if not w_sheet:
            raise ValueError(
                f"Can't to find the worksheet <{w_set.name}>"
            )
        if not book_to_add:
            raise ValueError(
                f"Can't to add an empty book to the worksheet <{w_set.name}>"
            )
        # get the values of the book dictionary in the same order as the headers in the worksheet
        values = [book_to_add.get(field) for field in fields]
        w_sheet.append_row(values)
        return book_to_add


# for testing purposes
# The below code will be executed only if this module is run as a script
if __name__ == '__main__':
    from library_system.config import SHEET_NAME, CREDS_PATH

    library = Library(SHEET_NAME, CREDS_PATH)
    library.connect()
    if not library.isConnected:
        print('Cannot connect to the Library Spreadsheet. Exiting...')
    else:
        print('Succesfully connected.')

    library.set_worksheets(list(WorksheetSets))

    # search books
    book = Book(title='Python')
    book_field = BookFields.title
    finded_books = library.search_books(
        book[book_field.name], book_field, WorksheetSets.stock.value
    )
    print(finded_books)

    # add book copies
    book_to_add = finded_books[1]
    copies = 3
    updated_book = library.add_book_copies(book_to_add, copies)
    print(updated_book)

    # append book
    book = Book(
        isbn='978-3-16-148410-0',
        title='The Lord of the Rings',
        author='J.R.R. Tolkien',
        genre='Fantasy',
        year='2001',
        copies='2',
        borrower='John Doe',
        borrow_date='2023-02-25',
        due_date='2023-04-1',
    )
    appended_book = library.append_book(book, WorksheetSets.stock)
    print(appended_book)
