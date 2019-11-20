from abc import ABC, abstractmethod


class Creature(ABC):
    """
    Абстрактный базовый класс
    """

    @abstractmethod
    def feed(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def make_noise(self):
        pass


class Animal(Creature):
    """
    Класс Животное
    """

    def feed(self):
        print("I eat grass")

    def move(self):
        print("I walk forward")

    def make_noise(self):
        print("WOOOO!")


class AbstractDecorator(Creature):
    """
    Класс абстрактного декаратора
    """

    def __init__(self, base):
        self.base = base

    def move(self):
        self.base.move()

    def feed(self):
        self.base.feed()

    def make_noise(self):
        self.base.make_noise()


class Swimming(AbstractDecorator):
    """
    Конкретный декаратор 1 для водоплавующего
    """

    def move(self):
        print("I sweem forward")

    def make_noise(self):
        print("...")


class Predator(AbstractDecorator):
    def feed(self):
        print("I eat other animals")


class Fast(AbstractDecorator):
    def move(self):
        self.base.move()
        print("Fast!")


if __name__ == "__main__":

    animal = Animal()
    animal.move()
    animal.feed()
    animal.make_noise()
    print("-"*45)

    swimming = Swimming(animal)
    swimming.move()
    swimming.feed()
    swimming.make_noise()
    print("-" * 45)
    predator = Predator(swimming)
    predator.move()
    predator.feed()
    predator.make_noise()
    print("-" * 45)
    fast = Fast(predator)
    fast.move()
    fast.feed()
    fast.make_noise()
    fast2 = Fast(swimming)
    fast2.move()
    fast2.feed()
    fast2.make_noise()


