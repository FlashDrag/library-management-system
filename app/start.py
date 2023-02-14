from pyfiglet import figlet_format
from tabulate import tabulate

from app.services.tools import font as F, clear_terminal

from app.services.spreadsheet import Library


def display_header():
    print(figlet_format('Library Management System', 'straight'))


def library_init() -> Library:
    '''
    Initialize a Library instance and connect to the Google Sheet.

    :return: Library instance
    '''
    print('Connecting to the Library Spreadsheet...')
    library = Library('library-management-system', 'creds.json')
    isConnected = library.connect()
    if not isConnected:
        print(f'{F.ERROR}Cannot connect to the Library Spreadsheet.{F.ENDC} Exiting...')
        return False  # type: ignore
    else:
        print(f'{F.BOLD}Succesfully connected.{F.ENDC}\n')
        return library


def display_main_menu():
    '''
    Displays the options available in the Library Main Menu
    using the tabulate library and allows the user to select an option using code number 1-5.
    While the user enters an incorrect code or a code that's not an integer,
    an error message will be displayed and the user will be prompted to try again.
    If correct code is enetered, appropriated funtion will be called
    '''
    print(F.HEADER + 'Library Main Menu' + F.ENDC)
    headers = ['Code', 'Option']
    options = [[1, 'Add Book'],
               [2, 'Remove Book'],
               [3, 'Check Out Book'],
               [4, 'Return Book'],
               [5, 'View Library Stock']]

    print(tabulate(options, headers=headers, tablefmt='outline'), '\n')

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
                func = '_'.join(options[code - 1][1].lower().split())
                try:
                    globals()[func]()
                    break
                except KeyError as e:
                    print(f'{F.ERROR}Cannot get access to {e}\n{F.ENDC}')
            else:
                print(f'{F.ERROR}Incorrect code: '
                      f'`{code}`.{F.ENDC} Try again.\n')


def on_startup() -> Library:
    ''''
    Clear terminal screen, display text header, initialize Library instance,
    connect to the Google Sheet and display the Main Menu.

    :return: Library instance
    '''
    clear_terminal()
    display_header()

    library = library_init()
    if not library:
        exit()

    display_main_menu()

    return library
