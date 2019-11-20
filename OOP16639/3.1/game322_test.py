from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(ABC, Hero):

    def __init__(self, base):
        self.base = base
        self.positive_effects = base.get_positive_effects()
        self.negative_effects = base.get_negative_effects()
        self.stats = base.get_stats()

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_positive_effects(self):
        pass

    def get_negative_effects(self):
        return self.negative_effects

    def get_stats(self):
        return self.stats


class AbstractNegative(AbstractEffect):
    def get_positive_effects(self):
        return self.positive_effects

    @abstractmethod
    def get_negative_effects(self):
        pass

    def get_stats(self):
        return self.stats


class Berserk(AbstractPositive):
    def get_positive_effects(self):
        self.positive_effects.append("Berserk")
        return self.positive_effects

    def get_stats(self):
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
        self.positive_effects.append("Blessing")
        return self.positive_effects

    def get_stats(self):
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
        self.negative_effects.append("Weakness")
        return self.negative_effects

    def get_stats(self):
        self.stats["Strength"] -= 4
        self.stats["Endurance"] -= 4
        self.stats["Agility"] -= 4
        return self.stats


class Curse(AbstractNegative):
    def get_negative_effects(self):
        self.negative_effects.append("Curse")
        return self.negative_effects

    def get_stats(self):
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
        self.negative_effects.append("EvilEye")
        return self.negative_effects

    def get_stats(self):
        self.stats["Luck"] -= 10
        return self.stats


if __name__ == "__main__":
    h = Hero()
    print(f"Это: {type(h).__name__}")
    print(h.get_positive_effects())
    print(h.get_negative_effects())
    print(h.get_stats())
    print("-" * 45)

    h1 = Blessing(h)
    print(f"Это: {type(h1).__name__}")
    print(h1.get_positive_effects())
    print(h1.get_negative_effects())
    print(h1.get_stats())
