import cv2
import numpy as np
import time
import pygame  # 加在檔案最上面

class Player:
    def __init__(self, img1_path, img2_path, x=100, y=100):
        self.img1 = self.remove_background_with_alpha(img1_path)
        self.img2 = self.remove_background_with_alpha(img2_path)

        self.img1 = cv2.resize(self.img1, (70, 70))
        self.img2 = cv2.resize(self.img2, (70, 70))

        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 10
        self.jump_strength = -22
        self.jump_count = 0  # 二段跳計數

        self.frame_flag = True
        self.direction = "right"
        self.width = self.img1.shape[1]
        self.height = self.img1.shape[0]
        self.floor_y = 538  # 地板 y 座標
        self.score = 0  # 新增分數屬性

        self.origin_img1_path = img1_path
        self.origin_img2_path = img2_path
        self.star_img1_path = "images/starwalk1.png"
        self.star_img2_path = "images/starwalk2.png"
        self.star_mode = False
        self.star_mode_end_time = 0

        self.grow_animating = False
        self.grow_anim_start_time = 0

        self.invincible_until = 0

        self.big_mode = False  # 新增

    def remove_background_with_alpha(self, img_path, threshold=40):
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"圖片找不到: {img_path}")
        h, w = img.shape[:2]
        corners = [img[0, 0], img[0, w - 1], img[h - 1, 0], img[h - 1, w - 1]]
        bg_color = np.mean(corners, axis=0)
        diff = cv2.absdiff(img, np.uint8(bg_color))
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(diff_gray, threshold, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        b, g, r = cv2.split(img)
        return cv2.merge((b, g, r, mask))  # BGRA

    def update(self, key_map, canvas_width, platforms, pipe_infos, coins=None, world_w=10000, items=None):
        # 水平移動
        self.vx = 0
        if key_map['left']:
            self.vx = -self.speed
            self.direction = "left"
        elif key_map['right']:
            self.vx = self.speed
            self.direction = "right"

        self.x += self.vx
        self.x = max(0, min(self.x, world_w - self.width))  # 限制不超出左邊與右邊

        # 跳躍
        if key_map['jump'] and self.jump_count <= 2:
            self.vy = self.jump_strength
            self.jump_count += 1
            cv2.waitKey(20)  # 等待一段時間以避免過快的跳躍

        # 重力與垂直移動
        self.vy += 1.5
        self.y += self.vy

        # 平台碰撞偵測
        on_ground = False
        player_bottom = self.y + self.height
        player_center_x = self.x + self.width // 2

        for x1, y1, x2, y2 in platforms:
            if x1 <= player_center_x <= x2:
                if self.vy >= 0 and player_bottom >= y1 and (self.y + self.height - self.vy) <= y1:
                    self.y = y1 - self.height
                    self.vy = 0
                    self.jump_count = 0
                    on_ground = True
                    break
        # --- Pipe 碰撞偵測 ---
        pipe_width = 50
        pipe_top_height = 30
        for pipe_x, pipe_height in pipe_infos:
            px1 = pipe_x
            px2 = pipe_x + pipe_width
            py1 = 525 - pipe_height - pipe_top_height
            py2 = 525

            # 站在水管頂部
            if px1 <= player_center_x <= px2:
                if self.vy >= 0 and player_bottom >= py1 and (self.y + self.height - self.vy) <= py1:
                    self.y = py1 - self.height
                    self.vy = 0
                    self.jump_count = 0
                    on_ground = True
                    break

            # 左右側碰撞（防止穿過水管側邊）
            # 玩家往右撞到水管左側
            if self.vx > 0 and self.x + self.width > px1 and self.x < px1 and player_bottom > py1 + 5:
                if self.y + self.height > py1 + 5 and self.y < py2:
                    self.x = px1 - self.width
            # 玩家往左撞到水管右側
            if self.vx < 0 and self.x < px2 and self.x + self.width > px2 and player_bottom > py1 + 5:
                if self.y + self.height > py1 + 5 and self.y < py2:
                    self.x = px2
                
        # 地板碰撞
        if not on_ground and self.y + self.height >= self.floor_y:
            self.y = self.floor_y - self.height
            self.vy = 0
            self.jump_count = 0

        # --- 金幣碰撞偵測 ---
        if coins is not None:
            player_rect = (self.x, self.y, self.x + self.width, self.y + self.height)
            remove_list = []
            for coin in coins:
                coin_rect = (coin.x - 10, coin.y - 10, coin.x + 10, coin.y + 10)  # 半徑10
                # 簡單矩形碰撞判斷
                if (player_rect[0] < coin_rect[2] and player_rect[2] > coin_rect[0] and
                    player_rect[1] < coin_rect[3] and player_rect[3] > coin_rect[1]):
                    remove_list.append(coin)
            for coin in remove_list:
                coins.remove(coin)
                self.score += 1  # 每吃到一個金幣加一分
                pygame.mixer.Sound("music/getcoin.mp3").play()  # 播放音效

        # --- 蘑菇碰撞偵測 ---
        if items is not None:
            player_rect = (self.x, self.y, self.x + self.width, self.y + self.height)
            remove_list = []
            for item in items:
                h, w = item.img.shape[:2]
                item_rect = (item.x, item.y, item.x + w, item.y + h)
                if (player_rect[0] < item_rect[2] and player_rect[2] > item_rect[0] and
                    player_rect[1] < item_rect[3] and player_rect[3] > item_rect[1]):
                    if hasattr(item, "type") and item.type == "mushroom":
                        # 進入變大動畫
                        pygame.mixer.Sound("music/grow.mp3").play()  # 播放變大音效
                        self.img1 = cv2.resize(self.img1, (100, 100))
                        self.img2 = cv2.resize(self.img2, (100, 100))
                        self.width = 100
                        self.height = 100
                        self.y -= 30
                        self.big_mode = True  # 變大
                        self.grow_animating = True
                        self.grow_anim_start_time = time.time()
                        remove_list.append(item)
                        
                    elif hasattr(item, "type") and item.type == "star":
                        self.img1 = cv2.resize(self.remove_background_with_alpha(self.star_img1_path), (self.width, self.height))
                        self.img2 = cv2.resize(self.remove_background_with_alpha(self.star_img2_path), (self.width, self.height))
                        self.star_mode = True
                        self.star_mode_end_time = time.time() + 5
                        remove_list.append(item)
                        # 播放 star.mp3，並在 5 秒後停止
                        pygame.mixer.music.load("music/star.mp3")
                        pygame.mixer.music.play(-1)  # 循環播放
                        self.star_music_start_time = time.time()
            for item in remove_list:
                items.remove(item)

        # --- 變大動畫進行 ---
        if self.grow_animating:
            if time.time() - self.grow_anim_start_time >= 0.5:
                self.img1 = cv2.resize(self.img1, (100, 100))
                self.img2 = cv2.resize(self.img2, (100, 100))
                self.width = 100
                self.height = 100
                self.big_mode = True  # 變大
                self.grow_animating = False
            return
        # --- 星星模式倒數 ---
        if self.star_mode and time.time() > self.star_mode_end_time:
            self.img1 = cv2.resize(self.remove_background_with_alpha(self.origin_img1_path), (self.width, self.height))
            self.img2 = cv2.resize(self.remove_background_with_alpha(self.origin_img2_path), (self.width, self.height))
            self.star_mode = False
            # 恢復音樂
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/bgm.mp3")
            pygame.mixer.music.play(-1)

    def get_image(self):
        # 動畫交替與方向處理
        img = self.img1 if self.vx == 0 else (self.img1 if self.frame_flag else self.img2)
        self.frame_flag = not self.frame_flag if self.vx != 0 else self.frame_flag

        if self.direction == "left":
            img = cv2.flip(img, 1)
        return img

    def check_enemy_collision(self, enemies, canvas, player_lives):
        """
        檢查與敵人碰撞，若碰撞則扣一條命、黑畫面顯示 heart，並回傳剩餘生命值
        """
        # 1秒無敵緩衝期間，什麼都不做
        if time.time() < self.invincible_until:
            return player_lives, False

        # 星星無敵判斷（如果有 star_mode）
        if self.star_mode:
            player_rect = (self.x, self.y, self.x + self.width, self.y + self.height)
            for enemy in enemies[:]:
                enemy_rect = (enemy.x, enemy.y, enemy.x + 50, enemy.y + 50)
                if (player_rect[0] < enemy_rect[2] and player_rect[2] > enemy_rect[0] and
                    player_rect[1] < enemy_rect[3] and player_rect[3] > enemy_rect[1]):
                    if enemy in enemies:
                        enemies.remove(enemy)
                    self.score += 1
            return player_lives, False  # 無敵時不會扣命

        # 變大狀態下碰到敵人，只變回原本大小，不扣命
        if self.big_mode:
            player_rect = (self.x, self.y, self.x + self.width, self.y + self.height)
            for enemy in enemies:
                enemy_rect = (enemy.x, enemy.y, enemy.x + 50, enemy.y + 50)
                if (player_rect[0] < enemy_rect[2] and player_rect[2] > enemy_rect[0] and
                    player_rect[1] < enemy_rect[3] and player_rect[3] > enemy_rect[1]):
                    # 判斷是否從上方踩到敵人
                    player_bottom_last = self.y + self.height - self.vy  # 上一幀底部
                    enemy_top = enemy.y
                    if self.vy > 0 and player_bottom_last <= enemy_top:
                        # 從上方踩到敵人
                        if enemy in enemies:
                            enemies.remove(enemy)
                        self.score += 1
                        self.vy = self.jump_strength // 2  # 踩到後彈跳
                        return player_lives, False  # 沒有扣命
                    else:
                        # 側面或下方碰撞，變回原本大小
                        pygame.mixer.Sound("music/besmall.mp3").play()
                        self.img1 = cv2.resize(self.remove_background_with_alpha(self.origin_img1_path), (70, 70))
                        self.img2 = cv2.resize(self.remove_background_with_alpha(self.origin_img2_path), (70, 70))
                        self.width = 70
                        self.height = 70
                        self.big_mode = False
                        self.invincible_until = time.time() + 1  # 1秒無敵緩衝
                        return player_lives, False  # 只變小，不扣命

        # 其餘情況才會扣命
        player_rect = (self.x, self.y, self.x + self.width, self.y + self.height)
        for enemy in enemies:
            enemy_rect = (enemy.x, enemy.y, enemy.x + 50, enemy.y + 50)
            # 判斷是否碰撞
            if (player_rect[0] < enemy_rect[2] and player_rect[2] > enemy_rect[0] and
                player_rect[1] < enemy_rect[3] and player_rect[3] > enemy_rect[1]):
                # 判斷是否從上方踩到敵人
                player_bottom_last = self.y + self.height - self.vy  # 上一幀底部
                enemy_top = enemy.y
                if self.vy > 0 and player_bottom_last <= enemy_top:
                    # 從上方踩到敵人
                    if enemy in enemies:
                        enemies.remove(enemy)
                    self.score += 1
                    self.vy = self.jump_strength // 2  # 踩到後彈跳
                    return player_lives, False  # 沒有扣命
                else:
                    # 側面或下方碰撞，扣命
                    player_lives -= 1
                    canvas[:] = (0, 0, 0)
                    heart_text = f"heart x {player_lives}"
                    text_size, _ = cv2.getTextSize(heart_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
                    text_x = canvas.shape[1] // 2 - text_size[0] // 2
                    text_y = 50
                    cv2.putText(canvas, heart_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
                    cv2.imshow("mario", canvas)
                    cv2.waitKey(600)
                    self.x, self.y = 100, 300
                    self.vx, self.vy = 0, 0
                    self.invincible_until = time.time() + 0.8
                    return player_lives, True
        return player_lives, False
