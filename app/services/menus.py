from tabulate import tabulate

from .tools import font as F
from pydantic import ValidationError
from .validators import IntInRange, UniqueStringsList, NonEmptyStr


class Menu:
    '''
    Displays menu with numbered options.
    Gets user input and validates it.
    '''
    def __init__(self, name: str, options: list[str], table_format: str = 'outline'):
        '''
        Initialize the Menu instance.
        Validates the menu name and options list using `NonEmptyStr` and `UniqueStringsList` validators.
        :param name: menu name
        :param options: list of menu options
        :param table_format: table output format for `tabulate` library
        '''
        self.name: str = NonEmptyStr(str_value=name).str_value
        self.options = UniqueStringsList(lst=options)
        self.table_format = table_format

        self.selected_code: int | None = None

    def _render_table(self):
        '''
        Get the dictionary from `UniqueStringsList` instance with
        numbered options and render it using `tabulate` library.
        :return: table with numbered options
        '''
        numbered_options = self.options.to_dict()
        table = tabulate(
            numbered_options.items(),
            headers=['Code', 'Option'], tablefmt=self.table_format
        )
        return table

    def _display(self):
        '''
        Displays the menu name with table of options.
        '''
        print(F.HEADER + self.name + F.ENDC)
        print(self._render_table())

    def _get_user_selection(self):
        '''
        Gets user input and validates it using `IntInRange` validator.
        If the input is valid, the option code is stored in `self.selected_code`.
        '''

        while True:
            print(F.BOLD + 'Select an option using code number' + F.ENDC)
            try:
                user_selection = IntInRange(
                    num_range=len(self.options.lst),
                    num=int(input(F.ITALIC + 'Enter option code:\n' + F.ENDC))
                )
            except ValidationError as e:
                print(f'{F.ERROR}{e.errors()[0].get("msg", "Error")}. Try again{F.ENDC}\n')
                continue
            except ValueError as e:
                print(f'''{F.ERROR}Incorrect code: '''
                      f'''`{str(e).split("'")[1]}`. '''
                      f'''Code must be an integer. Try again\n {F.ENDC}''')
                continue
            else:
                self.selected_code = user_selection.num
                break

    def get_selected(self) -> str:
        '''
        Convert the parsed selected option to function name
        :return: converted function name
        '''
        if self.selected_code is None:
            raise ValueError(F.ERROR + 'No option selected in the menu.' + F.ENDC)
        # Get selected option from dictionary of `UniqueStringsList` instance
        selected_option = self.options.to_dict().get(self.selected_code, None)

        if selected_option is None:
            raise ValueError(F.ERROR + 'No option selected in the menu.' + F.ENDC)
        # prepare selected option for function name
        func_name = '_'.join(selected_option.lower().split())
        return func_name

    def run(self):
        self._display()
        self._get_user_selection()


# For testing purposes
# The below code will be executed only if this module is run as a script
if __name__ == '__main__':

    options = ['Add Book',
               'Remove Book',
               'Check Out Book',
               'Return Book',
               'View Library Stock']

    try:
        menu = Menu('Library Main Menu', options)
        menu.run()
    except (ValidationError, ValueError) as e:
        print(f'{F.ERROR}{e}{F.ENDC}')
        raise SystemExit
    else:
        print(f'Selected option: {menu.get_selected()}')
