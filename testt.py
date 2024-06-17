import time

from cemirutils import CemirUtilsDecorators


@CemirUtilsDecorators.deprecate("Please use new_function instead.")
def old_function(x, y):
    return x + y

@CemirUtilsDecorators.debug
def add_numbers(a, b):
    return a + b


# Örnek fonksiyonları çalıştırma
old_function(3, 5)
add_numbers(3, 5)
