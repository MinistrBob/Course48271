# =============================================================================
# Скрипт для тестирования решений студентов по заданию "Создание декоратора
# класса" (тесты содержат примеры, приведенные в описании задания)
# https://stepik.org/lesson/106937/step/4?unit=81460
# Скопируйте код вашего решения в секцию ВАШ КОД и запустите скрипт
# =============================================================================
from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        print("Hero.__init__")
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        print("Hero.get_positive_effects")
        return self.positive_effects.copy()

    def get_negative_effects(self):
        print("Hero.get_negative_effects")
        return self.negative_effects.copy()

    def get_stats(self):
        print("Hero.get_stats")
        return self.stats.copy()


# =============================================================================
# начало секции ВАШ КОД
# =============================================================================
class AbstractEffect(ABC, Hero):

    def __init__(self, base):
        print("AbstractEffect.__init__")
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        print("AbstractEffect.@@@get_positive_effects")
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        print("AbstractEffect.@@@get_negative_effects")
        return self.base.get_negative_effects()

    @abstractmethod
    def get_stats(self):
        print("AbstractEffect.@@@get_stats")
        return self.base.get_stats()


class AbstractPositive(AbstractEffect):
    def __init__(self, base):
        print("AbstractPositive.__init__")
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        print("AbstractPositive.@@@get_positive_effects")
        pass

    def get_negative_effects(self):
        print("AbstractPositive.get_negative_effects")
        return self.base.get_negative_effects()

    def get_stats(self):
        print("AbstractPositive.get_stats")
        return self.base.get_stats()


class AbstractNegative(AbstractEffect):
    def __init__(self, base):
        print("AbstractNegative.__init__")
        self.base = base

    def get_positive_effects(self):
        print("AbstractNegative.get_positive_effects")
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        print("AbstractNegative.@@@get_negative_effects")
        pass

    def get_stats(self):
        print("AbstractNegative.get_stats")
        return self.base.get_stats()


class Berserk(AbstractPositive):

    def get_positive_effects(self):
        print("Berserk.get_positive_effects")
        self.positive_effects = self.base.get_positive_effects()
        self.positive_effects.append("Berserk")
        return self.positive_effects

    def get_stats(self):
        print("Berserk.get_stats")
        self.stats = self.base.get_stats()
        self.stats["HP"] += 50
        self.stats["Strength"] += 7
        self.stats["Perception"] -= 3
        self.stats["Endurance"] += 7
        self.stats["Charisma"] -= 3
        self.stats["Intelligence"] -= 3
        self.stats["Agility"] += 7
        self.stats["Luck"] += 7
        return self.stats


class Blessing(AbstractPositive):

    def get_positive_effects(self):
        self.positive_effects = self.base.get_positive_effects()
        self.positive_effects.append("Blessing")
        return self.positive_effects

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Strength"] += 2
        self.stats["Perception"] += 2
        self.stats["Endurance"] += 2
        self.stats["Charisma"] += 2
        self.stats["Intelligence"] += 2
        self.stats["Agility"] += 2
        self.stats["Luck"] += 2
        return self.stats


class Weakness(AbstractNegative):
    def get_negative_effects(self):
        self.negative_effects = self.base.get_negative_effects()
        self.negative_effects.append("Weakness")
        return self.negative_effects

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Strength"] -= 4
        self.stats["Endurance"] -= 4
        self.stats["Agility"] -= 4
        return self.stats


class Curse(AbstractNegative):

    def get_negative_effects(self):
        print("Curse.get_negative_effects")
        self.negative_effects = self.base.get_negative_effects()
        self.negative_effects.append("Curse")
        return self.negative_effects

    def get_stats(self):
        print("Curse.get_stats")
        self.stats = self.base.get_stats()
        self.stats["Strength"] -= 2
        self.stats["Perception"] -= 2
        self.stats["Endurance"] -= 2
        self.stats["Charisma"] -= 2
        self.stats["Intelligence"] -= 2
        self.stats["Agility"] -= 2
        self.stats["Luck"] -= 2
        return self.stats


