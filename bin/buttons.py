import pygame


class ButtonGame:
    def __init__(self, name, rect: pygame.Rect, game_module):
        self.name = name
        self.original_rect = rect
        self.rect = rect.copy()
        self.game_module = game_module  # Импортированный модуль
        self.font = pygame.font.SysFont(None, 30)

        self.hovered = False
        self.scale = 1.1
        self.offset_x = 0
        self.offset_y = 0

        self.growth_speed = 2  # скорость увеличения
        self.angle = 0
        self.angle_add = 1
        self.angle_itter = 0
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
        # Масштабируем базовую поверхность до текущих размеров
        scaled_surface = pygame.transform.smoothscale(
            self.base_surface,
            (self.current_width, self.current_height)
        )

        # Поворачиваем масштабированную поверхность
        rotated_surface = pygame.transform.rotate(scaled_surface, self.angle)

        # Центрируем её на месте исходной кнопки
        rotated_rect = rotated_surface.get_rect(center=self.original_rect.center)

        # Рисуем
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

        # Ограничим размеры, чтобы не было скачков
        self.current_width = max(min(self.current_width, target_width), min(self.original_rect.width, target_width))
        self.current_height = max(min(self.current_height, target_height), min(self.original_rect.height, target_height))

        # Позиция с поворотом
        if self.angle_itter == 1:
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

            self.angle_itter = 0

        else:
            self.angle_itter += 1


        self.rect = pygame.Rect(
            self.original_rect.centerx - self.current_width // 2 + self.offset_x,
            self.original_rect.centery - self.current_height // 2 + self.offset_y,
            self.current_width,
            self.current_height
        )


    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)