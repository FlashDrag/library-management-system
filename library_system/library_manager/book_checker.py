import logging
from datetime import date as dt
import time

from library_system.tools import library_init, cleanup_app, clear_terminal, F
from library_system.views.console_ui import Menu, Table_Formats, get_book_input, display_book
from library_system.views.menus import MenuSets
from library_system.models.spreadsheet import Library
from library_system.models.book import Book, BookFields, BorrowFields
from library_system.models.worksheets_cfg import WorksheetSets

logger = logging.getLogger(__name__)


def display_header():
    clear_terminal()
    print(f'{F.YELLOW}BORROWING BOOKS{F.ENDC}\n')


def run_borrow_book_menu() -> BookFields:
    '''
    Display the menu `how to check out a book` with the options.
    Get the selected option from the menu and split it to get the book field (e.g. `by isbn` -> `isbn`).
    Get book field attribute from the BorrowFields enum.
    :return: BorrowFields attribute
    '''
    menu = Menu(**MenuSets.check_out_book.value)
    menu.run()
    selected = menu.get_selected_option_str().split()[1]
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
        f'{F.YELLOW}Showing all books matching the {book_field.value} '
        f'"{book[book_field.name]}"{F.ENDC}\n'
    )
    show_books_menu = Menu(
        'Select the book you want to check out:',
        found_books,
        Table_Formats.rounded_outline
    )
    show_books_menu.run()
    # get the selected book to check out in the form of a dictionary
    book_to_check_out = show_books_menu.get_selected_option_dict()

    return book_to_check_out


def set_borowing_details(library: Library, book: Book, book_to_check_out: dict):
    clear_terminal()
    print(f'{F.YELLOW}You selected:{F.ENDC}\n')
    display_book(book_to_check_out)

    for field in (BorrowFields.borrower, BorrowFields.due_date):
        value = get_book_input(book, field)
        book_to_check_out[field.name] = value

    # set today date as `Borrow date`
    today = dt.today()
    book_to_check_out[BorrowFields.borrow_date.name] = today.strftime('%d-%m-%Y')

    try:
        upd_book = library.check_out_book(book_to_check_out, book)
    except Exception as e:
        print(f'{F.ERROR}Failed to check out the book. Try again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        logger.error(f'Failed to check out the book: {e}')
        cleanup_app()
        library_init()
        check_out_book(library)
    else:
        show_updated_book(upd_book)


def show_updated_book(updated_book: dict | None):
    if not updated_book:
        print(f'{F.YELLOW}The book was completely checked out from the library stock.{F.ENDC}\n')
    else:
        clear_terminal()
        print(f'{F.YELLOW}The book has been checked out.{F.ENDC}\n')
        print(f'{F.YELLOW}Current stock:{F.ENDC}\n')
        display_book(updated_book)


# entry point for the add book functionality
def check_out_book(library: Library):
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
        print(f'{F.ERROR}Failed to search for the book. Try again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        logger.error(f'Failed to search for the book: {e}')
        cleanup_app()
        library_init()
        check_out_book(library)
    else:
        if not len(found_books):
            print(f'{F.ERROR}No books matching the {book_field.value}\n'
                  f'Try again...{F.ENDC}')
            time.sleep(2)
            check_out_book(library)
        else:
            book_to_check_out = show_found_books(book, book_field, found_books)
            set_borowing_details(library, book, book_to_check_out)
