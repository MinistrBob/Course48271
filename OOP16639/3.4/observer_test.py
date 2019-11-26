from abc import ABC, abstractmethod


class Engine:
    pass


class ObservableEngine(Engine):
    def __init__(self):
        self.subscribers = set()
        self.atches = [{"title": "Покоритель1", "text": "Дается при выполнении всех заданий в игре"},
                       {"title": "Покоритель3", "text": "Дается при выполнении всех заданий в игре"},
                       {"title": "Покоритель3", "text": "Дается при выполнении всех заданий в игре"},
                       {"title": "Покоритель4", "text": "Дается при выполнении всех заданий в игре"},
                       {"title": "Покоритель5", "text": "Дается при выполнении всех заданий в игре"}]

    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)

    def run(self):
        for a in self.atches:
            self.notify(a)

class AbstractObserver(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def update(self, message):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self, name):
        super().__init__(name)
        self.achievements = set()

    def update(self, message):
        self.achievements.add(message["title"])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self, name):
        super().__init__(name)
        self.achievements = list()

    def update(self, message):
        if message not in self.achievements:
            self.achievements.append(message)


if __name__ == "__main__":
    eng = ObservableEngine()
    s = ShortNotificationPrinter("short")
    f = FullNotificationPrinter("full")

    eng.subscribe(s)
    eng.subscribe(f)

    eng.run()

    print(eng)
    print(s.achievements)
    print(f.achievements)

