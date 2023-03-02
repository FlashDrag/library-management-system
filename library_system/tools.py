import os
import sys
import logging

from library_system.config import SHEET_NAME, CREDS_PATH
from library_system.models.spreadsheet import Library
from library_system.models.worksheets_cfg import WorksheetSets


logger = logging.getLogger(__name__)


class F:
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    HEADER = '\033[92m'
    ERROR = '\033[91m'
    YELLOW = '\033[93m'
    UNDERLINE = '\033[4m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GREY = '\033[90m'
    ENDC = '\033[0m'


def clear_terminal():
    '''Clear terminal screen'''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")


def library_init() -> Library:
    '''
    Initialize a Library instance and connect to the Google Sheet.

    :return: Library instance
    '''
    print('Connecting to the Library Spreadsheet...')
    library = Library(SHEET_NAME, CREDS_PATH)
    library.connect()
    if not library.isConnected:
        print(f'{F.ERROR}Cannot connect to the Library Spreadsheet. Restart the App or try again later.\n'
              f'Exiting...{F.ENDC}')
        logger.error('Failed to connect to the Library Spreadsheet.')
        quit()
    else:
        print(f'{F.BOLD}Succesfully connected.{F.ENDC}\n')
        logger.info('Connected to the Library Spreadsheet.')
        library.set_worksheets(list(WorksheetSets))
    return library


def restart_app():
    """
    Restarts the current program.
    """
    python = sys.executable
    logger.info('Restarting the app...')
    os.execv(python, [python] + sys.argv)
