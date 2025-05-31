import pygame
import sys

def show_finish_screen(pass_time, score):
    screen = pygame.display.set_mode((400, 200))
    screen.fill((255, 255, 255))
    font_big = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 36)
    text1 = font_big.render("Game Pass", True, (0, 128, 0))
    text2 = font_small.render(f"Time: {pass_time}s", True, (0, 0, 0))
    text3 = font_small.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text1, (80, 30))
    screen.blit(text2, (120, 100))
    screen.blit(text3, (120, 140))
    pygame.display.flip()
    # 等待玩家關閉視窗
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()