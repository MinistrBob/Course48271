from abc import ABC, abstractmethod


class Engine:
    pass


class ObservableEngine(Engine):
    pass


class AbstractObserver(ABC):
    pass


class ShortNotificationPrinter(AbstractObserver):
    pass


class FullNotificationPrinter(AbstractObserver):
    pass


if __name__ == "__main__":
    pass
