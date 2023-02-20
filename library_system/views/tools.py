import os
from enum import Enum


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


class Table_Formats(Enum):
    '''
    Supported table formats for `tabulate` library
    '''
    plain = "plain"
    simple = "simple"
    gihub = "github"
    grid = 'grid'
    simple_grid = 'simple_grid'
    rounded_grid = 'rounded_grid'
    heavy_grid = 'heavy_grid'
    mixed_grid = 'mixed_grid'
    double_grid = 'double_grid'
    fancy_grid = 'fancy_grid'
    outline = 'outline'
    simple_outline = 'simple_outline'
    rounded_outline = 'rounded_outline'
    heavy_outline = 'heavy_outline'
    mixed_outline = 'mixed_outline'
    double_outline = 'double_outline'
    fancy_outline = 'fancy_outline'
    pipe = 'pipe'
    orgtbl = 'orgtbl'
    asciidoc = 'asciidoc'
    jira = 'jira'
    presto = 'presto'
    pretty = 'pretty'
    psql = 'psql'
    rst = 'rst'
    mediawiki = 'mediawiki'
    moinmoin = 'moinmoin'
    youtrack = 'youtrack'
    html = 'html'
    unsafehtml = 'unsafehtml'
    latex = 'latex'
    latex_raw = 'latex_raw'
    latex_booktabs = 'latex_booktabs'
    latex_longtable = 'latex_longtable'
    textile = 'textile'
    tsv = 'tsv'
