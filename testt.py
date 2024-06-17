from cemirutils import CemirUtilsConditions

cemir_utils = CemirUtilsConditions()

@cemir_utils.condition_collector
def test_function(x, y, z):
    if x > 15:
        # print("x is greater than 15")
        pass
    elif x < 15 and y > 10:
        # print("x is less than 15 and y is greater than 10")
        pass
    else:
        # print("x is not within the expected range or y is not greater than 10")
        pass

    if y == 20:
        # print("y is exactly 20")
        pass
    elif y >= 15:
        # print("y is greater than or equal to 15")
        pass
    else:
        # print("y is less than 15")
        pass

    if z == "hello":
        # print("z is 'hello'")
        pass
    elif z == "world":
        # print("z is 'world'")
        pass
    else:
        # print("z is something else")
        pass

    if x == 10:
        # print("x is 10")
        pass
    elif x >= 10:
        # print("x is greater than or equal to 10")
        pass
    else:
        # print("x is less than 10")
        pass

    if y % 2 == 0:
        # print("y is even")
        pass
    else:
        # print("y is odd")
        pass

    if z.startswith("hq"):
        # print("z starts with 'h'")
        pass
    elif z.startswith("w"):
        # print("z starts with 'w'")
        pass
    else:
        # print("z starts with another letter")
        pass


test_function(10, 20, "hello")
