from app.services.tools import font as F, clear_terminal
from app.services.spreadsheet import Library


def add_book(library: Library):
    clear_terminal()
    print(F.HEADER + 'Adding books' + F.ENDC)
    new_isbn = input(f'{F.ITALIC}Enter ISBN of the Book:{F.ENDC}\n')
    new_title = input(f'{F.ITALIC}Enter Title of the Book:{F.ENDC}\n')
    # library.append_book('978-3-16-148410-0', 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 'English', '2001', '1')
    library.append_book(new_isbn, new_title, 'J.R.R. Tolkien', 'Fantasy', 'English', '2001', '1')
