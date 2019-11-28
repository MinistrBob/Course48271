#!/usr/bin/env python3.6

from abc import ABC, abstractmethod


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
        self.value = value
        self.type = type(value)


class NullHandler(ABC):
    def __init__(self, successor=None):
        self.__successor = successor

    @abstractmethod
    def handle(self, obj, event):
        if self.__successor:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):

        if isinstance(event, EventGet):
            if event.type is int:
                return obj.integer_field
            else:
                return super().handle(obj, event)

        elif isinstance(event, EventSet):
            if event.type is int:
                obj.integer_field = event.value
            else:
                super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):

        if isinstance(event, EventGet):
            if event.type is float:
                return obj.float_field
            else:
                return super().handle(obj, event)

        elif isinstance(event, EventSet):
            if event.type is float:
                obj.float_field = event.value
            else:
                super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):

        if isinstance(event, EventGet):
            if event.type is str:
                return obj.string_field
            else:
                return super().handle(obj, event)

        elif isinstance(event, EventSet):
            if event.type is str:
                obj.string_field = event.value
            else:
                super().handle(obj, event)

