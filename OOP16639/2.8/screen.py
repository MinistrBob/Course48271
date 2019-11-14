#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, v=(0, 0)):
        """
        Вектор определяется координатами x2, y2 — точка конца вектора.
        Начало вектора всегда совпадает с центом координат (x1, y1)=(0, 0).
        :param v:
        """
        if v is None:
            self.x2 = float(0)
            self.y2 = float(1)
        self.x2 = float(v[0])
        self.y2 = float(v[1])

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d((self.x2 + other.x2, self.y2 + other.y2))

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d((self.x2 - other.x2, self.y2 - other.y2))

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d((self.x2 * k, self.y2 * k))

    def __len__(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x2 * self.x2 + self.y2 * self.y2)

    def int_pair(self):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return self.x2, self.y2


class Polyline:
    """
    Реализовать класс замкнутых ломаных Polyline с методами отвечающими за добавление в ломаную точки (Vec2d)
    c её скоростью, пересчёт координат точек (set_points) и отрисовку ломаной (draw_points). Арифметические действия
    с векторами должны быть реализованы с помощью операторов, а не через вызовы соответствующих методов.
    """

    def __init__(self, display, points, speeds, step):
        self.display = display
        self.points = points
        self.speeds = speeds
        self.steps = step

    def add_point(self, pos):
        self.points.append(Vec2d(pos))
        self.speeds.append(Vec2d((random.random() * 2, random.random() * 2)))

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x2 > SCREEN_DIM[0] or self.points[p].x2 < 0:
                self.speeds[p] = Vec2d((- self.speeds[p].x2, self.speeds[p].y2))
            if self.points[p].y2 > SCREEN_DIM[1] or self.points[p].y2 < 0:
                self.speeds[p] = Vec2d((self.speeds[p].x2, -self.speeds[p].y2))

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.display, color,
                                 (int(points[p_n].x2), int(points[p_n].y2)),
                                 (int(points[p_n + 1].x2), int(points[p_n + 1].y2)), width)
        elif style == "points":
            for p in points:
                pygame.draw.circle(self.display, color,
                                   (int(p.x2), int(p.y2)), width)

    def draw_help(self):
        """функция отрисовки экрана справки программы"""
        self.display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = [["F1", "Show Help"], ["R", "Restart"], ["P", "Pause/Play"], ["Num+", "More points"],
                ["Num-", "Less points"], ["", ""], [str(self.steps), "Current points"]]

        pygame.draw.lines(self.display, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.display.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


class Knot(Polyline):

    def __init__(self, display, points, speeds, step):
        self.display = display
        self.points = points
        self.speeds = speeds
        self.steps = step

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, bpoints, count):
        if len(bpoints) < 3:
            return []
        res = []
        for i in range(-2, len(bpoints) - 2):
            ptn = []
            ptn.append((bpoints[i] + bpoints[i + 1]) * 0.5)
            ptn.append(bpoints[i + 1])
            ptn.append((bpoints[i + 1] + bpoints[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("MyScreenSaver")

    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    k = Knot(gameDisplay, [], [], 35)

    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    k.points = []
                    k.speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    k.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    k.steps -= 1 if k.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                k.add_point(event.pos)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        k.draw_points(k.points)
        k.draw_points(k.get_knot(k.points, k.steps), "line", 3, color)
        if not pause:
            k.set_points()
        if show_help:
            k.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
