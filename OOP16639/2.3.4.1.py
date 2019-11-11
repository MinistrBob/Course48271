# Неправильный код
class Parent:
    def __init__(self, value):
        self.value = value

    def do_something(self):
        print("Function was called")


class Child(Parent):

    def do_something(self):
        super().do_something()
        self.value = 0


def function(obj: Parent):
    obj.do_something()
    if obj.value > 0:
        print("All correct!")
    else:
        print("SOMETHING IS GOING WRONG!")


# Посмотрим на поведение
parent = Parent(5)
function(parent)
print()

# Данный код должен работать корректно, если вместо родителя подставить потомка
child = Child(5)
function(child)
print()
