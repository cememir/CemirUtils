import time
import functools

class CemirUtils:

    @staticmethod
    def deprecate(message):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"WARNING: {func.__name__} is deprecated. {message}")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def debug(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"DEBUG: Calling function '{func.__name__}' with arguments {args} and keyword arguments {kwargs}")
            result = func(*args, **kwargs)
            print(f"DEBUG: Function '{func.__name__}' returned {result}")
            return result
        return wrapper


# Kullanım örnekleri:

@CemirUtils.deprecate("Please use new_function instead.")
def old_function(x, y):
    return x + y

@CemirUtils.debug
def add_numbers(a, b):
    return a + b


# Örnek fonksiyonları çalıştırma
old_function(3, 5)
add_numbers(3, 5)
