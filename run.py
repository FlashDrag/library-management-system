import os

from pyfiglet import figlet_format
from tabulate import tabulate


class font:
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    HEADER = '\033[92m'
    ERROR = '\033[91m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'


def clear_terminal():
    '''Clear terminal screen'''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")


def display_header():
    print(figlet_format('Library Management System', 'straight'))


def display_main_menu():
    '''
    Displays the options available in the Library Main Menu
    using the tabulate library and allows the user to select an option using code number 1-5.
    While the user enters an incorrect code or a code that's not an integer,
    an error message will be displayed and the user will be prompted to try again.
    If correct code is enetered, appropriated funtion will be called
    '''
    print(font.HEADER + 'Library Main Menu' + font.ENDC)
    headers = ['Code', 'Option']
    options = [[1, 'Add Book'],
               [2, 'Remove Book'],
               [3, 'Check Out Book'],
               [4, 'Return Book'],
               [5, 'View Library Stock']]

    print(tabulate(options, headers=headers, tablefmt='outline'), '\n')

    while True:
        print('Select an option using code number(1-5)')
        try:
            code = int(input(font.ITALIC + 'Enter your choice:\n'))
        except ValueError as e:
            print(f'''{font.ERROR}Incorrect code: `{str(e).split("'")[1]}`.{font.ENDC} '''
                  f'''Code must be an integer. Try again\n''')
        else:
            if code in range(1, 6):
                func = '_'.join(options[code-1][1].lower().split())
                try:
                    globals()[func]()
                    break
                except KeyError as e:
                    print(f'{font.ERROR}Cannot get access to {e}\n{font.ENDC}')
            else:
                print(f'{font.ERROR}Incorrect code: `{code}`.{font.ENDC} Try again.\n')


def add_book():
    clear_terminal()
    print(font.HEADER + 'Adding books' + font.ENDC)



def main():
    clear_terminal()
    display_header()
    display_main_menu()


if __name__ == '__main__':
    main()
