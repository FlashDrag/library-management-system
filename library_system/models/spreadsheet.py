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


if __name__ == '__main__':
    from library_system.config import SHEET_NAME, CREDS_PATH

    library = Library(SHEET_NAME, CREDS_PATH)
    library.connect()
    if not library.isConnected:
        print('Cannot connect to the Library Spreadsheet. Exiting...')
    else:
        print('Succesfully connected.')

    library.set_worksheets(list(WorksheetSets))

    book = Book(title='Python')
    book_field = BookFields.title
    finded_books = library.search_books(
        book[book_field.name], book_field, WorksheetSets.stock.value
    )
    print(finded_books)
