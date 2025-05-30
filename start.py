import pygame

tip_lines = [
    "Press 1 : easy game",
    "Press 2 : normal game",
    "Press 3 : hard game"
]
tip =[
    "W,space: Jump",
    "A,D: Move Left and Right",
    "ESC: Exit",
]
def show_start_screen():
    screen = pygame.display.set_mode((400,400 ))
    font_big = pygame.font.SysFont(None, 80)
    font_small = pygame.font.SysFont(None, 33)
    title = font_big.render("Super Mario", True, (255, 0, 0))
    while True:
        screen.fill((255, 255, 255))
        screen.blit(title, (200 - title.get_width()//2, 100))
        y = 180
        for line in tip_lines:
            tip_surface = font_small.render(line, True, (0, 0, 0))
            screen.blit(tip_surface, (35, y))
            y += 45  # 每行往下移一點
        pygame.display.flip() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    return 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    return 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    return 3

def show_tip_screen():
    screen = pygame.display.set_mode((250,200 ))
    screen.fill((255, 255, 255))
    y = 40
    font_small = pygame.font.SysFont(None, 25)
    font_big = pygame.font.SysFont(None, 30)
    title = font_big.render("Use pygame to control", True, (255, 0, 0))
    screen.blit(title, (10, 10))
    for line in tip:
            tip_surface = font_small.render(line, True, (0, 0, 0))
            screen.blit(tip_surface, (10, y))
            y += 45  # 每行往下移一點
    pygame.display.flip()