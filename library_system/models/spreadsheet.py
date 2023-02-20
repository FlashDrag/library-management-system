import gspread as gs
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError

from library_system.config import SCOPE, SHEET_NAME, CREDS_PATH


class Library:
    '''
    A class representing a Library as a spreadsheet, which contains books and
    methods for managing them.
    '''

    def __init__(self, sheet_name: str, creds_path: str) -> None:
        """
        Initialize a `Library` instance with the specified `sheet_name` and `creds_path`.

        :param `sheet_name`: Name of the Google Sheet.
        :param `creds_path`: Path to credentials file.
        """

        self._sheet_name = sheet_name
        self._creds_path = creds_path

        self._SHEET: gs.Spreadsheet | None = None
        self.stock: gs.Worksheet | None = None
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
            scope = Credentials.from_service_account_file(self._creds_path, scopes=SCOPE)
            client = gs.authorize(scope)
            self._SHEET = client.open(self._sheet_name)
            self.stock = self._set_worksheet('stock')
            self.isConnected = True
        except FileNotFoundError:
            print(f'Credentials file not found at {self._creds_path}.')
        except GoogleAuthError:
            print('GoogleAuthError: Check your credentials or try again later.')
        except gs.exceptions.SpreadsheetNotFound:
            print(f'Spreadsheet {self._sheet_name} not found!')
        except Exception as e:
            # catch-all Exception block is still included to handle any unexpected errors that may occur
            print(f"An unexpected error occurred: {e}")

    def _set_worksheet(self, worksheet_title: str, rows: int = 100, cols: int = 20) -> gs.Worksheet:
        '''
        Check if `worksheet_title` existed in Spreadsheet:
        - If not, create new Worksheet with `worksheet_title`.
        - If exist, returns a worksheet with specified title.

        :param worksheet_title:
        :param rows:
        :param cols:
        :return: worksheet

        '''
        assert isinstance(self._SHEET, gs.Spreadsheet)
        # assert self._SHEET is not None, 'Spreadsheet is not connected.'
        titles = list(map(lambda sheet: sheet.title, self._SHEET.worksheets()))
        if worksheet_title not in titles:
            worksheet = self._SHEET.add_worksheet(
                worksheet_title, rows=rows, cols=cols)
        else:
            worksheet = self._SHEET.worksheet(worksheet_title)

        return worksheet


if __name__ == '__main__':
    library = Library(SHEET_NAME, CREDS_PATH)
    isConnected = library.connect()
    if not isConnected:
        print('Cannot connect to the Library Spreadsheet. Exiting...')
    else:
        print('Succesfully connected.')
