class Colors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[34m'
    PINK = '\033[35m'
    BLUE = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    CYAN = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_BLUE = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    RESET = '\033[0m'


def print_colors():
    color_attributes = [attr for attr in dir(Colors) if not attr.startswith("__")]
    for color in color_attributes:
        print(getattr(Colors, color) + color + Colors.RESET)

