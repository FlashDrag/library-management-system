from pyfiglet import figlet_format
from pydantic import ValidationError

from library_system.views.tools import font as F, clear_terminal, Table_Formats

from library_system.models.spreadsheet import Library
from library_system.views.console_ui import Menu
from library_system import library_manager


def display_header():
    print(figlet_format('Library Management System', 'straight'))


def library_init() -> Library:
    '''
    Initialize a Library instance and connect to the Google Sheet.

    :return: Library instance
    '''
    print('Connecting to the Library Spreadsheet...')
    library = Library('library-management-system', 'creds.json')
    library.connect()
    if not library.isConnected:
        print(f'{F.ERROR}Cannot connect to the Library Spreadsheet.{F.ENDC} Exiting...')
        exit()
    else:
        print(f'{F.BOLD}Succesfully connected.{F.ENDC}\n')
        return library


def run_main_menu():
    '''
    Displays the options available in the Library Main Menu
    using the tabulate library.
    :return: list of lists with options
    '''
    menu_name = 'Library Main Menu'
    options = ['Add Book',
               'Remove Book',
               'Check Out Book',
               'Return Book',
               'View Library Stock']
    table_format = Table_Formats.outline

    try:
        menu = Menu(menu_name, options, table_format)
        menu.run()
        selected = menu.get_selected_option()
    except (ValidationError, ValueError):
        # TODO add logging for handling errors
        print(f'{F.ERROR}Something went wrong. Refresh the page and try again{F.ENDC}')
        exit()
    else:
        return selected


def execute_function(library: Library, func_name: str):
    '''
    Execute the function using the function name based on the user selection.
    :param library: Library instance
    :param func_name: function name
    '''
    try:
        # try to execute the function from the library_manager module
        getattr(library_manager, func_name)(library)
    # catch exception if the function not found in library_manager using getattr()
    except AttributeError as e:
        # TODO Add logging for errors
        print(
            f'''{F.ERROR}Cannot get access to `{str(e).split("'")[-2]}` '''
            f'''at `{str(e).split("'")[1]}` {str(e).split("'")[0]}.{F.ENDC} Exiting...''')
        exit()


def main():
    ''''
    Clear terminal screen, display text header;
    Initialize Library instance, connect to the Google Sheet;
    Display the Main Menu and process user selection.
    '''
    clear_terminal()
    display_header()

    library = library_init()
    selected = run_main_menu()
    execute_function(library, selected)


if __name__ == '__main__':
    main()
