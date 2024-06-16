from cemirutils.utils import CemirUtilsErrors

cemir_utils = CemirUtilsErrors()


@cemir_utils.condition_collector
def test_function(x, y, z):
    if x > 15:
        print("x is greater than 15")
    elif x < 15 and y > 10:
        print("x is less than 15 and y is greater than 10")
    else:
        print("x is not within the expected range or y is not greater than 10")

    if y == 20:
        print("y is exactly 20")
    elif y >= 15:
        print("y is greater than or equal to 15")
    else:
        print("y is less than 15")

    if z == "hello":
        print("z is 'hello'")
    elif z == "world":
        print("z is 'world'")
    else:
        print("z is something else")

    if x == 10:
        print("x is 10")
    elif x >= 10:
        print("x is greater than or equal to 10")
    else:
        print("x is less than 10")

    if y % 2 == 0:
        print("y is even")
    else:
        print("y is odd")

    if z.startswith("hq"):
        print("z starts with 'h'")
    elif z.startswith("w"):
        print("z starts with 'w'")
    else:
        print("z starts with another letter")


test_function(10, 20, "hello")
