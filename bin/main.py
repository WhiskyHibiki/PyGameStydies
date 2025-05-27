import pygame
import asyncio
import importlib
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
        # loading all games from library
        current_dir = os.path.dirname(__file__)
        project_dir = os.path.abspath(os.path.join(current_dir, ".."))
        library_dir = os.path.join(project_dir, "library")

        files = [f for f in os.listdir(library_dir) if f.endswith(".py")]
        buttons = []

        cols = 3  # count columns in the grid
        spacing = 50
        button_w = 200
        button_h = 60

        rows = (len(files) + cols - 1) // cols  # округляем вверх

        # >>> calculate total grid size <<<
        grid_width = cols * button_w + (cols - 1) * spacing
        grid_height = rows * button_h + (rows - 1) * spacing

        # >>> calculate offsets to center the grid <<<
        offset_x = (self.x - grid_width) // 2
        offset_y = (self.y - grid_height) // 2

        for index, file in enumerate(files):
            module_name = file[:-3]  # without >> .py <<
            game_module = importlib.import_module(f"library.{module_name}")

            row = index // cols
            col = index % cols

            x = offset_x + col * (button_w + spacing)
            y = offset_y + row * (button_h + spacing)

            rect = pygame.Rect(x, y, button_w, button_h)
            button = ButtonGame(module_name, rect, game_module)
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