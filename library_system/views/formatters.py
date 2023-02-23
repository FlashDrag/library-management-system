import os


def clear_terminal():
    '''Clear terminal screen'''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")


class font:
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    HEADER = '\033[92m'
    ERROR = '\033[91m'
    YELLOW = '\033[93m'
    UNDERLINE = '\033[4m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GREY = '\033[90m'
    ENDC = '\033[0m'
