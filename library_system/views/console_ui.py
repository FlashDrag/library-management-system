from tabulate import tabulate

from .tools import font as F, Table_Formats, BookFields
from pydantic import ValidationError
from ..models.validators import IntInRange, UniqueStringsList, NonEmptyStr, Book


class Menu:
    '''
    Displays menu with numbered options.
    Gets user input and validates it.

    :param name: menu name
    :param options: list of menu options
    :param table_format: table output format from Table_Formats enum
    '''

    def __init__(self,
                 name: str,
                 options: list[str],
                 table_format: Table_Formats = Table_Formats.simple):
        # Validates the input menu name and options list using `NonEmptyStr` and `UniqueStringsList` validators.
        self.name: str = NonEmptyStr(str_value=name).str_value
        self.options: UniqueStringsList = UniqueStringsList(lst=options)
        # gets the value from `Table_Formats` enum.
        self.table_format: str = table_format.value

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

    def display(self):
        '''
        Displays the menu name with table of options.
        '''
        print(F.HEADER + self.name + F.ENDC)
        print(self._render_table())

    def get_user_input(self):
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
                self.selected_code = user_selection.num
                return self.selected_code

    def get_selected_option(self) -> str:
        '''
        Convert the selected option to lowercase and replace spaces with underscores.
        :return: option name string in format: `option_name` (e.g. `add_book`, `by_title`)
        '''
        if self.selected_code is None:
            raise ValueError(
                F.ERROR + 'No option selected in the menu.' + F.ENDC
            )
        # Get selected option from dictionary of `UniqueStringsList` instance
        selected_option = self.options.to_dict().get(self.selected_code, None)

        if selected_option is None:
            raise ValueError(
                F.ERROR + 'No option selected in the menu.' + F.ENDC
            )
        # prepare selected option for function name
        option_name = '_'.join(selected_option.lower().split())
        return option_name

    def run(self):
        '''
        Displays the menu and gets user input.
        '''
        self.display()
        self.get_user_input()


def get_input(field: BookFields):
    while True:
        try:
            user_input = input(f'{F.ITALIC}{str(field)}{F.ENDC}\n')
            Book.validate_input(field, user_input)
        except ValueError as e:
            print(e, 'Try again.\n')
            continue
        except AttributeError:
            # TODO: add logging
            pass
        else:
            break
    return user_input


# For testing purposes
# The below code will be executed only if this module is run as a script
if __name__ == '__main__':

    name = 'Library Main Menu'
    options = ['Add Book',
               'Remove Book',
               'Check Out Book',
               'Return Book',
               'View Library Stock']
    table_format = Table_Formats.double_grid

    try:
        menu = Menu(name, options, table_format)
        menu.run()
    except (ValidationError, ValueError):
        # TODO add logging: logger.error(e)
        print(f'{F.ERROR}Error. Refresh the page and try again{F.ENDC}')
        exit()
    else:
        print(f'Selected option code: {menu.selected_code}')
        print(f'Selected option: {menu.get_selected_option()}')
