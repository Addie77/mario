# main.py
import cv2
import numpy as np
import pygame
import sys
from player import Player

def paste_transparent(imgBackground, overlay, x, y):
    bgr = overlay[:, :, :3]
    alpha = overlay[:, :, 3] / 255.0
    h, w = overlay.shape[:2]

    for c in range(3):
        imgBackground[y:y+h, x:x+w, c] = (
            imgBackground[y:y+h, x:x+w, c] * (1 - alpha) + bgr[:, :, c] * alpha
        )
    return imgBackground

# 初始化
pygame.init()
pygame.display.set_mode((200, 100))
clock = pygame.time.Clock()

canvas_w, canvas_h = 1000, 600
canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255

player = Player("walk1.png", "walk2.png", x=100, y=450)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    key_map = {
        'left': keys[pygame.K_a] or keys[pygame.K_LEFT],
        'right': keys[pygame.K_d] or keys[pygame.K_RIGHT],
        'jump': keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]
    }

    player.update(key_map, canvas_w)

    canvas[:] = 255
    current_img = player.get_image()
    canvas = paste_transparent(canvas, current_img, player.x, player.y)

    cv2.imshow("maerio", canvas)
    if cv2.waitKey(30) == 27:
        break

    clock.tick(30)

cv2.destroyAllWindows()
pygame.quit()
