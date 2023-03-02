import logging

from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich import box, padding as p

from pydantic import ValidationError

from library_system.tools import restart_app
from library_system.models.book import Book, BookFields, BorrowFields
from library_system.models.validators import IntInRange, MenuOptions, NonEmptyStr
from library_system.models.worksheets_cfg import WorksheetSets
from library_system.tools import F

logger = logging.getLogger(__name__)


class Menu:

    '''
    Displays menu with numbered options.
    Gets user input and validates it.

    :param name: menu name
    :param options: list of menu options
    :param table_format: table output format
    :param maxcolwidths: max column width for table output
    '''

    def __init__(self,
                 title: str,
                 options: list[str] | list[dict],
                 table_format: box.Box = box.MINIMAL,
                 expand: bool = False,
                 padding: p.PaddingDimensions = (0, 1)):
        # Validates the input menu name and options list using `NonEmptyStr` and `MenuOptions` validators.
        self._title: str = NonEmptyStr(str_value=title).str_value
        self._options: list = MenuOptions(lst=options).lst

        self._table_format = table_format
        self._expand = expand
        self._padding = padding

        self._numbered_options: list[dict] = self._numerate_options()
        self._selected_code: int | None = None

    @staticmethod
    def print_table(
            options: list[dict],
            table_format: box.Box,
            title: str | None = None,
            expand: bool = False,
            padding: p.PaddingDimensions = (0, 1)):
        '''
        Prints a table based on options list of dictionaries using `rich` library.
        Set column headers to the keys of the first dictionary in the list.
        Set row values to the values of the dictionaries in the list.

        Default settings: title style - green, title justify - left, column overflow - fold;
        console print default options: overflow - fold

        :param options: list of dictionaries with table data
        :param table_format: table output format
        :param title: table title
        :param expand: expand table to the full width of the console
        :param padding: table padding: (top, right, bottom, left). Default:
        (0, 1) - no padding on top and bottom, 1 space on the right and left.
        '''

        title_style = Style(color='green')
        table = Table(
            title=title,
            title_style=title_style,
            title_justify='left',
            box=table_format,
            expand=expand,
            padding=padding)
        headers = options[0].keys()
        for header in headers:
            table.add_column(header, overflow='fold')

        for d in options:
            table.add_row(*map(str, d.values()))

        console = Console()
        console.print(table, overflow='fold')

    def _numerate_options(self) -> list[dict]:
        '''
        Numerate the menu options.
        '''
        # TODO sort options self._sort_options if True
        if isinstance(self._options[0], str):
            numbered_options = [{'Code': i + 1, 'Option': item}
                                for i, item in enumerate(self._options)]

        if isinstance(self._options[0], dict):
            # add new key `Code` with unique number to each dictionary and add it to a new list
            # `{"Code": i + 1} | d` creates new dict and merge `|` it with dict from `self._options`
            numbered_options = [{"Code": i + 1} |
                                d for i, d in enumerate(self._options)]

        return numbered_options  # type: ignore

    def _get_user_input(self):
        '''
        Gets user input and validates it using `IntInRange` validator.
        If the input is valid, the option code is stored in `self.selected_code`.
        '''

        while True:
            print(F.BOLD + 'Select an option using code number' + F.ENDC)
            try:
                user_selection = IntInRange(
                    num_range=len(self._options),
                    num=int(input(F.ITALIC + 'Enter option code:\n' + F.ENDC))
                )
            except ValidationError as e:
                print(
                    f'{F.ERROR}{e.errors()[0].get("msg", "Error")}\nTry again{F.ENDC}\n'
                )
                continue
            except ValueError as e:
                print(f'''{F.ERROR}Incorrect code: '''
                      f'''`{str(e).split("'")[1]}`. '''
                      f'''Code must be an integer.\nTry again\n {F.ENDC}''')
                continue
            else:
                self._selected_code = user_selection.num
                break

    def get_selected_code(self) -> int:
        '''
        Gets the selected option code.
        :return int: selected option code
        '''
        if self._selected_code is None:
            raise ValueError(
                'Cannot get selected code from self._selected_code')
        return self._selected_code

    def get_selected_option_str(self) -> str:
        '''
        Gets the selected option based on the selected code.
        :return str: selected option
        '''
        if self._selected_code is None:
            raise ValueError(
                'Cannot get selected code from self._selected_code')
        selected_option = self._numbered_options[self._selected_code - 1].get(
            'Option', None)
        if selected_option is None:
            raise ValueError(
                f'Cannot get option from self._numbered_options[{self._selected_code - 1}]')
        return selected_option.lower()

    def get_selected_option_dict(self) -> dict:
        '''
        Gets the selected option based on the selected code.
        :return dict: selected option
        '''
        if self._selected_code is None:
            raise ValueError(
                'Cannot get selected code from self._selected_code')
        selected_option = self._numbered_options[self._selected_code - 1]
        del selected_option['Code']
        return selected_option

    def run(self):
        '''
        Displays the menu and gets user input.
        '''
        Menu.print_table(self._numbered_options,
                         self._table_format, self._title,
                         self._expand, self._padding)
        self._get_user_input()


