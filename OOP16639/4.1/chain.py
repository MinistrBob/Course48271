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
