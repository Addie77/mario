import cv2
import numpy as np
import pygame
import sys
from player import Player
import random

def paste_transparent(imgBackground, overlay, x, y):
    bgr = overlay[:, :, :3]
    alpha = overlay[:, :, 3] / 255.0
    h, w = overlay.shape[:2]

    if x < 0:
        overlay = overlay[:, -x:, :]
        w = overlay.shape[1]
        x = 0
    if y < 0:
        overlay = overlay[-y:, :, :]
        h = overlay.shape[0]
        y = 0

    if x + w > imgBackground.shape[1]:
        w = imgBackground.shape[1] - x
        overlay = overlay[:, :w, :]
    if y + h > imgBackground.shape[0]:
        h = imgBackground.shape[0] - y
        overlay = overlay[:h, :, :]

    bgr = overlay[:, :, :3]
    alpha = overlay[:, :, 3] / 255.0

    for c in range(3):
        imgBackground[y:y+h, x:x+w, c] = (
            imgBackground[y:y+h, x:x+w, c] * (1 - alpha) + bgr[:, :, c] * alpha
        )
    return imgBackground

pygame.init()
pygame.display.set_mode((200, 100))
clock = pygame.time.Clock()

canvas_w, canvas_h = 800, 600
canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255

world_w, world_h = 10000, 600

platforms = [
    (200,350,350,320),
    (500,400,700,370),
    (800,250,1000,220),
    (1200,230,1400,200),
    (1600,300,1800,270),
    (2000,400,2200,370),
    (2400,350,2600,320),
    (2800,300,3000,270),
    (3200,250,3400,220),
    (3600,200,3800,170),
    (4000,150,4200,120)
]

player = Player("walk1.png", "walk2.png", x=100, y=450)

camera_x = 0  # 全域變數，用來追蹤相機X軸位置（只能往右移）

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
    
    player.update(key_map, world_w, platforms)

    # 限制玩家不要超出視窗左邊界（player.x >= camera_x）
    if player.x < camera_x:
        player.x = camera_x

    # 相機只往右移動
    desired_camera_x = player.x - canvas_w // 2
    if desired_camera_x > camera_x:
        camera_x = min(desired_camera_x, world_w - canvas_w)

    canvas[:] = (255, 206, 135)

    # 畫雲，減去 camera_x 來捲動畫面
    cv2.ellipse(canvas, (150 - camera_x, 100), (60, 40), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(canvas, (200 - camera_x, 90), (50, 35), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(canvas, (250 - camera_x, 100), (60, 40), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(canvas, (500 - camera_x, 80), (50, 30), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(canvas, (540 - camera_x, 70), (40, 25), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(canvas, (580 - camera_x, 80), (50, 30), 0, 0, 360, (255, 255, 255), -1)

    # 地板
    cv2.rectangle(canvas, (0 - camera_x, 525), (world_w - camera_x, world_h), (45, 82, 160), -1)

    # 平台
    for x1, y1, x2, y2 in platforms:
        cv2.rectangle(canvas, (x1 - camera_x, y1+15), (x2 - camera_x, y2+15), (45, 82, 160), -1)

    current_img = player.get_image()
    canvas = paste_transparent(canvas, current_img, int(player.x - camera_x), int(player.y))

    cv2.imshow("maerio", canvas)
    cv2.waitKey(25)
    clock.tick(60)

    if keys[pygame.K_ESCAPE]:
        break

pygame.quit()
cv2.destroyAllWindows()
