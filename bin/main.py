import pygame
import asyncio
import importlib
import importlib.util
import os

from bin.config import x_pixels, y_pixels, tick_rate
from bin.buttons import ButtonGame

class GameWindow:
    def __init__(self, x_pix: int, y_pix: int, ticks: int):
        self.x = x_pix
        self.y = y_pix
        self.tick_rate = ticks

        pygame.init()

        self.screen = pygame.display.set_mode((self.x, self.y))
        pygame.display.set_caption("Mini Game Launcher")
        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.SysFont(None, 36)
        self.buttons = self.load_games()

    def load_games(self):

        current_dir = os.path.dirname(__file__)
        project_dir = os.path.abspath(os.path.join(current_dir, ".."))
        library_dir = os.path.join(project_dir, "library")

        buttons = []
        cols = 3
        spacing = 50
        button_w = 200
        button_h = 60

        entries = os.listdir(library_dir)
        valid_games = []

        for entry in entries:
            full_path = os.path.join(library_dir, entry)

            # 1. Если обычный .py-файл
            if entry.endswith(".py") and os.path.isfile(full_path):
                module_name = f"library.{entry[:-3]}"
                valid_games.append((entry[:-3], module_name))

            # 2. Если папка с main.py внутри
            elif os.path.isdir(full_path):
                main_file = os.path.join(full_path, "main.py")
                if os.path.isfile(main_file):
                    module_name = f"library.{entry}.main"
                    valid_games.append((entry, module_name))

        rows = (len(valid_games) + cols - 1) // cols
        grid_width = cols * button_w + (cols - 1) * spacing
        grid_height = rows * button_h + (rows - 1) * spacing
        offset_x = (self.x - grid_width) // 2
        offset_y = (self.y - grid_height) // 2

        for index, (display_name, module_name) in enumerate(valid_games):
            try:
                game_module = importlib.import_module(module_name)
            except Exception as e:
                print(f"❌ Failed to import {module_name}: {e}")
                continue

            row = index // cols
            col = index % cols

            x = offset_x + col * (button_w + spacing)
            y = offset_y + row * (button_h + spacing)

            rect = pygame.Rect(x, y, button_w, button_h)
            button = ButtonGame(display_name, rect, game_module)
            buttons.append(button)

        return buttons

    async def start_game(self):
        some_numb = 26
        add = 1
        iteration = 0

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

                else:
                    if button.hovered:
                        button.hovered = False


            iteration, some_numb, add = self.iter_gradient(iteration, some_numb, add)

            pygame.display.flip()
            self.clock.tick(self.tick_rate)

            await asyncio.sleep(0)

    @staticmethod
    def iter_gradient(iteration, some_numb, add):
        if iteration == 1:
            if some_numb == 125 or some_numb == 25:
                add = -add
                some_numb += add

            else:
                some_numb += add
            iteration = 0

        else:
            iteration += 1

        return iteration, some_numb, add


    def run_game(self, module):
        if hasattr(module, "run"):
            module.run(self.x, self.y)  # Предполагаем, что в игре есть функция run()



async def main():
    game = GameWindow(x_pixels, y_pixels, tick_rate)
    await game.start_game()

asyncio.run(main())