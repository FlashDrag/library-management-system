import logging
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
    print(f'{F.YELLOW}RETURNING BOOKS{F.ENDC}\n')


def run_return_book_menu() -> BorrowFields:
    '''
    Display the menu `how to return a book` with the options.
    Get the selected option from the menu and split it to get the book field (e.g. `by isbn` -> `isbn`).
    Get book field attribute from the BorrowFields enum.
    :return: BorrowFields attribute
    '''
    menu = Menu(**MenuSets.return_book.value)
    menu.run()
    selected = menu.get_selected_option_str().split()[2]
    borrow_field = getattr(BorrowFields, selected)
    return borrow_field


def show_found_books(book: Book, book_field: BookFields | BorrowFields, found_books: list[dict]):
    '''
    Display search results in a menu:
    all books matching the BorrowFields attribute and value provided by the user.
    Prompt the user to select the book to return.

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
        'Select the book you want to return:',
        found_books,
        box.ASCII_DOUBLE_HEAD,
        expand=True
    )
    show_books_menu.run()
    # get the selected book to return in the form of a dictionary
    book_to_return = show_books_menu.get_selected_option_dict()

    return book_to_return


def return_book_to_stock(library: Library, book_to_return: dict):
    '''
    Return the book to the library stock using the Library instance method `return_book`.
    Display the updated book details in the library stock using the `show_updated_book` function.

    :param library: Library instance
    :param book_to_return: dictionary with the book details
    '''
    clear_terminal()
    title = 'You selected:'
    display_book(book_to_return, WorksheetSets.borrowed, table_title=title)
    print('Returning the book to the Library stock...\n')
    try:
        upd_book = library.return_book(book_to_return)
    except Exception as e:
        logger.error(f'Failed to return the book: {type(e).__name__}: {e}')
        print(f'{F.ERROR}Failed to return the book.\n Try again\n'
              f'Restarting...{F.ENDC}')
        library = library_init()
        return_book(library)
    else:
        show_updated_book(upd_book)


def show_updated_book(updated_book: dict):
    '''
    Display the updated book details in the library stock.

    :param updated_book: dictionary with the updated book details
    '''
    print(f'{F.YELLOW}The book was returned to the library stock.{F.ENDC}\n')
    title = 'The current book details in the library stock:'
    display_book(updated_book, table_title=title)


# entry point for the return book functionality
def return_book(library: Library):
    book = Book(search_mode=True)

    display_header()

    borrow_field = run_return_book_menu()
    book_value = get_book_input(book, borrow_field)

    print(
        f'Searching for "{book_value}" in the Library `borrowed` worksheet...')
    try:
        found_books = library.search_books(
            book_value, borrow_field, WorksheetSets.borrowed.value
        )
    except Exception as e:
        print(f'{F.ERROR}Failed to search for the book.\nTry again\n'
              f'Restarting...{F.ENDC}')
        logger.error(f'Failed to search for the book: {e}')
        library = library_init()
        return_book(library)
    else:
        if not len(found_books):
            print(f'{F.ERROR}No books matching the {borrow_field.value}\n'
                  f'Try again...{F.ENDC}')
            time.sleep(3)
            return_book(library)
        else:
            book_to_return = show_found_books(book, borrow_field, found_books)
            return_book_to_stock(library, book_to_return)
            back_to_menu(library)
