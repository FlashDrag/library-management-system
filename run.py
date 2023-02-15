from pyfiglet import figlet_format
from tabulate import tabulate

from app.services.tools import font as F, clear_terminal

from app.services.spreadsheet import Library


def display_header():
    print(figlet_format('Library Management System', 'straight'))


def library_init() -> Library | bool:
    '''
    Initialize a Library instance and connect to the Google Sheet.

    :return: Library instance
    '''
    print('Connecting to the Library Spreadsheet...')
    library = Library('library-management-system', 'creds.json')
    isConnected = library.connect()
    if not isConnected:
        print(f'{F.ERROR}Cannot connect to the Library Spreadsheet.{F.ENDC} Exiting...')
        return False
    else:
        print(f'{F.BOLD}Succesfully connected.{F.ENDC}\n')
        return library


def display_main_menu() -> list[list[object]]:
    '''
    Displays the options available in the Library Main Menu
    using the tabulate library.
    :return: list of lists with options
    '''
    print(F.HEADER + 'Library Main Menu' + F.ENDC)
    headers = ['Code', 'Option']
    options = [[1, 'Add Book'],
               [2, 'Remove Book'],
               [3, 'Check Out Book'],
               [4, 'Return Book'],
               [5, 'View Library Stock']]

    print(tabulate(options, headers=headers, tablefmt='outline'), '\n')

    return options


def get_user_selection(options, library: Library):
    '''
    Get user selection from the Main Menu and process it.
    While the user enters an incorrect code or a code that's not an integer,
    an error message will be displayed and the user will be prompted to try again.
    If correct code is enetered, appropriated funtion will be called.

    :param options: list of lists with options
    :param library: Library instance
    '''
    while True:
        print(F.BOLD + 'Select an option using code number(1-5)' + F.ENDC)
        try:
            code = int(input(F.ITALIC + 'Enter your choice:\n' + F.ENDC))
        except ValueError as e:
            print(f'''{F.ERROR}Incorrect code:'''
                  f'''{str(e).split("'")[1]}`.{F.ENDC} '''
                  f'''Code must be an integer. Try again\n''')
        else:
            if code in range(1, 6):
                # convert option to function name
                func = '_'.join(options[code - 1][1].lower().split())
                try:
                    globals()[func](library)
                    break
                except KeyError as e:
                    print(f'{F.ERROR}Cannot get access to {e}\n{F.ENDC}')
            else:
                print(f'{F.ERROR}Incorrect code: '
                      f' `{code}`.{F.ENDC} Try again.\n')


def main():
    ''''
    Clear terminal screen, display text header;
    Initialize Library instance, connect to the Google Sheet;
    Display the Main Menu and process user selection.
    '''
    clear_terminal()
    display_header()

    library = library_init()
    if not library:
        exit()

    options = display_main_menu()
    get_user_selection(options, library)  # type: ignore


if __name__ == '__main__':
    main()
