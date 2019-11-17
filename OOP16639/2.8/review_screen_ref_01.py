#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


# =======================================================================================
# Класс для работы с векторами (точками). Создает новый тип данных, с которым потом работают другие классы
# =======================================================================================
class Vec2d:
    def __init__(self, point):
        self.x = int(point[0])
        self.y = int(point[1])

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d((self.x - other.x, self.y - other.y))

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d((self.x + other.x, self.y + other.y))

    def __len__(self):
        """возвращает длину вектора"""
        return int(math.sqrt(self.x * self.x + self.y * self.y))

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d((self.x * k, self.y * k))

    def __truediv__(self, k):
        """возвращает результат деления целочисленного вектора на число"""
        return Vec2d((self.x // k, self.y // k))

    def int_pair(self):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return self.x, self.y


# =======================================================================================
# Класс отрисовки точек и линий а так же вывод помощи
# =======================================================================================

class Polyline(object):
    """класс замкнутых ломаных Polyline с методами отвечающими 
    за добавление в ломаную точки (Vec2d) c её скоростью, пересчёт координат 
    точек (set_points) и отрисовку ломаной (draw_points)"""

    def __init__(self):
        self.speed = 0
        self.steps = 0
        self.points = []
        self.speeds = []
        self.working = True
        self.show_help = False
        self.pause = True

    def draw_points(self, style="points", width=3, color=(255, 255, 255), knot=False):
        """функция отрисовки точек на экране
        добавлена проверка knot=True, если да - рисуем кривую по опорным точкам, если нет - точки """
        if knot == True:
            points = self.get_knot()
        else:
            points = self.points

        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)
        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)

    def draw_help(self):
        """функция отрисовки экрана справки программы"""

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
        data.append([str(self.steps), "Current points"])
        data.append([str(self.points[-1].int_pair()), "Last point position"])
        data.append([str(self.speed), "Current speed"])

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d((- self.speeds[p].x, self.speeds[p].y))
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d((self.speeds[p].x, -self.speeds[p].y))

    def speed_up(self):
        """ доп. функционал - увеличиваем скорость движения линий и точек на экране в 2 раза (клавиша "UP" """
        self.speed += 2
        for idx, s in enumerate(self.speeds):
            self.speeds[idx] = s * 2

    def speed_down(self):
        """ доп. функционал - уменьшаем скорость движения линий и точек на экране в 2 раза (клавиша "DOWN" """
        self.speed -= 2
        for idx, s in enumerate(self.speeds):
            self.speeds[idx] = s / 2

    def get_status(self, event):
        """ контроль за обработкой клавиатурных команд и сбор координат точек для отрисовки"""
        if event.type == pygame.QUIT:
            self.working = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.working = False
            if event.key == pygame.K_r:
                self.points = []
                self.speeds = []
                self.steps = 0
            if event.key == pygame.K_p:
                self.pause = not self.pause
            if event.key == pygame.K_UP:
                self.speed_up()
            if event.key == pygame.K_DOWN:
                self.speed_down()
            if event.key == pygame.K_KP_PLUS:
                self.steps += 1
            if event.key == pygame.K_F1:
                self.show_help = not self.show_help
            if event.key == pygame.K_KP_MINUS:
                self.steps -= 1 if self.steps > 1 else 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            new_point = Vec2d(event.pos)
            self.points.append(new_point)
            new_speed = Vec2d((random.random() * 2, random.random() * 2))
            self.speeds.append(new_speed)
            self.steps += 1


# =======================================================================================
# Класс расчета опорных точек для рисования линий
# =======================================================================================
class Knot(Polyline):
    """расчет координат опорных точек"""

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn))
        return res


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":

    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    hue = 0
    color = pygame.Color(0)

    new_line = Knot()

    while new_line.working:
        for event in pygame.event.get():
            new_line.get_status(event)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        new_line.draw_points()
        new_line.draw_points("line", 3, color, knot=True)
        if not new_line.pause:
            new_line.set_points()
        if new_line.show_help:
            new_line.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
