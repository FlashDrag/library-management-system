from library_system.views.formatters import font as F, clear_terminal
from library_system.views.console_ui import Menu, Table_Formats, get_book_input
from library_system.models.spreadsheet import Library
from library_system.models.book import Book, BookFields


def add_book(library: Library):
    clear_terminal()
    print(f'{F.HEADER}ADDING BOOKS{F.ENDC}\n')

    menu = Menu(
        'How to add a book to the library stock?',
        ['By ISBN', 'By title', 'By author'],
        Table_Formats.rounded_outline
    )
    menu.run()
    # get the selected option from the menu and split it to get the user method name (e.g. `by_isbn` -> `isbn`)
    selected = menu.get_selected_option().split('_')[1]

    book = Book()
    # get the BookFields attribute based on the user selection
    book_field = getattr(BookFields, selected)
    # get the user input based on the selected BookFields attribute and assign it to the new book
    book = get_book_input(book, book_field)
    print(book_field.name)
    print(getattr(book, book_field.name))

    library.search_book(book, book_field, 'stock')

    # TODO: add book to the library stock
    """
    check if the book is already in the library stock - if not, add it
    if the book is already in the library stock show full book details and ask if the user wants to add another copy
    ---

    library.append_book(new_isbn, new_title, 'J.R.R. Tolkien', 'Fantasy', 'English', '2001', '1')

    Add worksheet titles
    library.stock.append_row(['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies', 'Available', 'Borrowed by'])

    Add a book
    library.stock.append_row(
        ['978-3-16-148410-0', 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', '2001', '1' 'True', '']
        )
    """
