class SomeObject:
    def __init__(self):
        self.integer_field = 6
        self.float_field = 0.0
        self.string_field = "99"


class EventGet:
    def __init__(self, match):
        self.match = 'GET_' + str(match.__name__).upper()
        # print(self.match)


class EventSet:
    def __init__(self, match):
        self.match = 'SET_' + str(type(match).__name__).upper()
        self.value = match
        # print(self.match)


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):  # обработчик
        if self.__successor is not None:  # даём следующему
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.match == 'GET_INT':
            # print('Int handler - get:', obj.integer_field)
            return obj.integer_field
        if event.match == 'SET_INT':
            # print('Int handler - set:', event.value)
            obj.integer_field = event.value
        else:
            # print('pass to another')
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.match == 'GET_FLOAT':
            # print('float handler - get:', obj.float_field)
            return obj.float_field
        if event.match == 'SET_FLOAT':
            # print('Float handler - set:', event.value)
            obj.float_field = event.value
        else:
            # print('pass to another')
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.match == 'GET_STR':
            # print('Str handler - get:', obj.string_field)
            return obj.string_field
        if event.match == 'SET_STR':
            # print('Str handler - set:', event.value)
            obj.string_field = event.value
        else:
            # print('pass to another')
            return super().handle(obj, event)


if __name__ == '__main__':
    obj = SomeObject()
    chain = IntHandler(FloatHandler(StrHandler(NullHandler())))

    print(obj.integer_field, obj.float_field, obj.string_field)

    print(chain.handle(obj, EventGet(str)))
    print(chain.handle(obj, EventGet(int)))
    print(chain.handle(obj, EventGet(float)))
    chain.handle(obj, EventSet(1))
    chain.handle(obj, EventSet(1.1))
    chain.handle(obj, EventSet('Hooray'))

    print(obj.integer_field, obj.float_field, obj.string_field)