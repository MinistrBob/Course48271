"""
Вам дан объект класса SomeObject, содержащего три поля: integer_field, float_field и string_field:

Необходимо реализовать поведение:

EventGet(<type>) - создаёт событие получения данных соответствующего типа
EventSet(<value>)  - создаёт событие изменения поля типа type(<value>)
Необходимо реализовать классы NullHandler, IntHandler, FloatHandler, StrHandler, чтобы можно было создать цепочку:

chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
Описание работы цепочки:

chain.handle(obj, EventGet(int)) — вернуть значение obj.integer_field
chain.handle(obj, EventGet(str)) — вернуть значение obj.string_field
chain.handle(obj, EventGet(float)) — вернуть значение obj.float_field
chain.handle(obj, EventSet(1)) — установить значение obj.integer_field =1
chain.handle(obj, EventSet(1.1)) — установить значение obj.float_field = 1.1
chain.handle(obj, EventSet("str")) — установить значение obj.string_field = "str"
"""


class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, type_):
        if type_ is int:
            self.type_ = 'int'
        elif type_ is float:
            self.type_ = 'float'
        elif type_ is str:
            self.type_ = 'str'
        else:
            raise Exception("Нет такого типа")


class EventSet:
    def __init__(self, value):
        self.value = value
        if isinstance(self.value, int):
            self.type_ = 'int'
        elif isinstance(self.value, float):
            self.type_ = 'float'
        elif isinstance(self.value, str):
            self.type_ = 'str'
        else:
            raise Exception("Нет такого типа")


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj_, event):
        print("NullHandler-handle")
        if self.__successor is not None:
            return self.__successor.handle(obj_, event)


class IntHandler(NullHandler):
    def handle(self, obj_, event):
        print("IntHandler-handle")
        if event.type_ == 'int':
            if isinstance(event, EventGet):
                return obj_.integer_field
            else:
                obj_.integer_field = event.value
        else:
            return super().handle(obj_, event)


class FloatHandler(NullHandler):
    def handle(self, obj_, event):
        print("FloatHandler-handle")
        if event.type_ == 'float':
            if isinstance(event, EventGet):
                return obj_.float_field
            else:
                obj_.float_field = event.value
        else:
            return super().handle(obj_, event)


class StrHandler(NullHandler):
    def handle(self, obj_, event):
        print("StrHandler-handle")
        if event.type_ == 'str':
            if isinstance(event, EventGet):
                return obj_.string_field
            else:
                obj_.string_field = event.value
        else:
            return super().handle(obj_, event)


if __name__ == '__main__':
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    print(chain.handle(obj, EventGet(int)))
    # 42
    print(chain.handle(obj, EventGet(float)))
    # 3.14
    print(chain.handle(obj, EventGet(str)))
    # 'some text'
    chain.handle(obj, EventSet(100))
    print(chain.handle(obj, EventGet(int)))
    # 100
    chain.handle(obj, EventSet(0.5))
    print(chain.handle(obj, EventGet(float)))
    # 0.5
    chain.handle(obj, EventSet('new text'))
    print(chain.handle(obj, EventGet(str)))
    # 'new text'

