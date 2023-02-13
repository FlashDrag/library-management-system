from gspread import authorize, Spreadsheet, Worksheet

from google.oauth2.service_account import Credentials


class Library:
    '''
    A class representing a Library as a spreadsheet, which contains books and methods for managing them.
    '''
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, sheet_name: str, creds_path: str) -> None:
        """
        Initialize a connection to the Google Sheet specified in the `sheet_name` parameter, using the credentials
        in the file at `creds_path`.
        - Create `_SHEET` private attribute with a `Spreadsheet` instance.
        - Create `stock_sheet` attr as a `Worksheet` instance of the 'stock' worksheet

        :param `sheet_name`: Name of the Google Sheet.
        :param `creds_path`: Path to credentials file.
        """
        scope = Credentials.from_service_account_file(
            creds_path, scopes=self.SCOPE)
        client = authorize(scope)
        self._SHEET: Spreadsheet = client.open(sheet_name)
        self.stock: Worksheet = self._set_worksheet('stock')

    def _set_worksheet(self, worksheet_title: str, rows: int = 100, cols: int = 20) -> Worksheet:
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


library = Library('library-management-system', 'creds.json')
print(library.stock)
