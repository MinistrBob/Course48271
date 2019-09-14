"""В классе TestFactorization, потомке TestCase, создан метод test_simple_multipliers().
Требуется написать проверку того, что a умножить на b равно x, с использованием унаследованного от TestCase метода assertEqual.
(Обратите внимание, что импортировать библиотеку и запускать unittest.main() не требуется.)"""
import unittest


def factorize(x):
    a = x / 10
    b = 10
    return a, b


class TestFactorization(unittest.TestCase):
    def test_simple_multipliers(self):
        x = 77
        a, b = factorize(x)
        self.assertEqual(a * b, x)


if __name__ == "__main__":
    unittest.main()
