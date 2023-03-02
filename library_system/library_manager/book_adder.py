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


def run_add_book_menu() -> BookFields:
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


def run_search_results_menu(library: Library, book: Book, book_field: BookFields, found_books: list[dict]):
    '''
    Display the menu what to do with the search results.
    Get the selected option from the menu and run the appropriate function:
    - show_found_books(): display the search results
    - add_full_book(): - continue adding the book without displaying the search results

    param library: Library instance
    param book: Book instance
    param book_field: selected BookFields attribute
    param found_books: list of books matching the BookFields attribute and value provided by the user
    '''
    print(f'{F.YELLOW}Found {len(found_books)} '
          f'books matching the {book_field.value} '
          f'"{book[book_field.name]}"{F.ENDC}\n')
    search_results_menu = Menu(
        'What do you want to do?',
        ['Show all the books to select and add new copies.', 'Continue adding the book, fill all fields.'],
        box.MINIMAL_DOUBLE_HEAD
    )
    search_results_menu.run()
    search_menu_selected = search_results_menu.get_selected_code()
    if search_menu_selected == 1:
        show_found_books(library, book, book_field, found_books)
    if search_menu_selected == 2:
        add_full_book(library, book, book_field)


def show_found_books(library: Library, book: Book, book_field: BookFields, found_books: list[dict]):
    '''
    Display search results in a menu:
    all books matching the BookFields attribute and value provided by the user.
    Prompt the user to select the book to add and run the func add_copies_to_book().

    param library: Library instance
    param book: Book instance
    param book_field: selected BookFields attribute
    param found_books: list of books matching the BookFields attribute and value provided by the user
    '''
    clear_terminal()
    print(
        f'{F.YELLOW}Showing all books matching the {book_field.value} '
        f'"{book[book_field.name]}"{F.ENDC}\n'
    )
    show_books_menu = Menu(
        'Select the book you want to add:',
        found_books,
        box.ASCII_DOUBLE_HEAD,
        expand=True
    )
    show_books_menu.run()
    # get the selected book to add in the form of a dictionary
    book_to_add = show_books_menu.get_selected_option_dict()
    add_copies_to_book(library, book, book_to_add)


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
    clear_terminal()
    print(f'{F.YELLOW}CONTINUE ADDING A NEW BOOK{F.ENDC}\n')
    # get the remaining book fields
    fields = [field for field in BookFields if field != book_field]

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


# entry point for the add book functionality
def add_book(library: Library):
    logger.info('Starting the `add book` functionality.')
    book = Book()

    display_header()

    book_field = run_add_book_menu()
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
    else:
        if len(found_books) > 0:
            clear_terminal()
            run_search_results_menu(library, book, book_field, found_books)
            back_to_menu(library)
        else:
            print(f'{F.ERROR}No books matching the {book_field.value}{F.ENDC}\n')
            time.sleep(3)
            clear_terminal()
            add_full_book(library, book, book_field)
