import pygame
import random
import time

SCREEN_DIM = (800, 600)

class Vec2d:

    def __init__(self, point):
        if not isinstance(point, tuple): raise ValueError
        if not isinstance(point[0], (int, float)): raise ValueError
        if not isinstance(point[1], (int, float)): raise ValueError
        self.x = point[0]
        self.y = point[1]

    def __add__(self, self2):  # сумма двух векторов
        if not isinstance(self2, Vec2d): raise ValueError
        return Vec2d((self.x + self2.x, self.y + self2.y))

    def __sub__(self, self2):  # разность двух векторов
        if not isinstance(self2, Vec2d): raise ValueError
        return Vec2d((self.x - self2.x, self.y - self2.y))

    def __mul__(self, k):  # умножение вектора на число
        if not isinstance(k, (int, float)): raise ValueError
        return Vec2d((self.x * k, self.y * k))

    def __len__(self):  # длинна вектора
        return int((self.x * self.x + self.y * self.y) ** 0.5)

    def int_pair(self):
        return (int(self.x), int(self.y))


class Polyline:

    def __init__(self):
        self._points = []
        self._speeds = []
        self._hue = 0
        self._color = pygame.Color(0)


    def add_point(self, vector):
        if not isinstance(vector, Vec2d): raise ValueError
        self._points.append(vector)
        self._speeds.append((random.random() * 2, random.random() * 2))

    def set_points(self):  # Персчитывание координат опорных точек
        points = self._points
        speeds = self._speeds
        for p in range(len(points)):
            points[p] = points[p] + Vec2d(speeds[p])
            if points[p].x > SCREEN_DIM[0] or points[p].x < 0:
                speeds[p] = (- speeds[p][0], speeds[p][1])
            if points[p].y > SCREEN_DIM[1] or points[p].y < 0:
                speeds[p] = (speeds[p][0], -speeds[p][1])

    def draw_points(self, count=5, width=3):  # "Отрисовка" точек
        def get_knot():  # Сглаживание ломаной
            def get_points(base_points):  # Сглаживание ломаной
                def get_point(points=None, alpha=None, deg=None):  # Сглаживание ломаной
                    if points is None: points = self._points
                    if deg is None:
                        deg = len(points) - 1
                    if deg == 0:
                        return points[0]
                    return points[deg] * alpha + get_point(points, alpha, deg - 1) * (1 - alpha)

                return [get_point(base_points, i / count) for i in range(count)]

            if len(self._points) < 3: return []
            res = []
            for i in range(-2, len(self._points) - 2):
                ptn = []
                ptn.append((self._points[i] + self._points[i + 1]) * 0.5)
                ptn.append(self._points[i + 1])
                ptn.append((self._points[i + 1] + self._points[i + 2]) * 0.5)
                res.extend(get_points(ptn))
            return res

        self._hue = (self._hue + 1) % 360
        self._color.hsla = (self._hue, 100, 50, 100)

        points = self._points
        for p in points:
            pygame.draw.circle(gameDisplay, (255, 255, 255), p.int_pair(), width)
        points = get_knot()
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, self._color, points[p_n].int_pair(), points[p_n + 1].int_pair(), width)


class Knot(Polyline):
    pass


# Отрисовка справки
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Speed"])
    data.append(["", ""])
    data.append(["1", "Use line 1"])
    data.append(["2", "Use line 2"])
    data.append(["3", "Use line 3"])
    data.append(["4", "Use line 4"])
    data.append(["5", "Use line 5"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    # unittest.main()

    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    pols = [None] * 5
    key = 0

    steps = 50

    working = True
    show_help = False
    pause = False

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                elif event.key == pygame.K_r:
                    pols = [None] * 5
                elif event.key == pygame.K_p:
                    pause = not pause
                elif event.key == pygame.K_KP_PLUS:
                    steps += 5
                elif event.key == pygame.K_F1:
                    show_help = not show_help
                elif event.key == pygame.K_KP_MINUS:
                    steps -= 5
                elif event.key == pygame.K_1:
                    key = 0
                elif event.key == pygame.K_2:
                    key = 1
                elif event.key == pygame.K_3:
                    key = 2
                elif event.key == pygame.K_4:
                    key = 3
                elif event.key == pygame.K_5:
                    key = 4
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pols[key] == None: pols[key] = Knot()
                pols[key].add_point(Vec2d(event.pos))

        gameDisplay.fill((0, 0, 0))

        for pol in pols:
            if pol is None: continue
            pol.draw_points()
            if not pause: pol.set_points()

        if show_help: draw_help()

        pygame.display.flip()

        steps = 5 if steps < 5 else steps
        time.sleep(0.1/steps)

    pygame.display.quit()
    pygame.quit()
    exit(0)