import sys
import time

from library_system.models.spreadsheet import Library
from library_system.views.console_ui import Menu
from library_system.views.menus import MenuSets
from library_system import library_manager
from library_system.tools import F, clear_terminal


def run_main_menu():
    '''
    Displays the options available in the Library Main Menu
    using the tabulate library.
    :return: selected option name
    '''
    menu = Menu(**MenuSets.main_menu.value)
    menu.run()
    selected = menu.get_selected_option_str()

    return selected


def run_selected_option(library: Library, selected_option: str):
    '''
    Execute the function using the function name based on the user selection.
    :param library: Library instance
    :param selected_option: selected option name
    '''
    func_name = selected_option.replace(' ', '_')
    getattr(library_manager, func_name)(library)


# entry point for the startup functionality
def back_to_menu(library: Library):
    '''
    Go back to the main menu after user input.
    '''
    print(f'{F.ITALIC}Enter any key to go back to the main menu or Ctrl+C to exit.{F.ENDC}')

    try:
        input()
    # catch KeyboardInterrupt to exit the app
    except KeyboardInterrupt:
        print(f'{F.ERROR}Exiting...{F.ENDC}')
        sys.exit()
    else:
        print(f'{F.YELLOW}Back to the main menu...{F.ENDC}')
        time.sleep(1)
        clear_terminal()
        selected_option = run_main_menu()
        run_selected_option(library, selected_option)
