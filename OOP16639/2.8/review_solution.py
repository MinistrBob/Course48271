import pygame
import random
import math
import copy


class Vec2d:
    """Класс 2-мерных векторов"""

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __sub__(self, other):
        """Разность векторов"""
        return Vec2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """Сложение векторов"""
        return Vec2d(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __len__(self):
        """Длина вектора"""
        return int(math.hypot(self.y, self.y))

    def __mul__(self, other):
        """Умножение вектора на число / скалярное произведение векторов

        :return: вектор / число
        """
        if isinstance(other, (int, float)):
            return Vec2d(self.x * other, self.y * other)
        return sum(self.x * other.x, self.y * other.y)

    @classmethod
    def vec(cls, a, b):
        """Создание вектора по началу (x) и концу (y) направленного отрезка"""
        return cls(b[0] - a[0], b[1] - a[1])

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    """Класс ломаной линии"""

    # Величина приращения скорости
    SPEED_SHIFT = 0.5

    def __init__(self, context):
        self._points = []
        self._shifts = []
        self._speed = 1
        self._context = context

    @property
    def speed(self):
        return self._speed

    @property
    def points_count(self):
        return len(self._points)

    def add_point(self, position):
        """Добавление в ломаную новой опорной точки и соответствующую ей величину смещения координаты

        :param position: кортеж координат точки
        """
        self._points.append(Vec2d(*position))
        self._shifts.append(Vec2d(random.random(), random.random()))

    def delete_point(self):
        """Удаление из ломаной последней добавленной опорной точки"""
        if self._points:
            self._points.pop()
            self._shifts.pop()

    def set_points(self):
        """Персчет координат опорных точек"""
        for i, p in enumerate(self._points):
            p += (self._shifts[i] * self._speed)
            if p.x > self._context.display.get_surface().get_width() or p.x < 0:
                self._shifts[i].x *= -1
            if p.y > self._context.display.get_surface().get_height() or p.y < 0:
                self._shifts[i].y *= -1
            self._points[i] = p

    def increment_speed(self):
        self._speed += self.SPEED_SHIFT

    def decrement_speed(self):
        if self._speed > self.SPEED_SHIFT:
            self._speed -= self.SPEED_SHIFT

    def _draw(self, style, pts, width, color):
        """Служебный метод отрисовки точек и линий

        :param style: point / line - отрисовка точки / линии
        :param pts: массив точек
        :param width: радиус / ширина
        :param color: цвет окружности / линии
        """
        screen = self._context.display.get_surface()
        if style == "point":
            for p in self._points:
                # В случае отрисовки точек width - это радиус круга с центром в отображаемой точке
                # Ширина окружности круга в методе circle по умолчанию равна 0,
                # поэтому ширина окружности будет равна радиусу круга.
                # Следовательно круг будет закрашен полностью.
                self._context.draw.circle(screen, color, (int(p.x), int(p.y)), width)
        elif style == "line":
            for p_n in range(-1, len(pts) - 1):
                self._context.draw.line(screen, color, (int(pts[p_n].x), int(pts[p_n].y)),
                                        (int(pts[p_n + 1].x), int(pts[p_n + 1].y)), width)

    def draw_points(self, radius=3, color=(255, 255, 255)):
        """Отрисовка опорных точек

        :param radius: radius круга с центром в отображаемой точке
        :param color: цвет окружности
        """
        self._draw("point", self._points, radius, color)

    def draw_line(self, width=3, color=(255, 255, 255)):
        """Отрисовка ломаной линии

        :param width: ширина линии
        :param color: цвет линии
        """
        self._draw("line", self._points, width, color)


class Knot(Polyline):
    """Класс ломаной сглаженной линии (кривой)"""

    def __init__(self, context, steps):
        """Инициализация

        :param context: инициализированный pygame
        :param steps: количество точек сглаживания ломаной линии
        """
        super().__init__(context)
        self._curve_points = []
        self.__steps = steps

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, value):
        if value >= 1:
            self.__steps = value
            self._set_knots()

    def add_point(self, point):
        super().add_point(point)
        self._set_knots()

    def delete_point(self):
        super().delete_point()
        self._set_knots()

    def set_points(self):
        """Персчитывание координат опорных точек"""
        super().set_points()
        self._set_knots()

    def draw_curve(self, width=3, color=(255, 255, 255)):
        """Отрисовка кривой

        :param width: ширина линии
        :param color: цвет линии
        """
        self._draw("line", self._curve_points, width, color)

    def __copy__(self):
        copy_line = type(self)(self._context, self.steps)
        copy_line.__dict__.update(self.__dict__)
        copy_line._points, copy_line._shifts = [], []
        screen = self._context.display.get_surface()
        for _ in range(len(self._points)):
            copy_line._points.append(Vec2d(random.randint(0, screen.get_width()),
                                           random.randint(0, screen.get_height())))
            copy_line._shifts.append(Vec2d(random.random(), random.random()))
        copy_line._set_knots()
        return copy_line

    def create_from_existing(self):
        return copy.copy(self)

    @staticmethod
    def _get_point(points, alpha):
        pt = points[0]
        for i in range(1, len(points)):
            pt = points[i] * alpha + pt * (1 - alpha)
        return pt

    def _get_points(self, base_points):
        alpha = 1 / self.__steps
        return [self._get_point(base_points, i * alpha) for i in range(self.steps)]

    def _set_knots(self):
        """Сглаживание ломаной - вычисление массива точек кривой на основе имеющихся опорных точек"""
        self._curve_points = []
        if len(self._points) >= 3:
            for i in range(-2, len(self._points) - 2):
                pts = [(self._points[i] + self._points[i + 1]) * 0.5, self._points[i + 1],
                       (self._points[i + 1] + self._points[i + 2]) * 0.5]
                self._curve_points.extend(self._get_points(pts))


