class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, type):
        self.type = type


class EventSet:
    def __init__(self, value):
        self.type = type(value)
        self.value = value


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.type.__name__ == 'str':
            if isinstance(event, EventGet):
                return obj.string_field
            else:
                obj.string_field = event.value
        else:
            print("StrHandler Передаю событие дальше")
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.type.__name__ == 'float':
            if isinstance(event, EventGet):
                return obj.float_field
            else:
                obj.float_field = event.value
        else:
            print("FloatHandler Передаю событие дальше")
            return super().handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.type.__name__ == 'int':
            if isinstance(event, EventGet):
                return obj.integer_field
            else:
                obj.integer_field = event.value
        else:
            print("IntHandler Передаю событие дальше")
            return super().handle(obj, event)
