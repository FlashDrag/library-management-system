import logging
from tabulate import tabulate

from library_system.tools import clear_terminal, F
from library_system.views.console_ui import TableFormats
from library_system.models.spreadsheet import Library


logger = logging.getLogger(__name__)


def display_overdue_borrowers(overdue_borrowers: list[dict]):
    '''
    Display the overdue borrowers in a table.

    param overdue_borrowers: list of overdue borrowers in the form of dictionaries
    '''
    clear_terminal()
    print(f'{F.YELLOW}Found {len(overdue_borrowers)} overdue borrowers{F.ENDC}\n')
    print(f'{F.YELLOW}Showing all overdue borrowers{F.ENDC}')
    max_col_widths = [13, 10, 8, 6, 4, 8, 5, 5, 4]
    overdue_borrowers_table = tabulate(
        overdue_borrowers,
        headers='keys',
        tablefmt=TableFormats.grid.value,
        maxcolwidths=max_col_widths,
        maxheadercolwidths=max_col_widths
    )
    print(overdue_borrowers_table)


# entry point for the checked_out viewer
def check_overdue_borrowers(library: Library):
    '''
    Shows borrwers that have not returned the book on time
    '''
    print('Searching for overdue borrowers in the Library "borrowed" sheet...')
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
            print(f'{F.YELLOW}No overdue borrowers found{F.ENDC}')