class LineCollection:
    """Коллекция линий"""

    def __init__(self, line):
        self._lines = [line]

    def get_lines(self):
        return self._lines

    def _get_random_line(self):
        idx = random.randint(0, len(self._lines) - 1)
        return self._lines[idx]

    def add_line(self):
        """Добавить в коллекцию новую линию
        Новая линия копирует состояние (скорость, количество точек) последней в коллекции
        Ограничение: 16 линий
        """
        if self._lines and len(self._lines) < 16:
            self._lines.append(self._lines[-1].create_from_existing())

    def delete_line(self):
        """Удалить из коллекции последнюю добавленную линию"""
        if len(self._lines) > 1:
            self._lines.pop()

    def add_point(self, position, is_shift):
        """Добавить точку в произвольную или во все линии

        :param position: кортеж координат точки
        :param is_shift: удерживается клавиша SHIFT
        """
        if is_shift:
            self._get_random_line().add_point(position)
        else:
            for line in self._lines:
                line.add_point(position)

    def delete_point(self, is_shift):
        """Удалить последнюю добавленную точку из произвольной или всех линий"""
        if is_shift:
            self._get_random_line().delete_point()
        else:
            for line in self._lines:
                line.delete_point()

    def set_points(self):
        """Пересчет координат опорных точек для всех линий"""
        for line in self._lines:
            line.set_points()

    def update_steps(self, steps):
        """Изменение количества точек сглаживания для всех линий"""
        for line in self._lines:
            line.steps = steps

    def increment_speed(self, is_shift):
        """Увеличение скорости произвольной или всех линий"""
        if is_shift:
            self._get_random_line().increment_speed()
        else:
            for line in self._lines:
                line.increment_speed()

    def decrement_speed(self, is_shift):
        """Уменьшение скорости произвольной или всех линий"""
        if is_shift:
            self._get_random_line().decrement_speed()
        else:
            for line in self._lines:
                line.decrement_speed()

    def draw_points(self):
        """Отрисовка опорных точек всех линий"""
        for line in self._lines:
            line.draw_points()

    def draw_curve(self, width, color):
        """Отрисовка всех (сглаженных) линий"""
        for i, line in enumerate(self._lines):
            line.draw_curve(width, color)


