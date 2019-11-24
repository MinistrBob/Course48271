class Light:
    def __init__(self, dim):
        """
        Класс Light создает в методе __init__ поле заданного размера.
        За размер поля отвечает параметр, представляющий из себя кортеж из 2 чисел.
        Элемент dim[1] отвечает за высоту карты, dim[0] за ее ширину.
        :param dim:
        """
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        """
        Метод set_lights устанавливает массив источников света с заданными координатами
        и просчитывает освещение.
        :param lights:
        :return:
        """
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        """
        Метод set_obstacles устанавливает препятствия аналогичным образом.
        Положение элементов задается списком кортежей.
        В каждом элементе кортежа хранятся 2 значения:
        elem[0] -- координата по ширине карты и
        elem[1] -- координата по высоте соответственно.
        :param obstacles:
        :return:
        """
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


# --------------------------------------------------------------------------
class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        self.adaptee.set_dim((len(grid[0]), len(grid)))
        lights = []
        obstacles = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] > 0:
                    # lights.append((i, j))
                    lights.append((j, i))
                if grid[i][j] < 0:
                    # obstacles.append((i, j))
                    obstacles.append((j, i))
        self.adaptee.set_obstacles(obstacles)
        self.adaptee.set_lights(lights)
        print(self.adaptee.lights)
        print(self.adaptee.obstacles)
        return self.adaptee.generate_lights()


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    s = System()
    print(s.map)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in s.map]))
    print("-"*60)

    lmap = Light((len(s.map[0]), len(s.map)))
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in lmap.grid]))
    print(type(lmap))
    print(lmap)
    print(id(lmap))

    ma = MappingAdapter(lmap)
    print(ma)
    print(type(ma.adaptee))
    print(ma.adaptee)
    print(id(ma.adaptee))

    s.get_lightening(ma)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in s.lightmap]))
