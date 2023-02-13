import gspread
from google.oauth2.service_account import Credentials


class Library:
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, sheet_name, creds_path) -> None:
        """
        :param sheet_name (str): Name of the Google Sheet.
        :param creds_path (str): Path to credentials file.
        """
        self.sheet_name = sheet_name
        scope = Credentials.from_service_account_file(self.creds_path, scopes=self.SCOPE)
        client = gspread.authorize(scope)
        self.stock_sheet = client.open(self.sheet_name).worksheet('stock')
