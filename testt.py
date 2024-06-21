import re


def cprint(data, indent=0):
    """
    İç içe veri türlerine göre renklendirme yaparak çıktı verir.

    Args:
        data (any): Yazdırılacak veri.
        indent (int): Girinti seviyesi.

    Returns:
        None
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "reset": "\033[0m"
    }

    def print_with_indent(string, indent_level):
        print(" " * 4 * indent_level + string)

    def colorize_numbers(string):
        def replace_with_color(match):
            value = match.group(0)
            if '.' in value:
                return f'{colors["yellow"]}{value}{colors["reset"]}'
            else:
                return f'{colors["blue"]}{value}{colors["reset"]}'

        return re.sub(r'\d+\.\d+|\d+', replace_with_color, string)

    if isinstance(data, str):
        print_with_indent(f'{colors["green"]}String: {colorize_numbers(data)}{colors["reset"]}', indent)
    elif isinstance(data, int):
        print_with_indent(f'{colors["blue"]}Integer: {data}{colors["reset"]}', indent)
    elif isinstance(data, float):
        print_with_indent(f'{colors["yellow"]}Float: {data}{colors["reset"]}', indent)
    elif isinstance(data, bool):
        print_with_indent(f'{colors["cyan"]}Boolean: {data}{colors["reset"]}', indent)
    elif isinstance(data, list):
        print_with_indent(f'{colors["magenta"]}List:{colors["reset"]}', indent)
        for item in data:
            cprint(item, indent + 1)
    elif isinstance(data, dict):
        print_with_indent(f'{colors["red"]}Dictionary:{colors["reset"]}', indent)
        for key, value in data.items():
            print_with_indent(f'{colors["green"]}{key}:{colors["reset"]}', indent + 1)
            cprint(value, indent + 2)
    else:
        print_with_indent(str(data), indent)


# Test cprint function with specific strings
test_strings = [
    "------------------",
    "Loop 1 (For at line 10): 0.12 seconds",
    "Loop 2 (While at line 20): 0.34 seconds",
    "Total execution time of 'example_function': 1.56 seconds",
    "------------------"
]

for s in test_strings:
    cprint(s)
