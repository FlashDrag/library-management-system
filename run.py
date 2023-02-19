from pyfiglet import figlet_format
from pydantic import ValidationError

from app.services.tools import font as F, clear_terminal

from app.services.spreadsheet import Library
from app.services.menus import Menu
from app import library_manager


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

    try:
        menu = Menu(menu_name, options)
        menu.run()
        selected = menu.get_selected()
    except (ValidationError, ValueError) as e:
        print(f'{F.ERROR}{e}{F.ENDC}')
        raise SystemExit
    else:
        return selected


def execute_function(library: Library, func_name: str):
    try:
        # try to execute the function from the library_manager module
        getattr(library_manager, func_name)(library)
    # catch exception if the function not found in library_manager using getattr()
    except AttributeError as e:
        print(
            f'''{F.ERROR}Cannot get access to `{str(e).split("'")[-2]}` '''
            f'''at `{str(e).split("'")[1]}` {str(e).split("'")[0]}.{F.ENDC}''')
        exit()


# TODO Add logging for errors
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