def get_book_input(book: Book, field: BookFields | BorrowFields, msg: str | None = None) -> str:
    '''
    Gets user input for specific field of the Book.
    Assigns it trought pydantic validation to the Book instance.
    :param book: Book instance
    :param field: BookFields enum
    :param msg: custom message to prompt user to enter value for the field,
    if None, default message is used based on `field` e.g: `Enter Title of the Book:`

    :return: validated user book input
    '''
    default_msg = str(field)
    message = msg if msg else default_msg
    while True:
        try:

            user_input = input(f'{F.ITALIC}{message}{F.ENDC}\n')
            # pass user input to the Book instance field based on field name
            setattr(book, field.name, user_input)
        except ValidationError as e:
            print(f"{F.ERROR}{e.errors()[0]['msg']}\nTry again.{F.ENDC}\n")
        except ValueError as e:
            logging.error(e)
            print(f"{F.ERROR}Something went wrong. Restarting...{F.ENDC}\n")
            restart_app()
        else:
            return book[field.name]


def display_book(
    book_to_display: dict,
    w_set: WorksheetSets = WorksheetSets.stock,
    table_title: str | None = None,
):
    '''
    Displays a book in a table format in order to the worksheet fields.

    :param book_to_display: dict with book data to display
    :param w_set: worksheet set to get the fields from
    :param table_title: table title
    '''
    sheet_fields = w_set.value['fields']
    # add `cell_row` displaying table if it is existed in the book dict
    fields = (sheet_fields + ['cell_row']
              ) if 'cell_row' in book_to_display else sheet_fields
    values = [book_to_display.get(field) for field in fields]
    book_to_print = dict(zip(fields, values))

    Menu.print_table([book_to_print], box.MARKDOWN,
                     title=table_title, expand=True)


'''
For testing purposes

Add the sys import to the top of the file if you want to run this module as a script:
import sys
sys.path.append('/absolute_path/to/app')  # to use dependent app modules

The below code will be executed only if this module is run as a script
'''
if __name__ == '__main__':
    # Menu
    title = 'Library Main Menu'
    options = ['Add Book',
               'Remove Book',
               'Check Out Book',
               'Return Book',
               'View Library Stock']
    table_format = box.DOUBLE_EDGE
    menu = Menu(title, options, table_format)
    menu.run()
    print(f'Selected option code: {menu.get_selected_code()}')
    print(f'Selected str option: {menu.get_selected_option_str()}')
    print(f'Selected dict option: {menu.get_selected_option_dict()}')
    print()

    # get_book_input
    book = Book()
    field = BookFields.copies
    book_value = get_book_input(book, field)
    print(book_value)
    print(book.dict())
    print(book[field.name])
    print(book.copies)
