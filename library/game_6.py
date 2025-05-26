import pygame

def run(old_x, old_y):
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Mini Game")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = pygame.display.set_mode((old_x, old_y))
                running = False

        screen.fill((0, 128, 128))
        pygame.display.flip()