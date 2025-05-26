import pygame
import asyncio
import importlib
import random
import os

from bin.config import x_pixels, y_pixels, tick_rate

class GameWindow:
    def __init__(self, x_pix: int, y_pix: int, ticks: int):
        self.x = x_pix
        self.y = y_pix
        self.tick_rate = ticks

        pygame.init()

        self.screen = pygame.display.set_mode((self.x, self.y))
        pygame.display.set_caption("Game Launcher")
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.SysFont(None, 36)
        self.buttons = self.load_games()

    def load_games(self):
        # loading all games from library
        current_dir = os.path.dirname(__file__)
        project_dir = os.path.abspath(os.path.join(current_dir, ".."))
        library_dir = os.path.join(project_dir, "library")

        files = [f for f in os.listdir(library_dir) if f.endswith(".py")]
        buttons = []

        cols = 3  # count columns in the grid
        spacing = 20
        button_w = 200
        button_h = 60

        for index, file in enumerate(files):
            module_name = file[:-3]  # without >> .py <<
            game_module = importlib.import_module(f"library.{module_name}")

            row = index // cols
            col = index % cols

            x = spacing + col * (button_w + spacing)
            y = spacing + row * (button_h + spacing)

            rect = pygame.Rect(x, y, button_w, button_h)
            button = ButtonGame(module_name, rect, game_module)
            buttons.append(button)

        return buttons

    async def start_game(self):
        some_numb = 26
        add = 1
        itteration = 0

        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            self.run_game(button.game_module)



            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill((some_numb, some_numb, some_numb//2))

            for button in self.buttons:
                button.update(mouse_pos)
                button.draw(self.screen)

                if button.original_rect.collidepoint(mouse_pos):
                    if not button.hovered:
                        button.hovered = True
                        await button.is_hovering()

                else:
                    if button.hovered:
                        button.hovered = False
                        await button.is_hovering()


            itteration, some_numb, add = self.itter_gradient(itteration, some_numb, add)

            pygame.display.flip()
            self.clock.tick(self.tick_rate)

            await asyncio.sleep(0)

    def itter_gradient(self, itteration, some_numb, add):
        if itteration == 1:
            if some_numb == 125 or some_numb == 25:
                add = -add
                some_numb += add

            else:
                some_numb += add
            itteration = 0

        else:
            itteration += 1

        return itteration, some_numb, add


    def run_game(self, module):
        if hasattr(module, "run"):
            module.run(self.x, self.y)  # Предполагаем, что в игре есть функция run()


class ButtonGame:
    def __init__(self, name, rect: pygame.Rect, game_module):
        self.name = name
        self.original_rect = rect
        self.rect = rect.copy()
        self.game_module = game_module  # Импортированный модуль
        self.font = pygame.font.SysFont(None, 30)

        self.hovered = False
        self.scale = 1.15
        self.offset_x = 0
        self.offset_y = 0

        self.growth_speed = 2  # скорость увеличения
        self.angle = 0
        self.angle_add = 1
        self.current_width = rect.width
        self.current_height = rect.height

        # Поверхность кнопки
        self.base_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.update_base_surface()

    def update_base_surface(self):
        self.base_surface.fill((255, 255, 255))  # белый фон
        text = self.font.render(self.name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.base_surface.get_width() // 2, self.base_surface.get_height() // 2))
        self.base_surface.blit(text, text_rect)


    def draw(self, screen):
        # Повернутая версия кнопки
        rotated_surface = pygame.transform.rotate(self.base_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=self.original_rect.center)

        screen.blit(rotated_surface, rotated_rect.topleft)


    def update(self, mouse_pos):
        self.hovered = self.original_rect.collidepoint(mouse_pos)

        target_scale = self.scale if self.hovered else 1.0
        target_width = int(self.original_rect.width * target_scale)
        target_height = int(self.original_rect.height * target_scale)

        # Плавное изменение размера
        if self.current_width < target_width:
            self.current_width += self.growth_speed
        elif self.current_width > target_width:
            self.current_width -= self.growth_speed

        if self.current_height < target_height:
            self.current_height += self.growth_speed
        elif self.current_height > target_height:
            self.current_height -= self.growth_speed

        # Ограничим размеры
        self.current_width = max(self.original_rect.width, min(target_width, self.current_width))
        self.current_height = max(self.original_rect.height, min(target_height, self.current_height))

        # Позиция с поворотом
        if self.hovered:
            if self.angle == 10 or self.angle == -10:
                self.angle_add = -self.angle_add
            self.angle = (self.angle + self.angle_add)  # вращение

        else:
            if self.angle != 0:
                if self.angle >= 0:
                    self.angle_add = -1
                    self.angle = (self.angle + self.angle_add)

                elif self.angle <= 0:
                    self.angle_add = 1
                    self.angle = (self.angle + self.angle_add)


        self.rect = pygame.Rect(
            self.original_rect.centerx - self.current_width // 2 + self.offset_x,
            self.original_rect.centery - self.current_height // 2 + self.offset_y,
            self.current_width,
            self.current_height
        )


    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)



async def main():
    game = GameWindow(x_pixels, y_pixels, tick_rate)
    await game.start_game()

asyncio.run(main())