import time
from rich import box

from library_system.tools import clear_terminal, library_init, F
from library_system.views.console_ui import Menu, get_book_input, display_book
from library_system.views.menus import MenuSets
from library_system.models.spreadsheet import Library
from library_system.models.book import Book, BookFields
from library_system.models.worksheets_cfg import WorksheetSets


def display_header():
    clear_terminal()
    print(f'{F.YELLOW}REMOVING BOOKS{F.ENDC}\n')


def run_remove_book_menu() -> BookFields:
    '''
    Display the menu `how to remove a book` with the options.
    Get the selected option from the menu and split it to get the book field (e.g. `Search by ISBN` -> `isbn`).
    Get book field attribute from the BookFields enum.
    :return: BookFields attribute
    '''
    menu = Menu(**MenuSets.remove_book.value)
    menu.run()
    selected = menu.get_selected_option_str().split()[2]
    book_field = getattr(BookFields, selected)
    return book_field


def show_found_books(book: Book, book_field: BookFields, found_books: list[dict]) -> dict:
    '''
    Display search results in a menu:
    all books matching the BookFields attribute and value provided by the user.
    Prompt the user to select the book to remove.

    param library: Library instance
    param book: Book instance
    param book_field: selected BookFields attribute
    param found_books: list of books matching the BookFields attribute and value provided by the user

    :return: dictionary of the selected book
    '''
    clear_terminal()
    print(
        f'{F.YELLOW}Showing all books matching the {book_field.value} '
        f'"{book[book_field.name]}"{F.ENDC}\n'
    )
    show_books_menu = Menu(
        'Select the book you want to remove:',
        found_books,
        box.ASCII_DOUBLE_HEAD,
        expand=True,
        padding=(1, 0)
    )
    show_books_menu.run()
    # get the selected book to remove in the form of a dictionary
    book_to_remove = show_books_menu.get_selected_option_dict()

    return book_to_remove


def prompt_remove_copies(library: Library, book: Book, book_to_remove: dict):
    '''
    Ask the user if they want to remove the full book or just some copies.
     - If the user wants to remove the full book, remove it from the stock worksheet,
         using the `remove_book` library method.
     - If the user wants to remove some copies, call the `remove_copies` function.

    :param library: Library instance
    :param book: Book instance
    :param book_to_remove: dictionary of the selected book
    '''
    clear_terminal()
    print(f'{F.YELLOW}You selected:{F.ENDC}')

    menu = Menu(
        'Do you want to remove the full book or just some copies?',
        ['Full book', 'Some copies'],
        box.MINIMAL_DOUBLE_HEAD
    )
    menu.run()
    selected = menu.get_selected_code()
    if selected == 1:
        try:
            library.remove_book(
                book_to_remove, WorksheetSets.stock.value, totally=True
            )
        except Exception:
            print(f'{F.ERROR}Failed to remove the book.\nTry again{F.ENDC}')
            print(f'{F.ERROR}Restarting...{F.ENDC}')
            # TODO: add logging
            # logger.error(f'Failed to remove the book: {e}')
            library = library_init()
            remove_book(library)
        else:
            print(f'{F.YELLOW}The Book has been completely removed{F.ENDC}\n')
    if selected == 2:
        remove_copies(library, book_to_remove)


def remove_copies(library: Library, book_to_remove: dict):
    '''
    Ask the user how many copies they want to remove.
    Remove the given number of book copies from the stock worksheet
    using the `remove_book` library method.

    :param library: Library instance
    :param book_to_remove: dictionary of the selected book
    '''
    print(f'{F.HEADER}How many copies do you want to remove?{F.ENDC}')

    while True:
        try:
            copies_to_remove = int(
                input(f'{F.ITALIC}Enter a number:\n{F.ENDC}'))
            if copies_to_remove < 1:
                raise ValueError
        except ValueError:
            print(f'{F.ERROR}Please enter a valid number{F.ENDC}')
        else:
            print('Removing....')
            try:
                removed_book = library.remove_book(
                    book_to_remove, WorksheetSets.stock.value, copies_to_remove
                )
            except Exception:
                print(f'{F.ERROR}Failed to remove the book.\nTry again{F.ENDC}')
                print(f'{F.ERROR}Restarting...{F.ENDC}')
                # TODO: add logging
                # logger.error(f'Failed to remove the book: {e}')
                library = library_init()
                remove_book(library)
            else:
                show_updated_book(removed_book, copies_to_remove)

            break


def show_updated_book(removed_book: dict | None, copies_to_remove: int):
    '''
    Display the updated book.
    If the book has been completely removed,
    display a message without the book details.

    :param removed_book: dictionary of the updated book
    :param copies_to_remove: number of copies to remove
    '''
    if not removed_book:
        print(f'{F.YELLOW}The Book has been completely removed{F.ENDC}\n')
    else:
        clear_terminal()
        print(f'{F.YELLOW}Successfully removed {copies_to_remove} copies{F.ENDC}\n')
        title = 'Updated book:'
        display_book(removed_book, table_title=title)


# entry point for the remove book functionality
def remove_book(library: Library):
    book = Book()

    display_header()

    book_field = run_remove_book_menu()
    book_value = get_book_input(book, book_field)

    print(f'Searching for "{book_value}" in the Library stock...')
    try:
        found_books = library.search_books(
            book_value, book_field, WorksheetSets.stock.value
        )
    except Exception:
        print(f'{F.ERROR}Failed to search for the book.\nTry again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        # TODO add logging
        # logger.error(f'Failed to search for the book: {e}')
        library = library_init()
        remove_book(library)
    else:
        if not len(found_books):
            print(f'{F.ERROR}No books matching the {book_field.value}\n'
                  f'Try again...{F.ENDC}')
            time.sleep(2)
            remove_book(library)
        else:
            book_to_remove = show_found_books(book, book_field, found_books)
            prompt_remove_copies(library, book, book_to_remove)
