import random
import yaml
from abc import ABC


class AbstractLevel(yaml.YAMLObject):

    @classmethod
    def get_map(cls):
        return cls.Map()

    @classmethod
    def get_objects(cls):
        return cls.Objects()

    @classmethod
    def from_yaml(cls, loader, node):  # <-- добавим метод класса from_yaml
        # получаем данные из yaml
        value = loader.construct_mapping(node)
        # необходимо выбрать из полученные данных необходимые
        # для создания экземпляра класса ExampleClass
        _map = cls.Map()
        _obj = cls.Objects()
        _obj.config = value
        res = {'map': _map, 'obj': _obj}
        return res

    class Map(ABC):
        pass

    class Objects(ABC):
        pass


class EasyLevel(AbstractLevel):
    yaml_tag = '!easy_level'

    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(5)] for _ in range(5)]
            for i in range(5):
                for j in range(5):
                    if i == 0 or j == 0 or i == 4 or j == 4:
                        self.Map[j][i] = -1  # граница карты
                    else:
                        self.Map[j][i] = random.randint(0, 2)  # случайная характеристика области

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = [('next_lvl', (2, 2))]
            self.config = {}

        def get_objects(self, _map):
            for obj_name in ['rat']:
                coord = (random.randint(1, 3), random.randint(1, 3))
                intersect = True
                while intersect:
                    intersect = False
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(1, 3), random.randint(1, 3))

                self.objects.append((obj_name, coord))

            return self.objects


class MediumLevel(AbstractLevel):
    yaml_tag = '!medium_level'

    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(8)] for _ in range(8)]
            for i in range(8):
                for j in range(8):
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        self.Map[j][i] = -1  # граница карты
                    else:
                        self.Map[j][i] = random.randint(0, 2)  # случайная характеристика области

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = [('next_lvl', (4, 4))]
            self.config = {'enemy': []}

        def get_objects(self, _map):
            for obj_name in self.config['enemy']:
                coord = (random.randint(1, 6), random.randint(1, 6))
                intersect = True
                while intersect:
                    intersect = False
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(1, 6), random.randint(1, 6))

                self.objects.append((obj_name, coord))

            return self.objects


class HardLevel(AbstractLevel):
    yaml_tag = '!hard_level'

    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(10)] for _ in range(10)]
            for i in range(10):
                for j in range(10):
                    if i == 0 or j == 0 or i == 9 or j == 9:
                        self.Map[j][i] = -1  # граница карты :: непроходимый участок карты
                    else:
                        self.Map[j][i] = random.randint(-1, 8)  # случайная характеристика области

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = [('next_lvl', (5, 5))]
            self.config = {'enemy_count': 5, 'enemy': []}

        def get_objects(self, _map):
            for obj_name in self.config['enemy']:
                for tmp_int in range(self.config['enemy_count']):
                    coord = (random.randint(1, 8), random.randint(1, 8))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[0]][coord[1]] == -1:
                            intersect = True
                            coord = (random.randint(1, 8), random.randint(1, 8))
                            continue
                        for obj in self.objects:
                            if coord == obj[1]:
                                intersect = True
                                coord = (random.randint(1, 8), random.randint(1, 8))

                    self.objects.append((obj_name, coord))

            return self.objects


if __name__ == '__main__':
    from pprint import pprint
    # ###################
    # #      Код 2      #
    # ###################
    # Levels = {'levels': []}
    # _map = EasyLevel.Map()
    # _obj = EasyLevel.Objects()
    # Levels['levels'].append({'map': _map, 'obj': _obj})
    #
    # _map = MediumLevel.Map()
    # _obj = MediumLevel.Objects()
    # _obj.config = {'enemy': ['rat']}
    # Levels['levels'].append({'map': _map, 'obj': _obj})
    #
    # _map = HardLevel.Map()
    # _obj = HardLevel.Objects()
    # _obj.config = {'enemy': ['rat', 'snake', 'dragon'],
    #                'enemy_count': 10}
    # Levels['levels'].append({'map': _map, 'obj': _obj})
    #
    # pprint(Levels)

    # {'levels':
    #      [{'map': <__main__.EasyLevel.Map object at 0x0000000002D15288>, 'obj': <__main__.EasyLevel.Objects object at 0x0000000002D15448>},
    #       {'map': <__main__.MediumLevel.Map object at 0x0000000002D15488>, 'obj': <__main__.MediumLevel.Objects object at 0x0000000002D15708>},
    #       {'map': <__main__.HardLevel.Map object at 0x0000000002D15748>, 'obj': <__main__.HardLevel.Objects object at 0x0000000002D15788>}
    #      ]
    # }

    ###################
    #      Код 1      #
    ###################
    Levels = yaml.load(
        '''
        levels:
            - !easy_level {}
            - !medium_level
                enemy: ['rat']
            - !hard_level
                enemy:
                    - rat
                    - snake
                    - dragon
                enemy_count: 10
        ''')

    pprint(Levels)
