import pygame
import random
import math


class ArkanoidBall:
    def __init__(self, screen_w, screen_h, angle_degrees: float = random.randint(0, 360)):
        self.ball_circle_radius = 15
        self.ball_speed = 10

        self.max_x = screen_w
        self.max_y = screen_h

        self.x = screen_w // 2
        self.y = screen_h // 2

        # Переводим угол в радианы
        angle_radians  = angle_degrees

        # Вектор движения
        self.dx = math.cos(angle_radians) * self.ball_speed
        self.dy = math.sin(angle_radians) * self.ball_speed

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Отражение от левых и правых стенок — меняем направление по X
        if self.x - self.ball_circle_radius <= 0 or self.x + self.ball_circle_radius >= self.max_x:
            self.reflect_vertical()  # меняем dx
            return False

        # Отражение от потолка — меняем направление по Y
        if self.y - self.ball_circle_radius <= 0:
            self.reflect_horizontal()  # меняем dy
            return False

        # Game Over
        elif self.y + self.ball_circle_radius >= self.max_y:
            self.ball_speed = 0
            return True


    def reflect_vertical(self):
        """Зеркальное отражение от вертикальной поверхности (например, от боковых стенок)"""
        self.dx = -self.dx

    def reflect_horizontal(self):
        """Зеркальное отражение от горизонтальной поверхности (например, от арки или потолка)"""
        self.dy = -self.dy

    def get_rect(self):
        return pygame.Rect(
            self.x - self.ball_circle_radius,
            self.y - self.ball_circle_radius,
            self.ball_circle_radius * 2,
            self.ball_circle_radius * 2,
        )

    def bounce_from_arka(self, arka_rect):
        # Центр арки
        arka_center = arka_rect.centerx
        offset = (self.x - arka_center) / (arka_rect.width / 2)  # от -1 до 1

        # Угол отскока от -60 до +60 градусов
        max_bounce_angle = math.radians(60)
        bounce_angle = offset * max_bounce_angle

        # Скорость мяча
        speed = math.hypot(self.dx, self.dy)

        # Новый вектор (отскакивает вверх)
        self.dx = speed * math.sin(bounce_angle)
        self.dy = -speed * math.cos(bounce_angle)


class ArkanoidArka:
    def __init__(self, screen_w, screen_h):
        width = 150
        height = 20
        self.max_w = screen_w
        x = (screen_w - width) // 2
        y = screen_h - height - 10  # отступ от низа

        self.arka_rect = pygame.Rect(x, y, width, height)
        self.arka_colour = (random.randint(100, 255), random.randint(0, 255), random.randint(0, 255))
        self.arka_speed = 10

    def touching(self):
        pass

    def move(self, direction: int):
        new_arka_pos = self.arka_rect.x + (self.arka_speed * direction)
        if new_arka_pos > 0 and new_arka_pos + self.arka_rect.width < self.max_w:
            self.arka_rect.x = new_arka_pos