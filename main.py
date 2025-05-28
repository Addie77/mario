import cv2
import numpy as np
import pygame
import sys
from player import Player
from castle import Castle
from flag import Flag

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
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1)
pygame.display.set_mode((200, 100))
clock = pygame.time.Clock()

canvas_w, canvas_h = 800, 600
canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255

world_w, world_h = 10000, 600
brick = (45, 82, 160)

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
    (3600,300,3800,270),
    (4000,350,4200,320),
    (4400,250,4600,220),
    (4800,200,5000,170),
    (5200,400,5400,370),
    (5600,350,5800,320),
    (6000,300,6200,270),
    (6400,250,6600,220),
    (6800,200,7000,170),
    (7200,300,7400,270),
    (7600,390,7800,360),
    (8000,230,8200,200),
    (8400,260,8600,230),
    (8800,350,9000,320)
]

player = Player("walk1.png", "walk2.png", x=100, y=300)

camera_x = 0  # 全域變數，用來追蹤相機X軸位置（只能往右移）

def draw_clouds(canvas, camera_x, world_w):
    for base_x in range(150, world_w, 800):
        # 第一層雲（三個橢圓組成一組）
        cv2.ellipse(canvas, (base_x - camera_x, 100), (60, 40), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(canvas, (base_x + 50 - camera_x, 90), (50, 35), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(canvas, (base_x + 100 - camera_x, 100), (60, 40), 0, 0, 360, (255, 255, 255), -1)

        # 第二層雲（三個橢圓組成一組，稍微下移）
        cv2.ellipse(canvas, (base_x + 350 - camera_x, 80), (50, 30), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(canvas, (base_x + 390 - camera_x, 70), (40, 25), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(canvas, (base_x + 430 - camera_x, 80), (50, 30), 0, 0, 360, (255, 255, 255), -1)

castle = Castle(x=9700, y=375)
flag = Flag(x=9500, y=150)

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

    # 畫布初始化後，加上這一行畫雲
    draw_clouds(canvas, camera_x, world_w)

    # 地板
    cv2.rectangle(canvas, (0 - camera_x, 525), (world_w - camera_x, world_h), brick, -1)

    #下方水管(障礙物)
    pipe_infos = [
    (1050, 150),
    (2650, 250),
    (5050, 400),
    (6280, 300),
    (7100, 290),
    (7900, 350),
    (8700, 250)
    ]

    pipe_width = 50
    pipe_top_height = 30
    pipe_top_width = 70  # 上方突出寬度

    for pipe_x_world, pipe_height in pipe_infos:
        pipe_x = pipe_x_world - camera_x
        pipe_base_y = 525  # 地板y座標
        pipe_top_y = pipe_base_y - pipe_height - pipe_top_height

        if -pipe_width < pipe_x < canvas_w:  # 在視窗範圍內才畫
            # 水管主體
            cv2.rectangle(canvas,
                          (pipe_x, pipe_base_y - pipe_height),
                          (pipe_x + pipe_width, pipe_base_y),
                          (0, 150, 0), -1)  # 深綠色

            # 水管上方突出部分
            cv2.rectangle(canvas,
                          (pipe_x - (pipe_top_width - pipe_width) // 2, pipe_top_y),
                          (pipe_x + pipe_width + (pipe_top_width - pipe_width) // 2, pipe_top_y + pipe_top_height),
                          (0, 180, 0), -1)  # 稍亮綠色

    # 平台
    for x1, y1, x2, y2 in platforms:
        cv2.rectangle(canvas, (x1 - camera_x, y1+15), (x2 - camera_x, y2+15), brick, -1)

    flag.draw(canvas, camera_x)
    castle.draw(canvas, camera_x)

    current_img = player.get_image()
    canvas = paste_transparent(canvas, current_img, int(player.x - camera_x), int(player.y))

    cv2.imshow("mario", canvas)
    cv2.waitKey(25)
    clock.tick(60)

    if keys[pygame.K_ESCAPE]:
        break

pygame.quit()
cv2.destroyAllWindows()
