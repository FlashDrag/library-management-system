import time
from rich import box
import logging

from library_system.tools import library_init, clear_terminal, F
from library_system.views.console_ui import Menu, get_book_input, display_book
from library_system.views.menus import MenuSets
from library_system.models.spreadsheet import Library
from library_system.models.book import Book, BookFields
from library_system.models.worksheets_cfg import WorksheetSets
from library_system.back_to_menu import back_to_menu

logger = logging.getLogger(__name__)


def display_header():
    clear_terminal()
    print(f'{F.YELLOW}ADDING BOOKS{F.ENDC}\n')


def run_field_selection_menu() -> BookFields:
    '''
    Display the menu `how to add a book` with the options.
    Get the selected option from the menu and split it to get the book field (e.g. `Search by ISBN` -> `isbn`).
    Get book field attribute from the BookFields enum.
    :return: BookFields attribute
    '''
    menu = Menu(**MenuSets.add_book.value)
    menu.run()
    selected = menu.get_selected_option_str().split()[2]
    book_field = getattr(BookFields, selected)
    return book_field


def show_found_books(book: Book, book_field: BookFields, found_books: list[dict]):
    '''
    Display search results in a menu:
    all books matching the BookFields attribute and value provided by the user.
    Prompt the user to select the book to add and run the func add_copies_to_book().

    param book: Book instance
    param book_field: selected BookFields attribute
    param found_books: list of books matching the BookFields attribute and value provided by the user
    '''
    clear_terminal()
    print(
        f'{F.YELLOW} all {len(found_books)} books matching the {book_field.value} '
        f'"{book[book_field.name]}"{F.ENDC}\n'
    )
    show_books_menu = Menu(
        'Select the book you want to add:',
        found_books,
        box.ASCII_DOUBLE_HEAD,
        expand=True,
        padding=(1, 1, 0, 1)
    )
    show_books_menu.run()
    # get the selected book to add in the form of a dictionary
    book_to_add = show_books_menu.get_selected_option_dict()

    return book_to_add


def add_copies_to_book(library: Library, book: Book, book_to_add: dict):
    '''
    Prompt the user to enter the number of copies to add.
    Call the library.add_book_copies() method to add copies to the book.

    param library: Library instance
    param book: Book instance
    param book_to_add: book to add to the library stock
    '''
    clear_terminal()
    title = 'You selected:'
    display_book(book_to_add, table_title=title)

    print(f'{F.HEADER}How many copies do you want to add?{F.ENDC}')
    copies = get_book_input(
        book, BookFields.copies, msg='Enter a number of copies in range 1-10:')
    try:
        # add the book to the library stock
        updated_book_dict = library.add_book_copies(
            book_to_add, WorksheetSets.stock.value, int(copies)
        )
    except Exception as e:
        print(f'{F.ERROR}Failed to add the book copies to the library stock.\nTry again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        logger.error(f'Failed to add the book to the library stock: {type(e)}: {e}')
        library = library_init()
        add_book(library)
    else:
        clear_terminal()
        print(
            f'{F.YELLOW}Successfully added {copies} copies of the book to the library stock.{F.ENDC}\n')
        logger.info(f'Added {copies} copies of the book: {book_to_add}')
        title = 'Updated book:'
        display_book(updated_book_dict, table_title=title)


def add_full_book(library: Library, book: Book, book_field: BookFields):
    '''
    Prompt the user to enter the remaining book fields.
    Add the book to the library stock using the library.append_book() method.

    param library: Library instance
    param book: Book instance
    param book_field: selected BookFields attribute
    '''

    # skip the book field that was used to search for the book and the book ISBN
    skip_fields = [BookFields.isbn, book_field]
    # get the remaining book fields
    fields = [field for field in BookFields if field not in skip_fields]

    # get the remaining book fields from the user
    for field in fields:
        get_book_input(book, field)

    try:
        added_book = library.append_book(book, WorksheetSets.stock.value)
    except Exception as e:
        print(f'{F.ERROR}Failed to add the book to the library stock.\nTry again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        logger.error(f'Failed to add the book to the library stock: {type(e)}: {e}')
        library = library_init()
        add_book(library)
    else:
        clear_terminal()
        print(f'{F.YELLOW}Successfully added the book to the library stock.{F.ENDC}\n')
        logger.info(f'Added the new book: {book}')
        title = 'Added book:'
        display_book(added_book, table_title=title)


def search_books(library: Library, book: Book, book_field: BookFields):
    '''
    Get the book field value from the user and
    search for the book in the library stock using the library.search_books() method.

    param library: Library instance
    param book: Book instance
    param book_field: selected BookFields attribute
    '''

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
        add_book(library)
        return None
    else:
        return found_books


# entry point for the add book functionality
def add_book(library: Library):
    logger.info('Starting the `add book` functionality.')
    book = Book()

    display_header()

    book_field = run_field_selection_menu()
    found_books = search_books(library, book, book_field)

    if found_books:
        clear_terminal()
        book_to_add = show_found_books(book, book_field, found_books)
        add_copies_to_book(library, book, book_to_add)
        back_to_menu(library)
    else:
        print(f'{F.ERROR}No books matching the {book_field.value}{F.ENDC}\n')
        time.sleep(3)
        clear_terminal()
        print(f'{F.YELLOW}CONTINUE ADDING A NEW BOOK{F.ENDC}\n')
        if book_field == BookFields.isbn:
            add_full_book(library, book, book_field)
            back_to_menu(library)
            return
        found_books = search_books(library, book, BookFields.isbn)
        if found_books:
            book_to_add = show_found_books(book, BookFields.isbn, found_books)
            add_copies_to_book(library, book, book_to_add)
            back_to_menu(library)
        else:
            add_full_book(library, book, book_field)
