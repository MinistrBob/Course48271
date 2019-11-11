# python -m unittest -v C:/MyGit/Course48271/OOP16639/1_6_test.py
import unittest


def factorize(n):
    """
        Factorize positive integer and return its factors.
        :type n: int,>=0
        :rtype: tuple[N],N>0
    """
    if not isinstance(n, int):
        raise TypeError
    if n < 0:
        raise ValueError
    if n == 0:
        return 0,
    if n == 1:
        return 1,

    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        ans.append(n)
    return tuple(ans)


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        cases = ('string', 1.5)
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        cases = (-1, -10, -100)
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        cases = ((0, (0,)), (1, (1,)))
        for x in cases:
            with self.subTest(x=x):
                self.assertTupleEqual(x[1], factorize(x[0]))

    def test_simple_numbers(self):
        cases = ((3, (3, )), (13, (13, )), (29, (29, )))
        for x in cases:
            with self.subTest(x=x):
                self.assertTupleEqual(x[1], factorize(x[0]))

    def test_two_simple_multipliers(self):
        cases = ((6, (2, 3)), (26, (2, 13)), (121, (11, 11)))
        for x in cases:
            with self.subTest(x=x):
                self.assertTupleEqual(x[1], factorize(x[0]))

    def test_many_multipliers(self):
        cases = ((1001, (7, 11, 13)), (9699690, (2, 3, 5, 7, 11, 13, 17, 19)))
        for x in cases:
            with self.subTest(x=x):
                self.assertTupleEqual(x[1], factorize(x[0]))


if __name__ == "__main__":
    unittest.main()
