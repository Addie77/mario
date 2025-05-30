import cv2
import numpy as np
import pygame
import sys
import time
from player import Player
from castle import Castle
from castle import Flag
from coin import coins as original_coins,Coin
from background_element import platforms,pipe_infos,draw_platforms,draw_pipes,draw_clouds
from item import items,Item,item_positions
from start import show_start_screen, show_tip_screen
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

show_start_screen()
show_tip_screen()

canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255

world_w, world_h = 10000, 600

player = Player("images/walk1.png", "images/walk2.png", x=100, y=300)

camera_x = 0  # 相機X軸位置

coins = [Coin(c.x, c.y) for c in original_coins]
items = [Item(x, y) for x, y in item_positions]

castle = Castle(x=9700, y=375)
flag = Flag(x=9500, y=150)

start_time = time.time()  # 記錄開始時間

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            cv2.destroyAllWindows()  # 關掉 OpenCV 視窗
            show_start_screen()
            show_tip_screen()
            # 重新初始化 coins、items、player、camera_x、start_time
            coins = [Coin(c.x, c.y) for c in original_coins]      # 重新產生金幣
            items = [Item(x, y) for x, y in item_positions]
            player = Player("images/walk1.png", "images/walk2.png", x=100, y=300)
            camera_x = 0
            start_time = time.time()
            continue

    keys = pygame.key.get_pressed()

    key_map = {
        'left': keys[pygame.K_a] or keys[pygame.K_LEFT],
        'right': keys[pygame.K_d] or keys[pygame.K_RIGHT],
        'jump': keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]
    }

    player.update(key_map, canvas_w, platforms, pipe_infos, coins, world_w, items)

    desired_camera_x = player.x - canvas_w // 2
    if desired_camera_x > camera_x:
        camera_x = min(desired_camera_x, world_w - canvas_w)

    canvas[:] = (255, 206, 135)
    brick = (45, 82, 160)
    
    cv2.rectangle(canvas, (0 - camera_x, 525), (world_w - camera_x, world_h), brick, -1)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    for coin in coins:
        coin.draw(canvas, camera_x)

    for item in items:
        item.draw(canvas, camera_x)
    
    flag.draw(canvas, camera_x)
    castle.draw(canvas, camera_x)
    draw_clouds(canvas, camera_x, world_w)
    draw_platforms(canvas, camera_x)
    draw_pipes(canvas, camera_x)

    current_img = player.get_image()
    canvas = paste_transparent(canvas, current_img, int(player.x - camera_x), int(player.y))

    # 顯示計時器
    elapsed_time = int(time.time() - start_time)
    timer_text = f"{elapsed_time}s"
    cv2.putText(canvas, timer_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 0), 2, cv2.LINE_AA)

    # 顯示分數（右上角）
    score_text = f"Score: {player.score}"
    text_size, _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    text_x = canvas.shape[1] - text_size[0] - 20
    text_y = 40
    cv2.putText(canvas, score_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("mario", canvas)
    cv2.waitKey(25)
    clock.tick(60)

    if keys[pygame.K_ESCAPE]:
        break

pygame.quit()
cv2.destroyAllWindows()
