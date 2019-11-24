# Вам нужно написать адаптер, который позволил бы использовать найденный вами класс совместно с вашей системой.
#
# Интерфейс класса выглядит следующим образом:


# class Light:
#     def __init__(self, dim):
#         self.dim = dim
#         self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
#         self.lights = []
#         self.obstacles = []
#
#     def set_dim(self, dim):
#         self.dim = dim
#         self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
#
#     def set_lights(self, lights):
#         self.lights = lights
#         self.generate_lights()
#
#     def set_obstacles(self, obstacles):
#         self.obstacles = obstacles
#         self.generate_lights()
#
#     def generate_lights(self):
#         return self.grid.copy()
#
#
# # Интерфейс системы выглядит следующим образом:
#
#
# class System:
#     def __init__(self):
#         self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
#         self.map[5][7] = 1  # Источники света
#         self.map[15][9] = 1  # Источники света
#         self.map[19][20] = 1  # Источники света
#         self.map[5][2] = -1  # Стены
#         self.map[10][5] = -1  # Стены
#         self.map[0][4] = -1  # Стены
#
#     def get_lightening(self, light_mapper):
#         self.lightmap = light_mapper.lighten(self.map)


# Класс Light создает в методе __init__ поле заданного размера. За размер поля отвечает параметр, представляющий из
# себя кортеж из 2 чисел. Элемент dim[1] отвечает за высоту карты, dim[0] за ее ширину. Метод set_lights устанавливает
# массив источников света с заданными координатами и просчитывает освещение. Метод set_obstacles устанавливает
# препятствия аналогичным образом. Положение элементов задается списком кортежей. В каждом элементе кортежа хранятся
# 2 значения: elem[0] -- координата по ширине карты и elem[1] -- координата по высоте соответственно. Метод
# generate_lights рассчитывает освещенность с учетом источников и препятствий.

# В системе в конструкторе создается двухмерная, карта, на которой источники света обозначены как 1, а препятствия
# как -1. Метод get_lightening принимает в качестве аргумента объект, который должен высчитывать освещение. У
# объекта вызывается метод lighten, который принимает карту объектов и источников света и возвращает карту освещенности.
#
# Вам необходимо написать адаптер MappingAdapter. Прототип класса вам дан в качестве исходного кода.


class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    @staticmethod
    def find_object(x_int, map_grid):
        obj_list = []
        for y, elem in enumerate(map_grid):
            for x, target in enumerate(elem):
                if x_int == target:
                    obj_list.append((x, y))
        return obj_list

    def lighten(self, grid):
        dim_from_grid = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim_from_grid)
        lights_from_grid = self.find_object(1, grid)
        self.adaptee.set_lights(lights_from_grid)
        obstacles_from_grid = self.find_object(-1, grid)
        self.adaptee.set_obstacles(obstacles_from_grid)
        print(self.adaptee.dim, self.adaptee.lights, self.adaptee.obstacles)
        return self.adaptee.generate_lights()


# if __name__ == "__main__":
#
#     system = System()
#     print('\n'.join(str(elem) for elem in system.map))
#
#     dim = (30, 20)
#
#     light = Light(dim)
#
#     adapter = MappingAdapter(light)
#
#     system.get_lightening(adapter)
#
#     print('\n'.join(str(elem) for elem in system.lightmap))

