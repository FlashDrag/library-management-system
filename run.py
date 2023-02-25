import logging
from library_system.config import LOGTAIL_TOKEN, SHEET_NAME, CREDS_PATH

from pyfiglet import figlet_format
from pydantic import ValidationError

from library_system.views.formatters import font as F, clear_terminal

from library_system.models.spreadsheet import Library
from library_system.models.worksheets_cfg import WorksheetSets
from library_system.views.console_ui import Menu
from library_system.views.menus import MenuSets
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
    library = Library(SHEET_NAME, CREDS_PATH)
    library.connect()
    if not library.isConnected:
        print(f'{F.ERROR}Cannot connect to the Library Spreadsheet. Restart the App or try again later.{F.ENDC}\n'
              f'Exiting...')
        exit()
    else:
        print(f'{F.BOLD}Succesfully connected.{F.ENDC}\n')
        library.set_worksheets(list(WorksheetSets))
        return library


def run_main_menu():
    '''
    Displays the options available in the Library Main Menu
    using the tabulate library.
    :return: list of lists with options
    '''
    try:
        menu = Menu(**MenuSets.main_menu.value)
        menu.run()
        selected = menu.get_selected_option()
    except (ValidationError, ValueError) as e:
        logging.error(e)
        print(f'{F.ERROR}Something went wrong. Restart the App or try again later.{F.ENDC}\nExiting...')
        exit()
    else:
        return selected


def execute_function(library: Library, selected_option: str):
    '''
    Execute the function using the function name based on the user selection.
    :param library: Library instance
    :param func_name: function name
    '''
    func_name = selected_option.replace(' ', '_')
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
