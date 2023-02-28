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
    print(f'{F.YELLOW}REMOVING BOOKS{F.ENDC}\n')


def run_remove_book_menu() -> BookFields:
    '''
    Display the menu `how to remove a book` with the options.
    Get the selected option from the menu and split it to get the book field (e.g. `by isbn` -> `isbn`).
    Get book field attribute from the BookFields enum.
    :return: BookFields attribute
    '''
    menu = Menu(**MenuSets.remove_book.value)
    menu.run()
    selected = menu.get_selected_option_str().split()[1]
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
        Table_Formats.rounded_outline
    )
    show_books_menu.run()
    # get the selected book to remove in the form of a dictionary
    book_to_remove = show_books_menu.get_selected_option_dict()

    return book_to_remove


def prompt_remove_copies(library: Library, book: Book, book_to_remove: dict):
    clear_terminal()
    print(f'{F.YELLOW}You selected:{F.ENDC}\n')
    print(tabulate([book_to_remove], headers='keys') + '\n')

    menu = Menu(
        'Do you want to remove the full book or just some copies?',
        ['Full book', 'Some copies'],
        Table_Formats.rounded_outline
    )
    menu.run()
    selected = menu.get_selected_code()
    if selected == 1:
        try:
            library.remove_book(
                book_to_remove, WorksheetSets.stock.value, totally=True
            )
        except Exception:
            print(f'{F.ERROR}Failed to remove the book. Try again{F.ENDC}')
            print(f'{F.ERROR}Restarting...{F.ENDC}')
            # TODO: add logging
            # logger.error(f'Failed to remove the book: {e}')
            library_init()
            time.sleep(2)
            remove_book(library)
        else:
            print(f'{F.YELLOW}The Book has been completely removed{F.ENDC}\n')
    if selected == 2:
        remove_copies(library, book, book_to_remove)


def remove_copies(library: Library, book: Book, book_to_remove: dict):
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
                print(f'{F.ERROR}Failed to remove the book. Try again{F.ENDC}')
                print(f'{F.ERROR}Restarting...{F.ENDC}')
                # TODO: add logging
                # logger.error(f'Failed to remove the book: {e}')
                library_init()
                time.sleep(2)
                remove_book(library)
            else:
                show_updated_book(removed_book, copies_to_remove)

            break


def show_updated_book(removed_book: dict | None, copies_to_remove: int):
    if not removed_book:
        print(f'{F.YELLOW}The Book has been completely removed{F.ENDC}\n')
    else:
        clear_terminal()
        print(f'{F.YELLOW}Successfully removed {copies_to_remove} copies{F.ENDC}\n')
        print(f'{F.YELLOW}Updated book:{F.ENDC}\n')
        print(tabulate([removed_book], headers='keys'))


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
        print(f'{F.ERROR}Failed to search for the book. Try again{F.ENDC}')
        print(f'{F.ERROR}Restarting...{F.ENDC}')
        # TODO add logging
        # logger.error(f'Failed to search for the book: {e}')
        library_init()
        time.sleep(2)
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
