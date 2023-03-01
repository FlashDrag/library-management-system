from typing import TypedDict
from enum import Enum

from library_system.models.book import BookFields, BorrowFields
from library_system.views.console_ui import TableFormats


class MenuSet(TypedDict):
    '''
    :param title: title of menu
    :param options: list of menu options
    :table_format: table output format from Table_Formats enum
    :maxcolwidths: max columns width for table output
    '''
    title: str
    options: list[str]
    table_format: TableFormats
    maxcolwidths: int | list[int] | None


# create a list of search book menu options based on BookFields enum excluding the `copies` field
search_book_menu_options = [('Search by ' + field.value) for field in BookFields if field != BookFields.copies]
# create a list of search borrower menu options based on BorrowFields enum
search_borrower_menu_options = [('Search by ' + field.value) for field in BorrowFields]


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
                 'Check Overdue Borrowers'],
        table_format=TableFormats.outline,
        maxcolwidths=None
    )
    add_book = MenuSet(
        title='How to add a book to the library stock?',
        options=search_book_menu_options,
        table_format=TableFormats.rounded_outline,
        maxcolwidths=None
    )

    remove_book = MenuSet(
        title='How to remove a book from the library stock?',
        options=search_book_menu_options,
        table_format=TableFormats.rounded_outline,
        maxcolwidths=None
    )

    check_out_book = MenuSet(
        title='How to check out a book from the library stock?',
        options=search_book_menu_options,
        table_format=TableFormats.rounded_outline,
        maxcolwidths=None
    )

    return_book = MenuSet(
        title='How to return a book to the library stock?',
        options=search_borrower_menu_options,
        table_format=TableFormats.rounded_outline,
        maxcolwidths=None
    )