class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        self.negative_effects = self.base.get_negative_effects()
        self.negative_effects.append("EvilEye")
        return self.negative_effects

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Luck"] -= 10
        return self.stats


# =============================================================================
# конец секции ВАШ КОД
# =============================================================================

if __name__ == '__main__':
    # создадим героя
    hero = Hero()
    # проверим правильность характеристик по-умолчанию
    print("Create - hero")
    print(hero.stats)
    assert hero.get_stats() == {'HP': 128,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 15,
                                'Perception': 4,
                                'Endurance': 8,
                                'Charisma': 2,
                                'Intelligence': 3,
                                'Agility': 8,
                                'Luck': 1}
    # проверим список отрицательных эффектов
    print(hero.negative_effects)
    assert hero.get_negative_effects() == []
    # проверим список положительных эффектов
    print(hero.positive_effects)
    assert hero.get_positive_effects() == []
    print("=" * 60)
    # наложим эффект Berserk
    print("# наложим эффект Berserk")
    print("brs1 = Berserk(hero)")
    brs1 = Berserk(hero)
    # проверим правильность изменения характеристик
    assert brs1.get_stats() == {'HP': 178,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 22,
                                'Perception': 1,
                                'Endurance': 15,
                                'Charisma': -1,
                                'Intelligence': 0,
                                'Agility': 15,
                                'Luck': 8}
    # проверим неизменность списка отрицательных эффектов
    assert brs1.get_negative_effects() == []
    # проверим, что в список положительных эффектов был добавлен Berserk
    assert brs1.get_positive_effects() == ['Berserk']
    print(brs1.get_stats())
    print(brs1.get_negative_effects())
    print(brs1.get_positive_effects())
    print("=" * 60)
    # повторное наложение эффекта Berserk
    print("# повторное наложение эффекта Berserk")
    print("brs2 = Berserk(brs1)")
    brs2 = Berserk(brs1)
    print(brs2.get_stats())
    print(brs2.get_negative_effects())
    print(brs2.get_positive_effects())
    print("=" * 60)
    # наложение эффекта Curse
    print("# наложение эффекта Curse")
    print("cur1 = Curse(brs2)")
    cur1 = Curse(brs2)
    print(cur1.get_stats())
    print(cur1.get_negative_effects())
    print(cur1.get_positive_effects())
    print("=" * 60)
    # проверим правильность изменения характеристик
    assert cur1.get_stats() == {'HP': 228,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 27,
                                'Perception': -4,
                                'Endurance': 20,
                                'Charisma': -6,
                                'Intelligence': -5,
                                'Agility': 20,
                                'Luck': 13}
    # проверим правильность добавления эффектов в список положительных эффектов
    assert cur1.get_positive_effects() == ['Berserk', 'Berserk']
    # проверим правильность добавления эффектов в список отрицательных эффектов
    assert cur1.get_negative_effects() == ['Curse']
    # снятие эффекта Berserk
    cur1.base = brs1
    # проверим правильность изменения характеристик
    assert cur1.get_stats() == {'HP': 178,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 20,
                                'Perception': -1,
                                'Endurance': 13,
                                'Charisma': -3,
                                'Intelligence': -2,
                                'Agility': 13,
                                'Luck': 6}
    # проверим правильность удаления эффектов из списка положительных эффектов
    assert cur1.get_positive_effects() == ['Berserk']
    # проверим правильность эффектов в списке отрицательных эффектов
    assert cur1.get_negative_effects() == ['Curse']
    # проверим незменность характеристик у объекта hero
    assert hero.get_stats() == {'HP': 128,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 15,
                                'Perception': 4,
                                'Endurance': 8,
                                'Charisma': 2,
                                'Intelligence': 3,
                                'Agility': 8,
                                'Luck': 1}
    print('All tests - OK!')
