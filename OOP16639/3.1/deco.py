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
