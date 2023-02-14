import gspread as gs
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError


class Library:
    '''
    A class representing a Library as a spreadsheet, which contains books and
    methods for managing them.
    '''
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, sheet_name: str, creds_path: str) -> None:
        """
        Initialize a `Library` instance with the specified `sheet_name` and `creds_path`.

        :param `sheet_name`: Name of the Google Sheet.
        :param `creds_path`: Path to credentials file.
        """

        self.sheet_name = sheet_name
        self.creds_path = creds_path

        self._SHEET: gs.Spreadsheet = None  # type: ignore
        self.stock: gs.Worksheet = None  # type: ignore
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
            scope = Credentials.from_service_account_file(self.creds_path, scopes=self.SCOPE)
            client = gs.authorize(scope)
            self._SHEET = client.open(self.sheet_name)
            self.stock = self._set_worksheet('stock')
            self.isConnected = True
        except FileNotFoundError:
            print(f'Credentials file not found at {self.creds_path}.')
        except GoogleAuthError:
            print('GoogleAuthError: Check your credentials or try again later.')
        except gs.exceptions.SpreadsheetNotFound:
            print(f'Spreadsheet {self.sheet_name} not found!')
        except Exception as e:
            # catch-all Exception block is still included to handle any unexpected errors that may occur
            print(f"An unexpected error occurred: {e}")
        finally:
            return self.isConnected

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
        titles = list(map(lambda sheet: sheet.title, self._SHEET.worksheets()))
        if worksheet_title not in titles:
            worksheet = self._SHEET.add_worksheet(
                worksheet_title, rows=rows, cols=cols)
        else:
            worksheet = self._SHEET.worksheet(worksheet_title)

        return worksheet
