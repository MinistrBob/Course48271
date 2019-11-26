# from abc import ABC, abstractmethod
#
#
# class Engine(ABC):
#     pass


class ObservableEngine(Engine):  # Наблюдаемая система
    def __init__(self):
        self.__subscribers = set()  # При инициализации множество подписчиков звдвется пустым

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)  # Для того чтобы подписать пользователя, он добавляется
        # print(self.__subscribers)
        # во множество подписчиков

    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)  # Удаление подписчика из списка
        # print(self.__subscribers)

    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)  # Отправка уведомления всем подписчикам
            # {"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"}


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, message):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, message):
        if isinstance(message, dict):
            dic = message
        if isinstance(message, str):
            dic = eval(message)
        self.achievements.add(dic['title'])
        # print(self.achievements)  # get rid of at give in


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, message):
        if isinstance(message, dict):
            dic = message
        if isinstance(message, str):
            dic = eval(message)
        if dic not in self.achievements:
            self.achievements.append(dic)
        # print(self.achievements)  # get rid of at give in


if __name__ == '__main__':

    engine = ObservableEngine()
    short = ShortNotificationPrinter()
    full = FullNotificationPrinter()
    full2 = FullNotificationPrinter()

    engine.subscribe(short)
    engine.subscribe(full)
    engine.subscribe(full2)

    engine.notify('{"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"}')
    engine.notify('{"title": "Повелитель", "text": "Дается при нагибании всех боссов"}')
    engine.notify('{"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"}')
    engine.notify('{"title": "Умняша"}')
    engine.notify({"title": "Лорд земель", "text": "Дается при захвате каждой земли"})

    engine.unsubscribe(full)

