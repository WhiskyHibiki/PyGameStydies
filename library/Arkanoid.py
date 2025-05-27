import pygame
import random
import math



def run(old_x, old_y):
    arkanoid_game = ArkanoidGame(old_x, old_y)
    arkanoid_game.start_game()

class ArkanoidGame:
    def __init__(self, screen_w, screen_h):
        self.pygame = pygame.init()
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.speed = 60
        self.clock = pygame.time.Clock()

        self.gradient = 30
        self.invert_gradient = 30
        self.gradient_add = 1
        self.iter = 0

        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption("Arkanoid Game")

        self.arka = ArkanoidArka(screen_w, screen_h)
        self.balls = [ArkanoidBall(screen_w, screen_h)]
        self.blocks = [
            ArkanoidBlock(10, 10),
            ArkanoidBlock(120, 10),
            ArkanoidBlock(230, 10),
            ArkanoidBlock(340, 10),
            ArkanoidBlock(450, 10),
        ]

        self.running = True

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
                pygame.display.set_caption("Mini Games Launcher")
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.arka.move(-1)
        elif keys[pygame.K_RIGHT]:
            self.arka.move(1)

    def draw(self):
        self.screen.fill((self.gradient, 30, self.invert_gradient))

        if self.iter == 1:
            if self.gradient == 50 or self.gradient == 10:
                self.gradient_add = -self.gradient_add

            self.invert_gradient += -self.gradient_add
            self.gradient += self.gradient_add

            self.iter = 0

        else:
            self.iter += 1

    def draw_cell(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y),)

    def update_object(self):

        for ball in self.balls:
            ball.move()
            pygame.draw.circle(self.screen, "white", (ball.x, ball.y), ball.ball_circle_radius)

            ball_rect = ball.get_rect()

            # --- Столкновение - Арка ---
            if ball_rect.colliderect(self.arka.arka_rect):
                ball.bounce_from_arka(self.arka.arka_rect)  # Отскакивает вверх от арки

            # --- Столкновение - Блоки ---
            for block in self.blocks[:]:  # Копия списка, будем удалять
                if ball_rect.colliderect(block.block_rect):
                    ball.reflect_horizontal()  # Простое отражение, можно улучшить

                    block.block_health -= 1
                    if block.block_health <= 0:
                        self.blocks.remove(block)

        # --- Сама Арка ---
        pygame.draw.rect(self.screen, self.arka.arka_colour, self.arka.arka_rect)

        # --- Сами Блоки ---
        for block in self.blocks:
            pygame.draw.rect(self.screen, block.block_colour, block.block_rect)

    def start_game(self):
        while self.running:
            self.clock.tick(self.speed)
            self.handle_input()
            self.draw()
            self.update_object()
            pygame.display.flip()

class ArkanoidBlock:
    def __init__(self, position_x, position_y):
        self.block_colour = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.block_rect = pygame.Rect(position_x, position_y, 100, 25)

        self.block_health = random.randint(1,5)

    def touching(self):
        pass

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

        # Отражение от потолка — меняем направление по Y
        if self.y - self.ball_circle_radius <= 0 or self.y + self.ball_circle_radius >= self.max_y:
            self.reflect_horizontal()  # меняем dy

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