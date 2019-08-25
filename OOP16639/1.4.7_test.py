def gcd(a, b):
    assert isinstance(a, int)
    assert isinstance(b, int)
    assert a > 0
    assert b > 0
    while b:
        a, b = b, a % b
    return a

# print(gcd(9, 3))
# print(gcd('Hello', 3))
print(gcd(0, 20))
