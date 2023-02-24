import logging

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
    :param `w_sets`: `WorksheetSets` Enum instance.

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
    w_sets = WorksheetSets

    def __init__(self, sheet_name: str, creds_path: str) -> None:
        self._sheet_name = sheet_name
        self._creds_path = creds_path

        self.s_sheet: gs.Spreadsheet | None = None
        self.isConnected: bool = False

    def connect(self):
        '''
        Connect to the Google Sheet specified in the `sheet_name` parameter,
        using the credentials in the file at `creds_path`.
        - Create `_SHEET` private attribute with a `Spreadsheet` instance.
        - Create `stock_sheet` attr as a `Worksheet` instance of the 'stock'
        worksheet
        '''
        try:
            scope = Credentials.from_service_account_file(
                self._creds_path, scopes=self.SCOPE)
            client = gs.authorize(scope)
            self.s_sheet = client.open(self._sheet_name)
            self._set_worksheets()
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

    def _set_worksheets(self):
        '''
        Sets worksheets for the `Library` instance.
        Add new worksheets to the `Google Spreadsheet` if they don't exist based on `WorksheetSet` parameters.

        Creates `gspread.Worksheet` instances for each `Google Worksheet`
        and adds them to the `self.worksheets` list as `w_sheet` value of appropriated `WorksheetSet` dict
        '''
        if self.s_sheet is None:
            raise gs.exceptions.GSpreadException(
                'Spreadsheet is not connected.')

        # get the list of worksheets titles from the google spreadsheet
        google_sheet_titles = list(
            map(lambda sheet: sheet.title, self.s_sheet.worksheets()))

        for w_set in self.w_sets:
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

    def search_book(self, book: Book, book_field: BookFields, worksheet_title: str):
        '''
        Search for a book in the `stock` worksheet by the specified `book_field`
        and `value`.

        :param `book_field`: The field to search by.
        :param `value`: The value to search for.
        :return: A list of dictionaries containing the book details.
        '''
        pass
        # TODO: search algorithm
        """
        1. Get column of specific header
        2. Get indexes of each finded value
        3. Ask user to show all finded rows
        if yes:
        4. Get all full rows by them indexes
        """


if __name__ == '__main__':
    from library_system.config import SHEET_NAME, CREDS_PATH

    library = Library(SHEET_NAME, CREDS_PATH)
    library.connect()
    if not library.isConnected:
        print('Cannot connect to the Library Spreadsheet. Exiting...')
    else:
        print('Succesfully connected.')

    stock_worksheet = library.w_sets.stock.value['w_sheet']
    if stock_worksheet is not None:
        print(stock_worksheet)
        print(stock_worksheet.get_all_records())
