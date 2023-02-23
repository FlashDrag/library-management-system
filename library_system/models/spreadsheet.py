import logging

import gspread as gs
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError

from library_system.config import SCOPE, SHEET_NAME, CREDS_PATH, WORKSHEETS

from library_system.models.book import Book, BookFields

logger = logging.getLogger(__name__)


class Library:
    '''
    Library class that connects to a Google Sheet and provides methods to interact with it.

    :param `sheet_name`: Name of the Google Sheet.
    :param `worksheets`: dict contains worksheet sets:
        worksheet title: {list of headers, `Worksheet` instances}
    :param `creds_path`: Path to credentials file.
    :param `_SHEET`: `Spreadsheet` instance.
    :param `isConnected`: indicates if the Library is connected to the Google Sheet.
    '''

    def __init__(self, sheet_name: str, worksheets: dict[str, dict], creds_path: str) -> None:
        self._sheet_name = sheet_name
        self.worksheets = worksheets
        self._creds_path = creds_path

        self._SHEET: gs.Spreadsheet | None = None
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
                self._creds_path, scopes=SCOPE)
            client = gs.authorize(scope)
            self._SHEET = client.open(self._sheet_name)
            self._set_worksheets()
            self.isConnected = True
        except FileNotFoundError:
            logger.error(f'Credentials file not found at {self._creds_path}.')
        except GoogleAuthError:
            logger.error(
                'GoogleAuthError: Check your credentials or try again later.')
        except gs.exceptions.SpreadsheetNotFound:
            logger.error(f'Spreadsheet {self._sheet_name} not found!')
        except Exception as e:
            # catch-all Exception block is still included to handle any unexpected errors that may occur
            logger.error(f"An unexpected error occurred: {e}")

    def _set_worksheets(self):
        '''
        Sets the worksheets for the Library instance.
        Add new worksheets to the Google Spreadsheet if they don't exist based on parameters from `worksheet` dicts:
        - dict key: title of the worksheet
        - values:
            * `headers`: list of headers for the worksheet
            * `wsheet_obj`: None | Worksheet instance
        Creates 'Worksheet' instances for each Google Worksheet and adds them to the `worksheets` list:
        -
        '''
        if self._SHEET is None:
            raise Exception('Spreadsheet is not connected.')

        # get the list of worksheets titles from the google spreadsheet
        google_sheet_titles = list(
            map(lambda sheet: sheet.title, self._SHEET.worksheets()))

        for worksheet_title in self.worksheets:
            headers = self.worksheets[worksheet_title]['headers']
            if worksheet_title not in google_sheet_titles:
                worksheet = self._SHEET.add_worksheet(
                    worksheet_title, rows=100, cols=len(headers))
            else:
                worksheet = self._SHEET.worksheet(worksheet_title)

            # add code that updates headers
            # update the first row with the headers
            worksheet.update('A1', [headers])
            self.worksheets[worksheet_title]['wsheet_obj'] = worksheet

    def search_book(self, book: Book, book_field: BookFields, worksheet_title: str) -> list[dict]:
        '''
        Search for a book in the `stock` worksheet by the specified `book_field`
        and `value`.

        :param `book_field`: The field to search by.
        :param `value`: The value to search for.
        :return: A list of dictionaries containing the book details.
        '''
        worksheet = self.worksheets[worksheet_title]['wsheet_obj']
        if worksheet is None:
            raise gs.exceptions.WorksheetNotFound(
                'Worksheet "stock" not found.'
            )
    # TODO: search algorithm
    """
    1. Get column of specific header
    2. Get indexes of each finded value
    3. Ask user to show all finded rows
    if yes:
    4. Get all full rows by them indexes
    """

if __name__ == '__main__':
    library = Library(SHEET_NAME, WORKSHEETS, CREDS_PATH)
    library.connect()
    if not library.isConnected:
        print('Cannot connect to the Library Spreadsheet. Exiting...')
    else:
        print('Succesfully connected.')
    for worksheet in library.worksheets:
        print(worksheet)
        wsheet_obj: gs.Worksheet = library.worksheets[worksheet]['wsheet_obj']
        print(wsheet_obj.get_values())
        print()
