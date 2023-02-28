import os
import sys
import psutil
import logging
import time

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
              f'Restarting...{F.ENDC}')
        logger.error('Failed to connect to the Library Spreadsheet. Restarting...')
        restart_app()
    else:
        print(f'{F.BOLD}Succesfully connected.{F.ENDC}\n')
        logger.info('Connected to the Library Spreadsheet.')
        library.set_worksheets(list(WorksheetSets))
    return library


# `restart_app` and `cleanup_app` functions based on
# code snippet from Stack Overflow answer by s3ni0r:
# https://stackoverflow.com/questions/11329917
def cleanup_app():
    """
    Closes all file descriptors and network connections
    that are associated with the current process.
    """
    time.sleep(2)
    try:
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)


def restart_app():
    """
    Restarts the current program.
    """
    cleanup_app()
    python = sys.executable
    os.execl(python, python, *sys.argv)
