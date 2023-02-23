import logging
from library_system.config import LOGTAIL_TOKEN, SHEET_NAME, CREDS_PATH, WORKSHEETS

from pyfiglet import figlet_format
from pydantic import ValidationError

from library_system.views.formatters import font as F, clear_terminal

from library_system.models.spreadsheet import Library
from library_system.views.console_ui import Menu, Table_Formats
from library_system import library_manager

from logtail import LogtailHandler

handler = LogtailHandler(source_token=LOGTAIL_TOKEN)

# set up logging with basicConfig
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s -> %(funcName)s() -> %(lineno)s]: %(message)s",
    datefmt="%d-%b-%y %H:%M",
    handlers=[handler]
)
logger = logging.getLogger(__name__)
logger.info('Starting the App...')


def display_header():
    print(figlet_format('Library Management System', 'straight'))


def library_init() -> Library:
    '''
    Initialize a Library instance and connect to the Google Sheet.

    :return: Library instance
    '''
    print('Connecting to the Library Spreadsheet...')
    library = Library(SHEET_NAME, WORKSHEETS, CREDS_PATH)
    library.connect()
    if not library.isConnected:
        print(f'{F.ERROR}Cannot connect to the Library Spreadsheet. Restart the App or try again later.{F.ENDC}\n'
              f'Exiting...')
        exit()
    else:
        print(f'{F.BOLD}Succesfully connected.{F.ENDC}\n')
        return library


def run_main_menu():
    '''
    Displays the options available in the Library Main Menu
    using the tabulate library.
    :return: list of lists with options
    '''
    menu_name = 'Library Main Menu'
    options = ['Add Book',
               'Remove Book',
               'Check Out Book',
               'Return Book',
               'View Library Stock']
    table_format = Table_Formats.outline

    try:
        menu = Menu(menu_name, options, table_format)
        menu.run()
        selected = menu.get_selected_option()
    except (ValidationError, ValueError) as e:
        logging.error(e)
        print(f'{F.ERROR}Something went wrong. Restart the App or try again later.{F.ENDC}\nExiting...')
        exit()
    else:
        return selected


def execute_function(library: Library, func_name: str):
    '''
    Execute the function using the function name based on the user selection.
    :param library: Library instance
    :param func_name: function name
    '''
    try:
        # try to execute the function from the library_manager module
        getattr(library_manager, func_name)(library)
    # catch exception if the function not found in library_manager using getattr()
    except AttributeError as e:
        logger.error(
            f'''Cannot get access to `{str(e).split("'")[-2]}` '''
            f'''at `{str(e).split("'")[1]}` {str(e).split("'")[0]}'''
        )
        print(f'{F.ERROR}Something went wrong. Restart the App or try again later.{F.ENDC}\nExiting...')
        exit()


def main():
    ''''
    Clear terminal screen, display text header;
    Initialize Library instance, connect to the Google Sheet;
    Display the Main Menu and process user selection.
    '''
    clear_terminal()
    display_header()

    library = library_init()
    selected = run_main_menu()
    execute_function(library, selected)


if __name__ == '__main__':
    main()
