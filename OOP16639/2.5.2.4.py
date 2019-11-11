# Переопределим some_method в B и C, а в С значение атрибута value
class A:
    value = 13

    def some_method(self):
        print(f"Method in A, value = {self.value}")


class B(A):

    def some_method(self):
        print(f"Method in B, value = {self.value}")


class C(A):
    value = 6

    def some_method(self):
        print(f"Method in С, value = {self.value}")


class D(B, C):
    pass


# Рассмотрим реализацию в D
D().some_method()
print()
x=D()
print(x.__mro__)