class ScreenSaver:
    """Класс экранной заставки"""

    def __init__(self, caption, screen_dim=(800, 600), steps=35):
        """Инициализация заставки

        :param caption: заголовок окна
        :param screen_dim: размер окна
        :param steps: количество точек сглаживания ломаной линии
        """
        self.steps = steps

        pygame.init()
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode(screen_dim)
        self.font1 = pygame.font.SysFont("courier", 24)
        self.font2 = pygame.font.SysFont("serif", 24)

    def start(self):
        """Основной метод управляющий заставкой"""
        working = True
        show_help = False
        show_info = False
        pause = True

        hue = 0
        color = pygame.Color(0)
        color.hsla = (hue, 100, 50, 100)

        collection = LineCollection(Knot(pygame, self.steps))

        while working:
            # Обработка очереди событий
            for event in pygame.event.get():
                mods = pygame.key.get_mods()
                is_shift = (mods == pygame.KMOD_SHIFT or
                            mods == pygame.KMOD_LSHIFT or
                            mods == pygame.KMOD_RSHIFT)
                if event.type == pygame.QUIT:
                    working = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    collection.add_point(event.pos, is_shift)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        working = False
                    elif event.key == pygame.K_F1:
                        show_help = not show_help
                    elif event.key == pygame.K_F2:
                        show_info = not show_info
                    elif event.key == pygame.K_r:
                        pause = True
                        collection = LineCollection(Knot(pygame, self.steps))
                    elif event.key == pygame.K_p:
                        pause = not pause
                    elif event.key == pygame.K_a:
                        collection.add_point((random.randint(0, self.screen.get_width()),
                                              random.randint(0, self.screen.get_height())), is_shift)
                    elif event.key == pygame.K_d:
                        collection.delete_point(is_shift)
                    elif event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                        collection.update_steps(self.steps)
                    elif event.key == pygame.K_KP_MINUS:
                        if self.steps > 1:
                            self.steps -= 1
                        collection.update_steps(self.steps)
                    elif event.key == pygame.K_PAGEUP:
                        collection.increment_speed(is_shift)
                    elif event.key == pygame.K_PAGEDOWN:
                        collection.decrement_speed(is_shift)
                    elif event.key == pygame.K_INSERT:
                        collection.add_line()
                    elif event.key == pygame.K_DELETE:
                        collection.delete_line()

            if pause:
                self.screen.fill((70, 70, 70))
                self.screen.blit(self.font1.render(
                    "Pause", True, (128, 128, 255)), (100, 100))
                collection.draw_points()
            else:
                hue = (hue + 1) % 360
                color.hsla = (hue, 100, 50, 100)
                self.screen.fill((0, 0, 0))
                collection.set_points()

            collection.draw_curve(3, color)

            if show_help:
                self.draw_help()
            if show_info:
                self.draw_info(collection)

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()

    def draw_help(self):
        """Отображение справки"""
        self.screen.fill((50, 50, 50))
        left_col_margin, right_col_margin, top_margin = 100, 200, 100
        # Высота строки
        line_height = 30
        data = [["F1", "Show Help"],
                ["F2", "Show Info"],
                ["R", "Restart"],
                ["P", "Pause/Play"],
                ["INS", "Add another curve"],
                ["DEL", "Delete last curve"],
                ["Num+", "More smoothing points"],
                ["Num-", "Less smoothing points"],
                ["A", "More base points"],
                ["D", "Less base points"],
                ["PgUp", "Increase curves speed"],
                ["PgDn", "Decrease curves speed"],
                ["SHIFT", "[Click, A, D, PgUp, PgDn] for random curve"],
                ]

        pygame.draw.lines(self.screen, (255, 50, 50, 255), True, [
            (0, 0), (self.screen.get_width(), 0),
            (self.screen.get_width(), self.screen.get_height()),
            (0, self.screen.get_height())], 5)
        for i, text in enumerate(data):
            self.screen.blit(self.font1.render(
                text[0], True, (128, 128, 255)), (left_col_margin, top_margin + line_height * i))
            self.screen.blit(self.font2.render(
                text[1], True, (128, 128, 255)), (right_col_margin, top_margin + line_height * i))

    def draw_info(self, collection):
        """Отображение информации по созданным линиям"""
        self.screen.fill((50, 50, 50))
        left_col_margin, right_col_margin, top_margin = 100, 200, 100
        # Высота строки
        line_height = 30
        pygame.draw.lines(self.screen, (255, 50, 50, 255), True, [
            (0, 0), (self.screen.get_width(), 0),
            (self.screen.get_width(), self.screen.get_height()),
            (0, self.screen.get_height())], 5)
        self.screen.blit(self.font1.render(
            "Curves", True, (128, 128, 255)), (left_col_margin, top_margin))
        self.screen.blit(self.font2.render(
            f"Num of smoothing points: {self.steps}",
            True, (128, 128, 255)), (right_col_margin, top_margin))
        for i, line in enumerate(collection.get_lines()):
            self.screen.blit(self.font1.render(
                f"#{i + 1:02}", True, (128, 128, 255)), (left_col_margin, top_margin + line_height * (i + 1)))
            self.screen.blit(self.font2.render(
                "Num of base points: {:>2d}   speed: {}".format(line.points_count, line.speed),
                True, (128, 128, 255)), (right_col_margin, top_margin + line_height * (i + 1)))


# Основная программа
if __name__ == "__main__":
    ScreenSaver("MyScreenSaver", steps=35).start()
