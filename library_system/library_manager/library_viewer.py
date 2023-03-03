import time
from rich import box
import logging

from library_system.tools import clear_terminal, F, library_init
from library_system.views.console_ui import Menu
from library_system.views.menus import MenuSets
from library_system.models.spreadsheet import Library
from library_system.models.book import BookFields, BorrowFields
from library_system.models.worksheets_cfg import WorksheetSets, WorksheetSet
from library_system.back_to_menu import back_to_menu


logger = logging.getLogger(__name__)


def display_header(stock_name: str | None = None):
    clear_terminal()
    if not stock_name:
        print(f'{F.YELLOW}VIEWING Library{F.ENDC}\n')
    else:
        print(f'{F.YELLOW}VIEWING {stock_name.upper()} STOCK{F.ENDC}\n')


def run_stock_selection_menu() -> WorksheetSet:
    '''
    Display the menu with the options to select the worksheet set to view.
    return: WorksheetSet instance
    '''
    menu = Menu(
        'Select the stock to view:',
        ['Library stock', 'Borrowed books'],
        box.MINIMAL_DOUBLE_HEAD
    )
    menu.run()
    selected = menu.get_selected_code()
    if selected == 1:
        worksheet_set = WorksheetSets.stock.value
    else:
        worksheet_set = WorksheetSets.borrowed.value
    return worksheet_set


def run_field_selection_menu(worksheet_set: WorksheetSet) -> BookFields | BorrowFields | None:
    '''
    Display the menu with the options to select the field to sort the library stock by.
    Options depend on the worksheet set selected in the run_stock_selection_menu().
    Get the field attribute from the BookFields or BorrowFields enum.

    param worksheet_set: WorksheetSet instance
    return: BookFields or BorrowFields attribute or None (if `Spreadsheet order` option is selected)
    '''

    if worksheet_set == WorksheetSets.stock.value:
        display_header('Library')
        menu = Menu(**MenuSets.view_library_stock.value)
    elif worksheet_set == WorksheetSets.borrowed.value:
        display_header('Borrowed')
        menu = Menu(**MenuSets.view_borrowed_stock.value)
    else:
        raise ValueError(
            f'Invalid worksheet set: {worksheet_set}. Expected WorksheetSet instance')

    menu.run()

    # code 1 is the `Spreadsheet order` option
    if menu.get_selected_code() == 1:
        return None
    selected = menu.get_selected_option_str().split()[2]
    selected_field = getattr(BookFields, selected) if worksheet_set == WorksheetSets.stock.value \
        else getattr(BorrowFields, selected)
    return selected_field


def get_sort_order(worksheet_set: WorksheetSet) -> bool:
    '''
    Display the menu with the options to select the sort order.
    return: False if ascending, True if descending
    '''
    if worksheet_set == WorksheetSets.stock.value:
        display_header('Library')
        menu = Menu(**MenuSets.view_library_stock.value)
    elif worksheet_set == WorksheetSets.borrowed.value:
        display_header('Borrowed')

    menu = Menu(
        'Select the sort order:',
        ['Ascending', 'Descending'],
        box.MINIMAL_DOUBLE_HEAD
    )
    menu.run()
    selected = menu.get_selected_code()
    if selected == 1:
        return False
    else:
        return True


def display_stock(
        worksheet_set: WorksheetSet,
        stock: list[dict],
        selected_field: BookFields | BorrowFields | None,
        sort_order: bool):
    '''
    Display the library stock in a table format using Menu.print_table() static method.
    param stock: list of dicts with the book data
    param selected_field: BookFields or BorrowFields attribute or None (if `Spreadsheet order` option is selected)
    param sort_order: False if ascending, True if descending
    '''
    stock_name = 'Library' if worksheet_set == WorksheetSets.stock.value else 'Borrowed'
    sort_order_name = 'ascending' if not sort_order else 'descending'
    display_header(stock_name)
    print(f'{F.YELLOW}Found {len(stock)} rows in the {stock_name} stock{F.ENDC}\n')

    if selected_field:
        print(f'{F.YELLOW}Books sorted by {selected_field.value} in {sort_order_name} order{F.ENDC}')
    else:
        print(f'{F.YELLOW}Books sorted in the order they appear in the Spreadsheet "{worksheet_set["title"]}"{F.ENDC}')

    Menu.print_table(stock, box.ASCII_DOUBLE_HEAD, expand=True, padding=(1, 1, 0, 1))


# entry point for the view library stock functionality
def view_library_stocks(library: Library):
    logger.info('Viewing the library stocks')
    display_header()

    worksheet_set = run_stock_selection_menu()
    selected_field = run_field_selection_menu(worksheet_set)
    if selected_field:
        # if `Spreadsheet order` option is selected, skip the sort order selection
        sort_order = get_sort_order(worksheet_set)
    else:
        sort_order = False

    print(f'{F.YELLOW}Getting the stock...{F.ENDC}\n'
          f'Depending on the size of the library, this may take a while.\n'
          f'Please wait...')

    try:
        library_stock = library.get_library_stock(
            worksheet_set, selected_field, sort_order
        )
    except Exception as e:
        print(
            f'{F.ERROR}Failed to get the library stock.\nTry again{F.ENDC}'
        )
        logger.error(f'Failed to get the library stock: {type(e)}: {e}')
        library = library_init()
        view_library_stocks(library)
    else:
        time.sleep(2)
        if library_stock:
            display_stock(worksheet_set, library_stock,
                          selected_field, sort_order)
            back_to_menu(library)
        else:
            clear_terminal()
            print(f'{F.YELLOW}No books found in the library stock{F.ENDC}\n')
            back_to_menu(library)
