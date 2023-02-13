import gspread
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
        :param sheet_name: Name of the Google Sheet.
        :param creds_path: Path to credentials file.
        """
        scope = Credentials.from_service_account_file(creds_path, scopes=self.SCOPE)
        client = gspread.authorize(scope)
        self._SHEET = client.open(sheet_name)
