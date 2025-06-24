from src.example import sum_numbers, complex_function

def test_sum():
    assert sum_numbers([1, 2, 3]) == 6

def test_complex():
    assert complex_function(2) == 4
    assert complex_function(3) == 9
    assert complex_function(-1) == 0
