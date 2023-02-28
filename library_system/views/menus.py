from typing import TypedDict
from enum import Enum
from library_system.views.console_ui import Table_Formats


class MenuSet(TypedDict):
    '''
    :param title: title of menu
    :param options: list of menu options
    :table_format: table output format from Table_Formats enum
    '''
    title: str
    options: list[str]
    table_format: Table_Formats


class MenuSets(Enum):
    '''
    Enum of `MenuSet` instances.
    Each `MenuSet` contains:
    menu `title`, `options` and `table_format`(table output format from Table_Formats enum)
    '''
    main_menu = MenuSet(
        title='Library Main Menu',
        options=['Add Book',
                 'Remove Book',
                 'Check Out Book',
                 'Return Book',
                 'View Library Stock'],
        table_format=Table_Formats.outline
    )
    add_book = MenuSet(
        title='How to add a book to the library stock?',
        options=['By ISBN', 'By title', 'By author'],
        table_format=Table_Formats.rounded_outline
    )

    remove_book = MenuSet(
        title='How to remove a book from the library stock?',
        options=['By ISBN', 'By title', 'By author'],
        table_format=Table_Formats.rounded_outline
    )

    check_out_book = MenuSet(
        title='How to check out a book from the library stock?',
        options=['By ISBN', 'By title', 'By author'],
        table_format=Table_Formats.rounded_outline
    )
