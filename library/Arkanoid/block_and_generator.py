import pygame
import random


class ArkanoidBlock:
    WIDTH = 100
    HEIGHT = 25

    def __init__(self, position_x, position_y):
        self.block_colour = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        self.block_rect = pygame.Rect(position_x, position_y, self.WIDTH, self.HEIGHT)
        self.block_health = random.randint(1, 5)


class BlockGenerator:
    def __init__(self, area_rect: pygame.Rect):
        """
        :param area_rect: pygame.Rect — зона, в которой можно размещать блоки
        """
        self.area_rect = area_rect

    def generate_grid(self, rows = 5, cols = 8, spacing_x = 10, spacing_y = 10):
        """
        Generate blocks in grid (pattern)
        :param rows: Blocks grid rows, lol
        :param cols: Blocks grid columns, lol
        :param spacing_x: Spacing between neighboring Blocks (x)
        :param spacing_y: Spacing between neighboring Blocks (y)
        :return: Blocks
        """
        blocks = []
        total_width = cols * ArkanoidBlock.WIDTH + (cols - 1) * spacing_x
        total_height = rows * ArkanoidBlock.HEIGHT + (rows - 1) * spacing_y

        start_x = self.area_rect.x + (self.area_rect.width - total_width) // 2
        start_y = self.area_rect.y + (self.area_rect.height - total_height) // 2

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (ArkanoidBlock.WIDTH + spacing_x)
                y = start_y + row * (ArkanoidBlock.HEIGHT + spacing_y)
                blocks.append(ArkanoidBlock(x, y))

        return blocks