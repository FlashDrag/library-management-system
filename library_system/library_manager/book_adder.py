from tabulate import tabulate
from pydantic import ValidationError

from library_system.views.formatters import font as F, clear_terminal
from library_system.views.console_ui import Menu, Table_Formats, get_book_input
from library_system.views.menus import MenuSets
from library_system.models.spreadsheet import Library
from library_system.models.book import Book, BookFields
from library_system.models.worksheets_cfg import WorksheetSets


def add_book(library: Library):
    clear_terminal()
    print(f'{F.YELLOW}ADDING BOOKS{F.ENDC}\n')

    book = Book()

    add_book_menu = Menu(**MenuSets.add_book.value)
    add_book_menu.run()
    # get the selected option from the menu and split it to get the book field (e.g. `by isbn` -> `isbn`)
    book_menu_selected = add_book_menu.get_selected_option_str().split()[1]

    # get the BookFields attribute based on the user selection
    book_field = getattr(BookFields, book_menu_selected)
    # get the user input based on the selected BookFields attribute and assign it to the new book
    book_value = get_book_input(book, book_field)

    # try to find the books matching the BookFields attribute and value provided by the user
    print(f"Searching for {book_value} in the Library...")
    finded_books = library.search_books(
        book_value, book_field, WorksheetSets.stock.value
    )
    clear_terminal()
    if len(finded_books) > 0:
        print(f'{F.YELLOW}Finded {len(finded_books)} '
              f'books matching the {book_field.value} '
              f'"{book[book_field.name]}"{F.ENDC}\n'
              )
        search_results_menu = Menu(
            'What do you want to do?',
            ['Show all books to choose from', 'Continue adding the book'],
            Table_Formats.rounded_outline
        )
        search_results_menu.run()
        search_menu_selected = search_results_menu.get_selected_code()
        if search_menu_selected == 1:
            clear_terminal()
            print(
                f'{F.YELLOW}Showing all books matching the {book_field.value} '
                f'"{book[book_field.name]}"{F.ENDC}\n'
            )
            show_books_menu = Menu(
                'Choose the book you want to add:',
                finded_books,
                Table_Formats.rounded_outline
            )
            show_books_menu.run()
            book_to_add = show_books_menu.get_selected_option_dict()
            clear_terminal()
            print(f'{F.YELLOW}You selected:{F.ENDC}\n')
            print(tabulate([book_to_add], headers='keys') + '\n')

            print('How many copies do you want to add?')
            while True:
                try:
                    user_input = input(f'{F.ITALIC}Enter the number of copies in range 1-10:{F.ENDC}\n')
                    # validate user input using Book instance
                    setattr(book, BookFields.copies.name, user_input)
                except ValidationError as e:
                    print(f"{F.ERROR}{e.errors()[0]['msg']}Try again.{F.ENDC}\n")
                else:
                    copies = int(user_input)
                    break

            try:
                # add the book to the library stock
                updated_book_dict = library.add_book_copies(book_to_add, copies)
            except Exception as e:
                print(e)
            else:
                clear_terminal()
                print(f'{F.YELLOW}Successfully added {copies} copies of the book to the library stock.{F.ENDC}')
                print(f'{F.YELLOW}Updated book:{F.ENDC}\n')
                print(tabulate([updated_book_dict], headers='keys'))

    # TODO: append book to the library stock
    """
    library.append_book(new_isbn, new_title, 'J.R.R. Tolkien', 'Fantasy', 'English', '2001', '1')
        library.stock.append_row(
            ['978-3-16-148410-0', 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', '2001', '1' 'True', '']
            )
    """
