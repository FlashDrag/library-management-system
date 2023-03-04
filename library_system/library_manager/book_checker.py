import logging
from datetime import date as dt
import time
from rich import box

from library_system.tools import library_init, clear_terminal, F
from library_system.views.console_ui import Menu, get_book_input, display_book
from library_system.views.menus import MenuSets
from library_system.models.spreadsheet import Library
from library_system.models.book import Book, BookFields, BorrowFields
from library_system.models.worksheets_cfg import WorksheetSets
from library_system.back_to_menu import back_to_menu

logger = logging.getLogger(__name__)


def display_header():
    clear_terminal()
    print(f'{F.YELLOW}BORROWING BOOKS{F.ENDC}\n')


def run_borrow_book_menu() -> BookFields:
    '''
    Display the menu `how to check out a book` with the options.
    Get the selected option from the menu and split it to get the book field (e.g. `Search by ISBN` -> `isbn`).
    Get book field attribute from the BorrowFields enum.
    :return: BorrowFields attribute
    '''
    menu = Menu(**MenuSets.check_out_book.value)
    menu.run()
    selected = menu.get_selected_option_str().split()[2]
    book_field = getattr(BookFields, selected)
    return book_field


def show_found_books(book: Book, book_field: BookFields, found_books: list[dict]):
    '''
    Display search results in a menu:
    all books matching the BorrowFields attribute and value provided by the user.
    Prompt the user to select the book to check out.

    param library: Library instance
    param book: Book instance
    param book_field: selected BorrowFields attribute
    param found_books: list of books matching the BorrowFields attribute and value provided by the user
    '''
    clear_terminal()
    print(
        f'{F.YELLOW}Showing {len(found_books)} books matching the {book_field.value} '
        f'"{book[book_field.name]}"{F.ENDC}\n'
    )
    show_books_menu = Menu(
        'Select the book you want to check out:',
        found_books,
        box.ASCII_DOUBLE_HEAD,
        expand=True,
        padding=(1, 1, 0, 1)
    )
    show_books_menu.run()
    # get the selected book to check out in the form of a dictionary
    book_to_check_out = show_books_menu.get_selected_option_dict()

    return book_to_check_out


def set_borowing_details(library: Library, book: Book, book_to_check_out: dict):
    clear_terminal()
    title = 'You selected:'
    display_book(book_to_check_out, table_title=title)

    for field in (BorrowFields.borrower_name, BorrowFields.due_date):
        value = get_book_input(book, field)
        book_to_check_out[field.name] = value

    # set today date as `Borrow date`
    today = dt.today()
    book_to_check_out[BorrowFields.borrow_date.name] = today.strftime('%d-%m-%Y')

    try:
        upd_book = library.check_out_book(book_to_check_out)
    except Exception as e:
        print(f'{F.ERROR}Failed to check out the book.\nTry again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        logger.error(f'Failed to check out the book: {type(e)}: {e}')
        library = library_init()
        check_out_book(library)
    else:
        borrower = book_to_check_out.get(BorrowFields.borrower_name.name)
        show_updated_book(upd_book, borrower)


def show_updated_book(updated_book: dict | None, borrower: str | None):
    if not updated_book:
        print(f'{F.YELLOW}The book has been borrowed by {borrower} and\n'
              f'completely checked out from the library stock.{F.ENDC}\n')
    else:
        clear_terminal()
        print(f'{F.YELLOW}A copy of the book has been borrowed by {borrower} and\n'
              f'checked out from the library stock.{F.ENDC}\n')
        logger.info(f'Book: {updated_book} has been borrowed by {borrower}')
        title = 'Current stock:'
        display_book(updated_book, table_title=title)


# entry point for the check out book functionality
def check_out_book(library: Library):
    logger.info('Starting the check out book functionality')
    book = Book()

    display_header()

    book_field = run_borrow_book_menu()
    book_value = get_book_input(book, book_field)

    print(f'Searching for "{book_value}" in the Library stock...')
    try:
        found_books = library.search_books(
            book_value, book_field, WorksheetSets.stock.value
        )
    except Exception as e:
        print(f'{F.ERROR}Failed to search for the book.\nTry again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        logger.error(f'Failed to search for the book: {type(e)}: {e}')
        library = library_init()
        check_out_book(library)
    else:
        if not len(found_books):
            print(f'{F.ERROR}No books matching the {book_field.value}\n'
                  f'Try again...{F.ENDC}')
            time.sleep(3)
            check_out_book(library)
        else:
            book_to_check_out = show_found_books(book, book_field, found_books)
            set_borowing_details(library, book, book_to_check_out)
            back_to_menu(library)
