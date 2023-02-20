from library_system.views.tools import font as F, clear_terminal
from library_system.models.spreadsheet import Library


def add_book(library: Library):
    clear_terminal()
    print(F.HEADER + 'Adding books' + F.ENDC)
    # TODO: add book to the library stock
    # new_isbn = input(f'{F.ITALIC}Enter ISBN of the Book:{F.ENDC}\n')
    # new_title = input(f'{F.ITALIC}Enter Title of the Book:{F.ENDC}\n')
    # new_author = input(f'{F.ITALIC}Enter Author of the Book:{F.ENDC}\n')
    # library.append_book(new_isbn, new_title, 'J.R.R. Tolkien', 'Fantasy', 'English', '2001', '1')

    # Add worksheet titles
    # library.stock.append_row(['ISBN', 'Title', 'Author', 'Genre', 'Year', 'Copies', 'Available', 'Borrowed by'])

    # Add a book
    # library.stock.append_row(['978-3-16-148410-0', 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', '2001', '1' 'True', ''])
