import math


class Vec2d:

    def __init__(self, v=(0, 0)):
        """
        Вектор определяется координатами x2, y2 — точка конца вектора.
        Начало вектора всегда совпадает с центом координат (x1, y1)=(0, 0).
        :param v:
        """
        if v is None:
            self.x2 = float(0)
            self.y2 = float(1)
        self.x2 = float(v[0])
        self.y2 = float(v[1])

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d((self.x2 + other.x2, self.y2 + other.y2))

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d((self.x2 - other.x2, self.y2 - other.y2))

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d((self.x2 * k, self.y2 * k))

    def __len__(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x2 * self.x2 + self.y2 * self.y2)

    def int_pair(self):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return self.x2, self.y2


aaa = Vec2d((123, 456))
x = aaa.int_pair()
print(type(x))
print(x)
