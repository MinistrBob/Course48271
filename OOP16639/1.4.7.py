def gcd(a, b):
    assert isinstance(a, int)
    assert isinstance(b, int)
    assert a > 0
    assert b > 0
    while b:
        a, b = b, a % b
    return a
