import pygame
from random import randrange


def run(old_x, old_y):
    snake_game = SnakeGame(old_x, old_y)
    snake_game.start_game()

class SnakeGame:
    def __init__(self, screen_w, screen_h):
        pygame.init()

        self.screen_w = screen_w
        self.screen_h = screen_h
        self.cell_size = 20
        self.grid_size = 32
        self.play_size = self.grid_size * self.cell_size

        # Центрируем игровое поле
        self.offset_x = (screen_w - self.play_size) // 2
        self.offset_y = (screen_h - self.play_size) // 2

        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.lost = False

        self.snake = [(16, 16)]
        self.direction = (1, 0)  # Начальное направление: вправо
        self.apple = self.spawn_apple()
        self.speed = 10

        self.next_direction = self.direction
        self.allow_turn = True

    def spawn_apple(self):
        while True:
            pos = (randrange(self.grid_size), randrange(self.grid_size))
            if pos not in self.snake:
                return pos

    def draw_cell(self, x, y, color):
        pygame.draw.rect(
            self.screen,
            color,
            (
                self.offset_x + x * self.cell_size,
                self.offset_y + y * self.cell_size,
                self.cell_size - 1,
                self.cell_size - 1,
            ),
        )

    def reset_game(self):
        self.snake = [(16, 16)]
        self.direction = (1, 0)
        self.apple = self.spawn_apple()
        self.lost = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.lost and event.key == pygame.K_r:
                    self.reset_game()

                elif not self.lost:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.direction = (1, 0)

    def move_snake(self):
        if self.lost:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % self.grid_size, (head_y + dy) % self.grid_size)

        if new_head in self.snake:
            self.lost = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.apple:
            self.apple = self.spawn_apple()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill((30, 30, 30))

        # Игровое поле
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.draw_cell(x, y, (50, 50, 50))

        # Яблоко
        self.draw_cell(*self.apple, (255, 0, 0))

        # Змея
        for part in self.snake:
            self.draw_cell(*part, (0, 255, 0))

        if self.lost:
            font = pygame.font.SysFont(None, 60)
            text1 = font.render("Game Over!", True, (255, 255, 255))
            text2 = font.render("Press R", True, (255, 255, 255))

            total_height = text1.get_height() + text2.get_height() + 10
            center_y = self.screen_h // 2 - total_height // 2

            text1_rect = text1.get_rect(center=(self.screen_w // 2, center_y + text1.get_height() // 2))
            text2_rect = text2.get_rect(center=(self.screen_w // 2, center_y + text1.get_height() + 10 + text2.get_height() // 2))

            self.screen.blit(text1, text1_rect)
            self.screen.blit(text2, text2_rect)

        pygame.display.flip()

    def start_game(self):
        while self.running:
            self.clock.tick(self.speed)
            self.handle_input()
            self.move_snake()
            self.draw()