import contextlib
import os


def cls():
    """Clear the console"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_hline():
    terminal_size = os.get_terminal_size()
    print("-" * terminal_size.columns)


@contextlib.contextmanager
def print_in_box(top=True, bottom=True):
    if top:
        print_hline()
    yield
    if bottom:
        print_hline()


class Color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def multi_line_input(prompt=""):
    print(prompt)
    lines = []
    while line := input():
        lines.append(line)
    return "\n".join(lines)
