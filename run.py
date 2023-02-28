import logging
from pyfiglet import figlet_format

from library_system.config import LOGTAIL_TOKEN
from library_system.tools import clear_terminal, library_init
from library_system.models.spreadsheet import Library
from library_system.views.console_ui import Menu
from library_system.views.menus import MenuSets
from library_system import library_manager

from logtail import LogtailHandler

# log to Logtail service
logtail_handler = LogtailHandler(source_token=LOGTAIL_TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s -> %(funcName)s() -> %(lineno)s]: %(message)s",
    datefmt="%d-%b-%y %H:%M",
    handlers=[logtail_handler]
)
logger = logging.getLogger(__name__)


def display_header():
    logger.info('Starting the App...')
    print(figlet_format('Library Management System', 'straight'))


def run_main_menu():
    '''
    Displays the options available in the Library Main Menu
    using the tabulate library.
    :return: selected option name
    '''
    menu = Menu(**MenuSets.main_menu.value)
    menu.run()
    selected = menu.get_selected_option_str()

    return selected


def run_selected_option(library: Library, selected_option: str):
    '''
    Execute the function using the function name based on the user selection.
    :param library: Library instance
    :param selected_option: selected option name
    '''
    func_name = selected_option.replace(' ', '_')
    # TODO add testing for execution each function from library_manager based on the user selection from the Main Menu
    getattr(library_manager, func_name)(library)


def main():
    ''''
    Clear terminal screen, display text header;
    Initialize Library instance, connect to the Google Sheet;
    Display the Main Menu and process user selection.
    '''
    clear_terminal()
    display_header()

    library = library_init()
    selected_option = run_main_menu()
    run_selected_option(library, selected_option)


if __name__ == '__main__':
    main()
