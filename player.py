import cv2
import numpy as np

class Player:
    def __init__(self, img1_path, img2_path, x=100, y=100):
        self.img1 = self.remove_background_with_alpha(img1_path)
        self.img2 = self.remove_background_with_alpha(img2_path)

        self.img1 = cv2.resize(self.img1, (100, 100))
        self.img2 = cv2.resize(self.img2, (100, 100))

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

    def update(self, key_map, canvas_width, platforms):
        # 水平移動
        self.vx = 0
        if key_map['left']:
            self.vx = -self.speed
            self.direction = "left"
        elif key_map['right']:
            self.vx = self.speed
            self.direction = "right"

        self.x += self.vx
        self.x = max(0, min(self.x, canvas_width - self.width))

        # 跳躍
        if key_map['jump'] and self.jump_count <= 3:
            self.vy = self.jump_strength
            self.jump_count += 1

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

        # 地板碰撞
        if not on_ground and self.y + self.height >= self.floor_y:
            self.y = self.floor_y - self.height
            self.vy = 0
            self.jump_count = 0

    def get_image(self):
        # 動畫交替與方向處理
        img = self.img1 if self.vx == 0 else (self.img1 if self.frame_flag else self.img2)
        self.frame_flag = not self.frame_flag if self.vx != 0 else self.frame_flag

        if self.direction == "left":
            img = cv2.flip(img, 1)
        return img
