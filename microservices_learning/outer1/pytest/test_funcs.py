def is_even(number):
    return number % 2 == 0


def test_is_even():
    assert is_even(2) == True
    assert is_even(5) == False
    assert is_even(0) == True
    assert is_even(-3) == False
    assert is_even(-4) == True
    assert is_even(00.0) == True
    assert is_even(-3.4) == False
    assert is_even(float('inf')) == False
