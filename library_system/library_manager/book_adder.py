from tabulate import tabulate

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
    Display the menu with the options how to add a book.
    Get the selected option from the menu and split it to get the book field (e.g. `by isbn` -> `isbn`).
    Get book field attribute from the BookFields enum.
    :return: BookFields attribute
    '''
    menu = Menu(**MenuSets.add_book.value)
    menu.run()
    selected = menu.get_selected_option_str().split()[1]
    book_field = getattr(BookFields, selected)
    return book_field


def get_book_value(book: Book, book_field: BookFields) -> str:
    '''
    Get the user input based on the selected BookFields attribute and assign it to the Book model.

    :param selected_field: selected BookFields attribute
    :return: validated user input with the Book model
    '''
    book_value = get_book_input(book, book_field)

    return book_value


def find_book(library: Library, book_field: BookFields, book_value: str) -> list[dict]:
    '''
    Try to find the books matching the BookFields attribute and value provided by the user.

    :param library: Library instance
    :param book_field: selected BookFields attribute
    :param book_value: validated user input from the Book model
    :return: list of books matching the BookFields attribute and value provided by the user
    '''
    print(f"Searching for {book_value} in the Library...")
    found_books = library.search_books(
        book_value, book_field, WorksheetSets.stock.value
    )

    return found_books


def run_search_results_menu(library: Library, book: Book, book_field: BookFields, found_books: list[dict]):
    print(f'{F.YELLOW}Found {len(found_books)} '
          f'books matching the {book_field.value} '
          f'"{book[book_field.name]}"{F.ENDC}\n')
    search_results_menu = Menu(
        'What do you want to do?',
        ['Show all books to choose from', 'Continue adding the book'],
        Table_Formats.rounded_outline
    )
    search_results_menu.run()
    search_menu_selected = search_results_menu.get_selected_code()
    if search_menu_selected == 1:
        show_found_books(library, book, book_field, found_books)
    if search_menu_selected == 2:
        add_full_book()


def show_found_books(library: Library, book: Book, book_field: BookFields, found_books: list[dict]):
    clear_terminal()
    print(
        f'{F.YELLOW}Showing all books matching the {book_field.value} '
        f'"{book[book_field.name]}"{F.ENDC}\n'
    )
    show_books_menu = Menu(
        'Choose the book you want to add:',
        found_books,
        Table_Formats.rounded_outline
    )
    show_books_menu.run()
    book_to_add = show_books_menu.get_selected_option_dict()
    add_copies_to_book(library, book, book_to_add)


def add_copies_to_book(library: Library, book: Book, book_to_add: dict):
    clear_terminal()
    print(f'{F.YELLOW}You selected:{F.ENDC}\n')
    print(tabulate([book_to_add], headers='keys') + '\n')

    print('How many copies do you want to add?')
    copies = get_book_input(
        book, BookFields.copies, msg='Enter the number of copies in range 1-10:')
    try:
        # add the book to the library stock
        updated_book_dict = library.add_book_copies(
            book_to_add, int(copies))
    except Exception as e:
        print(e)
    else:
        clear_terminal()
        print(
            f'{F.YELLOW}Successfully added {copies} copies of the book to the library stock.{F.ENDC}')
        print(f'{F.YELLOW}Updated book:{F.ENDC}\n')
        print(tabulate([updated_book_dict], headers='keys'))


def add_full_book():
    pass


# entry point for the add book functionality
def add_book(library: Library):
    book = Book()

    display_header()

    book_field = run_add_book_menu()
    book_value = get_book_value(book, book_field)

    found_books = find_book(library, book_field, book_value)

    clear_terminal()
    if len(found_books) > 0:
        run_search_results_menu(library, book, book_field, found_books)
    else:
        add_full_book()

    # TODO: append book to the library stock
    """
    library.append_book(new_isbn, new_title, 'J.R.R. Tolkien', 'Fantasy', 'English', '2001', '1')
        library.stock.append_row(
            ['978-3-16-148410-0', 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', '2001', '1' 'True', '']
            )
    """
