import logging
import time

from rich import box

from library_system.views.console_ui import Menu
from library_system.tools import clear_terminal, F
from library_system.models.spreadsheet import Library
from library_system.back_to_menu import back_to_menu


logger = logging.getLogger(__name__)


def display_overdue_borrowers(overdue_borrowers: list[dict]):
    '''
    Display the overdue borrowers in a table.

    param overdue_borrowers: list of overdue borrowers in the form of dictionaries
    '''
    clear_terminal()
    print(f'{F.YELLOW}Found {len(overdue_borrowers)} overdue borrowers{F.ENDC}\n')
    title = 'Showing all overdue borrowers'

    Menu.print_table(
        overdue_borrowers,
        box.ASCII_DOUBLE_HEAD,
        title,
        padding=(1, 0),
        expand=True
    )


# entry point for the checked_out viewer
def check_overdue_borrowers(library: Library):
    '''
    Shows borrwers that have not returned the book on time
    '''
    print('Searching for overdue borrowers in the Library "borrowed" sheet...')
    time.sleep(2)
    try:
        overdue_borrowers = library.get_overdue_borrowers()
    except Exception as e:
        print(f'{F.ERROR}Failed to get the overdue borrowers.\nRestart the app and try again{F.ENDC}')
        logger.error(f'Failed to get the overdue borrowers: {type(e)}: {e}')
        quit()
    else:
        if overdue_borrowers:
            display_overdue_borrowers(overdue_borrowers)
        else:
            clear_terminal()
            print(f'{F.YELLOW}No overdue borrowers found{F.ENDC}\n')
            back_to_menu(library)
