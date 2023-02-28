import logging
import time
from enum import Enum
from tabulate import tabulate

from pydantic import ValidationError
from library_system.models.book import Book, BookFields, BorrowFields
from library_system.models.validators import IntInRange, MenuOptions, NonEmptyStr
from library_system.models.worksheets_cfg import WorksheetSets

from library_system.views.formatters import font as F

logger = logging.getLogger(__name__)


class Table_Formats(Enum):
    '''
    Supported table formats for `tabulate` library
    '''
    plain = "plain"
    simple = "simple"
    gihub = "github"
    grid = 'grid'
    simple_grid = 'simple_grid'
    rounded_grid = 'rounded_grid'
    heavy_grid = 'heavy_grid'
    mixed_grid = 'mixed_grid'
    double_grid = 'double_grid'
    fancy_grid = 'fancy_grid'
    outline = 'outline'
    simple_outline = 'simple_outline'
    rounded_outline = 'rounded_outline'
    heavy_outline = 'heavy_outline'
    mixed_outline = 'mixed_outline'
    double_outline = 'double_outline'
    fancy_outline = 'fancy_outline'
    pipe = 'pipe'
    orgtbl = 'orgtbl'
    asciidoc = 'asciidoc'
    jira = 'jira'
    presto = 'presto'
    pretty = 'pretty'
    psql = 'psql'
    rst = 'rst'
    mediawiki = 'mediawiki'
    moinmoin = 'moinmoin'
    youtrack = 'youtrack'
    html = 'html'
    unsafehtml = 'unsafehtml'
    latex = 'latex'
    latex_raw = 'latex_raw'
    latex_booktabs = 'latex_booktabs'
    latex_longtable = 'latex_longtable'
    textile = 'textile'
    tsv = 'tsv'


class Menu:

    '''
    Displays menu with numbered options.
    Gets user input and validates it.

    :param name: menu name
    :param options: list of menu options
    :param table_format: table output format from Table_Formats enum
    '''

    def __init__(self,
                 title: str,
                 options: list[str] | list[dict],
                 table_format: Table_Formats = Table_Formats.simple,
                 sort_options: bool = False):
        # Validates the input menu name and options list using `NonEmptyStr` and `MenuOptions` validators.
        self._name: str = NonEmptyStr(str_value=title).str_value
        self._options: list = MenuOptions(lst=options).lst
        # gets the value from `Table_Formats` enum.
        self._table_format: str = table_format.value
        self._sort_options = sort_options

        self._numbered_options: list[dict] = self._numerate_options()
        self._selected_code: int | None = None

    def _numerate_options(self) -> list[dict]:
        '''
        Numerate the menu options.
        '''
        # TODO sort options self._sort_options if True
        if isinstance(self._options[0], str):
            numbered_options = [{'Code': i + 1, 'Option': item} for i, item in enumerate(self._options)]

        if isinstance(self._options[0], dict):
            # add new key `Code` with unique number to each dictionary and add it to a new list
            # `{"Code": i + 1} | d` creates new dict and merge `|` it with dict from `self._options`
            numbered_options = [{"Code": i + 1} | d for i, d in enumerate(self._options)]

        return numbered_options  # type: ignore

    def _render_table(self):
        '''
        Render the table using `tabulate` library.
        Set table headers as keys of `self._numbered_options` dicts.
        :return: table with numbered options
        '''
        table = tabulate(
            self._numbered_options,
            headers='keys',
            tablefmt=self._table_format
        )
        return table

    def display(self):
        '''
        Displays the menu name with table of options.
        '''
        print(F.HEADER + self._name + F.ENDC)
        print(self._render_table())

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
                    f'{F.ERROR}{e.errors()[0].get("msg", "Error")}. Try again{F.ENDC}\n'
                )
                continue
            except ValueError as e:
                print(f'''{F.ERROR}Incorrect code: '''
                      f'''`{str(e).split("'")[1]}`. '''
                      f'''Code must be an integer. Try again\n {F.ENDC}''')
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
            raise ValueError('Cannot get selected code from self._selected_code')
        return self._selected_code

    def get_selected_option_str(self) -> str:
        '''
        Gets the selected option based on the selected code.
        :return str: selected option
        '''
        if self._selected_code is None:
            raise ValueError('Cannot get selected code from self._selected_code')
        selected_option = self._numbered_options[self._selected_code - 1].get('Option', None)
        if selected_option is None:
            raise ValueError(f'Cannot get option from self._numbered_options[{self._selected_code - 1}]')
        return selected_option.lower()

    def get_selected_option_dict(self) -> dict:
        '''
        Gets the selected option based on the selected code.
        :return dict: selected option
        '''
        if self._selected_code is None:
            raise ValueError('Cannot get selected code from self._selected_code')
        selected_option = self._numbered_options[self._selected_code - 1]
        del selected_option['Code']
        return selected_option

    def run(self):
        '''
        Displays the menu and gets user input.
        '''
        self.display()
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
            print(f"{F.ERROR}{e.errors()[0]['msg']}.Try again.{F.ENDC}\n")
        except ValueError as e:
            logging.error(e)
            print(f"{F.ERROR}Something went wrong. Restarting...{F.ENDC}\n")
            time.sleep(2)
            exit()
            # TODO restart the app
        else:
            return book[field.name]


def display_book(book_to_display: dict):
    '''
    Displays a book in a table format in order to the worksheet fields.
    '''
    fields = WorksheetSets.stock.value['fields'] + ['cell_row']
    values = [book_to_display[field] for field in fields]
    print(tabulate([values], fields) + '\n')


'''
For testing purposes

Add the sys import to the top of the file if you want to run this module as a script:
import sys
sys.path.append('/absolute_path/to/app')  # to use dependent app modules

The below code will be executed only if this module is run as a script
'''
if __name__ == '__main__':
    # Menu
    name = 'Library Main Menu'
    options = ['Add Book',
               'Remove Book',
               'Check Out Book',
               'Return Book',
               'View Library Stock']
    table_format = Table_Formats.double_grid
    menu = Menu(name, options, table_format)
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
