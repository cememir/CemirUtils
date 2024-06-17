import time

from cemirutils import CemirUtilsDecorators


@CemirUtilsDecorators.timeit
@CemirUtilsDecorators.log
def example_function(x, y):
    time.sleep(1)
    return x + y


@CemirUtilsDecorators.retry(retries=5, delay=2)
def may_fail_function():
    if time.time() % 2 < 1:
        raise ValueError("Random failure!")
    return "Success"


@CemirUtilsDecorators.cache
def slow_function(x):
    time.sleep(2)  # Zaman alacak bir işlem yapalım.
    return x * x


# Örnek fonksiyonları çalıştırma
example_function(3, 5)
may_fail_function()
print(slow_function(4))
print(slow_function(4))  # Bu sefer önbellekten sonuç dönecek
