from tabulate import tabulate
import time

from library_system.config import library_init
from library_system.views.formatters import font as F, clear_terminal
from library_system.views.console_ui import Menu, Table_Formats, get_book_input
from library_system.views.menus import MenuSets
from library_system.models.spreadsheet import Library
from library_system.models.book import Book, BookFields
from library_system.models.worksheets_cfg import WorksheetSets


def display_header():
    clear_terminal()
    print(f'{F.YELLOW}ADDING BOOKS{F.ENDC}\n')


def run_add_book_menu() -> BookFields:
    '''
    Display the menu `how to add a book` with the options.
    Get the selected option from the menu and split it to get the book field (e.g. `by isbn` -> `isbn`).
    Get book field attribute from the BookFields enum.
    :return: BookFields attribute
    '''
    menu = Menu(**MenuSets.add_book.value)
    menu.run()
    selected = menu.get_selected_option_str().split()[1]
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
        Table_Formats.rounded_outline
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
        Table_Formats.rounded_outline
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
    print(f'{F.YELLOW}You selected:{F.ENDC}\n')
    print(tabulate([book_to_add], headers='keys') + '\n')

    print(f'{F.HEADER}How many copies do you want to add?{F.ENDC}')
    copies = get_book_input(
        book, BookFields.copies, msg='Enter a number of copies in range 1-10:')
    try:
        # add the book to the library stock
        updated_book_dict = library.add_book_copies(
            book_to_add, WorksheetSets.stock.value, int(copies)
        )
    except Exception:
        print(f'{F.ERROR}Failed to add the book copies to the library stock. Try again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        # TODO add logging
        # logger.error(f'Failed to add the book to the library stock: {e}')
        library_init()
        time.sleep(2)
        add_book(library)
    else:
        clear_terminal()
        print(
            f'{F.YELLOW}Successfully added {copies} copies of the book to the library stock.{F.ENDC}')
        print(f'{F.YELLOW}Updated book:{F.ENDC}\n')
        print(tabulate([updated_book_dict], headers='keys'))


def add_full_book(library: Library, book: Book, book_field: BookFields):
    clear_terminal()
    print(f'{F.YELLOW}CONTINUE ADDING A NEW BOOK{F.ENDC}\n')
    fields = [field for field in BookFields if field != book_field]

    for field in fields:
        get_book_input(book, field)

    try:
        added_book = library.append_book(book, WorksheetSets.stock.value)
    except Exception:
        print(f'{F.ERROR}Failed to add the book to the library stock. Try again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        # TODO add logging
        # logger.error(f'Failed to add the book to the library stock: {e}')
        library_init()
        time.sleep(2)
        add_book(library)
    else:
        clear_terminal()
        print(f'{F.YELLOW}Successfully added the book to the library stock.{F.ENDC}')
        print(f'{F.YELLOW}Added book:{F.ENDC}\n')
        print(tabulate([added_book], headers='keys'))


# entry point for the add book functionality
def add_book(library: Library):
    book = Book()

    display_header()

    book_field = run_add_book_menu()
    book_value = get_book_input(book, book_field)

    print(f'Searching for "{book_value}" in the Library stock...')
    try:
        found_books = library.search_books(
            book_value, book_field, WorksheetSets.stock.value
        )
    except Exception:
        print(f'{F.ERROR}Failed to search for the book. Try again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        # TODO add logging
        # logger.error(f'Failed to search for the book: {e}')
        library_init()
        time.sleep(2)
        add_book(library)
    else:
        if len(found_books) > 0:
            clear_terminal()
            run_search_results_menu(library, book, book_field, found_books)
        else:
            print(f'{F.ERROR}No books matching the {book_field.value}{F.ENDC}\n')
            time.sleep(2)
            clear_terminal()
            add_full_book(library, book, book_field)
