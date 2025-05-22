# player.py
import cv2
import numpy as np

class Player:
    def __init__(self, img1_path, img2_path, x=0, y=0):
        self.img1 = self._load_image(img1_path)
        self.img2 = self._load_image(img2_path)
        self.img1_flipped = cv2.flip(self.img1, 1)
        self.img2_flipped = cv2.flip(self.img2, 1)

        self.x = x
        self.y = y
        self.vx = 10
        self.vy = 0
        self.jump_power = -15
        self.gravity = 1
        self.jump_count = 0
        self.max_jumps = 2
        self.ground_y = y
        self.jump_key_released = True
        self.direction = "right"
        self.frame_flag = True
        self.width = self.img1.shape[1]

    def _load_image(self, path):
        img = cv2.imread(path)
        img = cv2.resize(img, (100, 100))
        h, w = img.shape[:2]
        corners = [img[0, 0], img[0, w-1], img[h-1, 0], img[h-1, w-1]]
        bg_color = np.mean(corners, axis=0)
        diff = cv2.absdiff(img, np.uint8(bg_color))
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(diff_gray, 40, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        b, g, r = cv2.split(img)
        return cv2.merge((b, g, r, mask))

    def update(self, keys, canvas_w):
        moved = False
        if keys['left']:
            self.x = max(0, self.x - self.vx)
            self.direction = "left"
            moved = True
        if keys['right']:
            self.x = min(canvas_w - self.width, self.x + self.vx)
            self.direction = "right"
            moved = True

        if keys['jump']:
            if self.jump_key_released and self.jump_count < self.max_jumps:
                self.vy = self.jump_power
                self.jump_count += 1
                self.jump_key_released = False
        else:
            self.jump_key_released = True

        self.y += self.vy
        self.vy += self.gravity

        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.vy = 0
            self.jump_count = 0

        if moved:
            self.frame_flag = not self.frame_flag

    def get_image(self):
        if self.direction == "right":
            return self.img1 if self.frame_flag else self.img2
        else:
            return self.img1_flipped if self.frame_flag else self.img2_flipped
