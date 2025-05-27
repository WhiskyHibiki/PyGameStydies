import pygame

from library.Arkanoid.arkanoid import ArkanoidBall, ArkanoidArka
from library.Arkanoid.block_and_generator import BlockGenerator


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
        self.generator = BlockGenerator(pygame.Rect(0, 0, screen_w, 300))
        self.blocks = self.generator.generate_grid()

        self.running = True
        self.game_over = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
                pygame.display.set_caption("Mini Games Launcher")
                self.running = False

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.arka.move(-1)
            elif keys[pygame.K_RIGHT]:
                self.arka.move(1)

        elif self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Рестарт: просто создаём новый объект и запускаем
                run(self.screen_w, self.screen_h)
                self.running = False

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

        if self.game_over:
            font = pygame.font.SysFont(None, 60)
            text1 = font.render("Game Over!", True, (255, 255, 255))
            text2 = font.render("Press R", True, (255, 255, 255))

            total_height = text1.get_height() + text2.get_height() + 10
            center_y = self.screen_h // 2 - total_height // 2

            text1_rect = text1.get_rect(center=(self.screen_w // 2, center_y + text1.get_height() // 2))
            text2_rect = text2.get_rect(center=(self.screen_w // 2, center_y + text1.get_height() + 10 + text2.get_height() // 2))

            self.screen.blit(text1, text1_rect)
            self.screen.blit(text2, text2_rect)

    def draw_cell(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y),)

    def update_object(self):
        if not self.game_over:

            for ball in self.balls:
                self.game_over = ball.move()
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