from typing import TypedDict
from enum import Enum

from library_system.models.book import BookFields, BorrowFields
from rich import box


class MenuSet(TypedDict):
    '''
    :param title: title of menu
    :param options: list of menu options
    :table_format: table output format from Table_Formats enum
    :maxcolwidths: max columns width for table output
    '''
    title: str
    options: list[str]
    table_format: box.Box


# list of search book menu options based on BookFields enum excluding the `copies` field
search_book_menu_options = [('Search by ' + field.value) for field in BookFields if field != BookFields.copies]
# list of search borrower menu options based on BorrowFields enum
search_borrower_menu_options = [('Search by ' + field.value) for field in BorrowFields]

# list of view stock menu options based on BookFields enum
view_library_stock_menu_options = [('Sorted by ' + field.value) for field in BookFields]
view_library_stock_menu_options.insert(0, 'Spreadsheet order')

# list of borrowed_stock menu options based on BorrowFields enum
view_borrowed_stock_menu_options = [('Sorted by ' + field.value) for field in BorrowFields]
view_borrowed_stock_menu_options.insert(0, 'Spreadsheet order')


class MenuSets(Enum):
    '''
    Enum of `MenuSet` instances.
    Each `MenuSet` contains:
    menu `title`, `options` and `table_format`(table output format from Table_Formats enum), maxcolwidths
    '''
    main_menu = MenuSet(
        title='Library Main Menu',
        options=['Add Book',
                 'Remove Book',
                 'Check Out Book',
                 'Return Book',
                 'Check Overdue Borrowers',
                 'View Library Stocks'],
        table_format=box.MINIMAL_DOUBLE_HEAD,
    )
    add_book = MenuSet(
        title='How to add a book to the library stock?',
        options=search_book_menu_options,
        table_format=box.MINIMAL_DOUBLE_HEAD,
    )

    remove_book = MenuSet(
        title='How to remove a book from the library stock?',
        options=search_book_menu_options,
        table_format=box.MINIMAL_DOUBLE_HEAD,
    )

    check_out_book = MenuSet(
        title='How to check out a book from the library stock?',
        options=search_book_menu_options,
        table_format=box.MINIMAL_DOUBLE_HEAD,
    )

    return_book = MenuSet(
        title='How to return a book to the library stock?',
        options=search_borrower_menu_options,
        table_format=box.MINIMAL_DOUBLE_HEAD,
    )

    view_library_stock = MenuSet(
        title='How to view the library stock?',
        options=view_library_stock_menu_options,
        table_format=box.MINIMAL_DOUBLE_HEAD,
    )

    view_borrowed_stock = MenuSet(
        title='How to view the borrowed stock?',
        options=view_borrowed_stock_menu_options,
        table_format=box.MINIMAL_DOUBLE_HEAD,
    )
