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
from finish import show_finish_screen
from enemy import Enemy, enemy_positions

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

difficulty = show_start_screen()  # 1, 2, 3
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

game_passed = False  # 新增遊戲是否通過的標誌

speed_map = {1: 5, 2: 10, 3: 15}
enemy_speed = speed_map.get(difficulty, 1)
enemies = [Enemy(x, y, speed=enemy_speed) for x, y in enemy_positions]

# 初始化
player_lives = 3

while True:
    if not game_passed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                cv2.destroyAllWindows()
                difficulty = show_start_screen()
                show_tip_screen()
                coins = [Coin(c.x, c.y) for c in original_coins]
                items = [Item(x, y) for x, y in item_positions]
                player = Player("images/walk1.png", "images/walk2.png", x=100, y=300)
                camera_x = 0
                start_time = time.time()
                game_passed = False
                enemy_speed = speed_map.get(difficulty, 1)
                enemies = [Enemy(x, y, speed=enemy_speed) for x, y in enemy_positions]
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

        # 顯示生命數
        heart_text = f"heart x {player_lives}"
        text_size, _ = cv2.getTextSize(heart_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
        text_x = canvas.shape[1] // 2 - text_size[0] // 2
        text_y = 50
        cv2.putText(canvas, heart_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)

        # 繪製敵人
        for enemy in enemies:
            enemy.update()
            enemy.draw(canvas, camera_x)

        cv2.imshow("mario", canvas)
        cv2.waitKey(25)
        clock.tick(60)

        if keys[pygame.K_ESCAPE]:
            break

        # 正確縮排，確保每次都會檢查過關
        if not game_passed and player.x >= 9750 and player.y >= 400:
            game_passed = True
            pass_time = int(time.time() - start_time)
            from history import save_history, get_best_history
            save_history(pass_time, player.score)
            best_times, best_scores = get_best_history()
    else:
        # 只負責顯示過關畫面
        canvas[:] = (255, 255, 255)
        h, w = canvas.shape[:2]
        cv2.putText(canvas, "You win!", (w//2 - 150, h//2 - 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 128, 0), 5, cv2.LINE_AA)
        cv2.putText(canvas, f"Time: {pass_time}s", (w//2 - 120, h//2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(canvas, f"Score: {player.score}", (w//2 - 120, h//2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3, cv2.LINE_AA)
        # 顯示排行榜
        while len(best_times) < 3:
            best_times.append('-')
        while len(best_scores) < 3:
            best_scores.append('-')
        cv2.putText(canvas, "Best Times:", (w//2 - 120, h//2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 128), 2, cv2.LINE_AA)
        for i, t in enumerate(best_times):
            cv2.putText(canvas, f"{i+1}. {t}s", (w//2 - 60, h//2 + 110 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 128), 2, cv2.LINE_AA)
        cv2.putText(canvas, "Best Scores:", (w//2 + 80, h//2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 0, 0), 2, cv2.LINE_AA)
        for i, s in enumerate(best_scores):
            cv2.putText(canvas, f"{i+1}. {s}", (w//2 + 100, h//2 + 110 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow("mario", canvas)
        cv2.waitKey(25)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    cv2.destroyAllWindows()
                    show_start_screen()
                    show_tip_screen()
                    coins = [Coin(c.x, c.y) for c in original_coins]
                    items = [Item(x, y) for x, y in item_positions]
                    player = Player("images/walk1.png", "images/walk2.png", x=100, y=300)
                    camera_x = 0
                    start_time = time.time()
                    game_passed = False
                    break
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    cv2.destroy_allwindows()
                    sys.exit()

    # 主迴圈內敵人 update 後
    player_lives, hit_enemy = player.check_enemy_collision(enemies, canvas, player_lives)
    if hit_enemy:
        if player_lives <= 0:
            # 遊戲結束處理，顯示 Game Over 畫面並等待玩家操作
            canvas[:] = (0, 0, 0)
            over_text = "Game Over"
            text_size, _ = cv2.getTextSize(over_text, cv2.FONT_HERSHEY_SIMPLEX, 2, 5)
            text_x = canvas.shape[1] // 2 - text_size[0] // 2
            text_y = canvas.shape[0] // 2
            cv2.putText(canvas, over_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
            cv2.imshow("mario", canvas)
            cv2.waitKey(100)  # 短暫顯示

            # 進入等待玩家按鍵的 Game Over 畫面
            game_over_restart = False
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        cv2.destroyAllWindows()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            cv2.destroyAllWindows()
                            difficulty = show_start_screen()
                            show_tip_screen()
                            coins = [Coin(c.x, c.y) for c in original_coins]
                            items = [Item(x, y) for x, y in item_positions]
                            player = Player("images/walk1.png", "images/walk2.png", x=100, y=300)
                            camera_x = 0
                            start_time = time.time()
                            game_passed = False
                            player_lives = 3
                            enemy_speed = speed_map.get(difficulty, 1)
                            enemies = [Enemy(x, y, speed=enemy_speed) for x, y in enemy_positions]
                            game_over_restart = True
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            cv2.destroyAllWindows()
                            sys.exit()
                if game_over_restart:
                    break  # 跳出 Game Over 畫面 while True
                # 持續顯示 Game Over 畫面
                cv2.imshow("mario", canvas)
                cv2.waitKey(25)
        else:
            # 只重設道具，不要 new Player
            coins = [Coin(c.x, c.y) for c in original_coins]
            items = [Item(x, y) for x, y in item_positions]
            camera_x = 0
            player.score = 0  # 歸零分數
            continue
pygame.quit()
cv2.destroy_allwindows()
