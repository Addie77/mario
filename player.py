import cv2
import numpy as np

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
        self.x = max(0, min(self.x, world_w - self.width))

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

        # --- 蘑菇碰撞偵測 ---
        if items is not None:
            player_rect = (self.x, self.y, self.x + self.width, self.y + self.height)
            remove_list = []
            for item in items:
                # 假設 item.img 已經 resize 成 100x100
                h, w = item.img.shape[:2]
                item_rect = (item.x, item.y, item.x + w, item.y + h)
                if (player_rect[0] < item_rect[2] and player_rect[2] > item_rect[0] and
                    player_rect[1] < item_rect[3] and player_rect[3] > item_rect[1]):
                    if hasattr(item, "type") and item.type == "mushroom":
                        # 角色變大
                        self.img1 = cv2.resize(self.img1, (100, 100))
                        self.img2 = cv2.resize(self.img2, (100, 100))
                        self.width = 100
                        self.height = 100
                        remove_list.append(item)
            for item in remove_list:
                items.remove(item)

    def get_image(self):
        # 動畫交替與方向處理
        img = self.img1 if self.vx == 0 else (self.img1 if self.frame_flag else self.img2)
        self.frame_flag = not self.frame_flag if self.vx != 0 else self.frame_flag

        if self.direction == "left":
            img = cv2.flip(img, 1)
        return img
