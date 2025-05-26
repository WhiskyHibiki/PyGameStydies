import pygame

def run(old_x, old_y):
    turtle_game = TurtleGame(old_x, old_y)
    turtle_game.start_game()

class TurtleGame:
    def __init__(self, old_x, old_y):
        pygame.init()
        self.old_screen = (old_x, old_y)
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Turtle Game")

        self.fill = (255, 255, 255)
        self.running = True

        self.last_point = None  # Последняя точка для рисования линии
        self.lines = []         # Линии (пары точек)

    def start_game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.screen = pygame.display.set_mode(self.old_screen)
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка — рисуем
                        current_pos = event.pos
                        if self.last_point is not None:
                            self.lines.append((self.last_point, current_pos))
                        self.last_point = current_pos

                    elif event.button == 3:  # Правая кнопка — обрываем цепочку
                        self.last_point = None

            self.screen.fill(self.fill)

            for start, end in self.lines:
                pygame.draw.line(self.screen, (0, 0, 0), start, end, 2)

            pygame.display.flip()
