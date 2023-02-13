import os

from pyfiglet import figlet_format
from tabulate import tabulate


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
    print('Library Main Menu')
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
            code = int(input('Enter your choice:\n'))
        except ValueError as e:
            print(f'''Incorrect code: {str(e).split("'")[1]}. Code must be an integer. Try again\n''')
        else:
            if code in range(1, 6):
                func = '_'.join(options[code-1][1].lower().split())
                try:
                    clear_terminal()
                    globals()[func]()
                    break
                except KeyError as e:
                    print(f'Cannot get access to {e}\n')
            else:
                print(f'Incorrect code: {code}. Try again.\n')


def add_book():
    print('hello world')


def main():
    clear_terminal()
    display_header()
    display_main_menu()


if __name__ == '__main__':
    main()
