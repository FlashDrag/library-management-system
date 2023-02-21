from library_system.views.tools import font as F, clear_terminal, BookFields
from library_system.views.console_ui import get_input
from library_system.models.spreadsheet import Library


def add_book(library: Library):
    clear_terminal()
    print(f'{F.HEADER}ADDING BOOKS{F.ENDC}\n')

    title = get_input(BookFields.title)
    print(title)

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
