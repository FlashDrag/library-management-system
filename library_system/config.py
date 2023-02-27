'''
This file contains all the configuration variables for the application.
'''
import os
import logging

from library_system.models.spreadsheet import Library
from library_system.models.worksheets_cfg import WorksheetSets
from library_system.views.formatters import font as F


logger = logging.getLogger(__name__)

LOGTAIL_TOKEN = os.getenv('LOGTAIL_TOKEN')
SHEET_NAME = 'library-management-system'
CREDS_PATH = 'creds.json'


def library_init() -> Library:
    '''
    Initialize a Library instance and connect to the Google Sheet.

    :return: Library instance
    '''
    print('Connecting to the Library Spreadsheet...')
    library = Library(SHEET_NAME, CREDS_PATH)
    library.connect()
    if not library.isConnected:
        print(f'{F.ERROR}Cannot connect to the Library Spreadsheet. Restart the App or try again later.{F.ENDC}\n'
              f'Exiting...')
        logger.error('Failed to connect to the Library Spreadsheet. Exiting...')
        exit()
    else:
        print(f'{F.BOLD}Succesfully connected.{F.ENDC}\n')
        logger.info('Connected to the Library Spreadsheet.')
        library.set_worksheets(list(WorksheetSets))
        return library
