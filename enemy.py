import cv2
import numpy as np

class Enemy:
    def __init__(self, x, y, speed=1, move_range=100):
        self.init_x = x
        self.x = x
        self.y = y
        self.radius = 25
        self.img = self.create_image()
        self.speed = speed
        self.move_range = move_range
        self.direction = 1  # 1:右, -1:左
        self.moved = 0      # 已移動距離

    def create_image(self):
        img = np.zeros((50, 50, 4), dtype=np.uint8)  # 全透明
        center = (25, 25)
        cv2.circle(img, center, self.radius, (18, 18, 201, 255), -1)
        cv2.circle(img, (center[0]-10, center[1]-7), 3, (0, 0, 0, 255), -1)
        cv2.circle(img, (center[0]+10, center[1]-7), 3, (0, 0, 0, 255), -1)
        cv2.line(img, (center[0]-10, center[1]+10), (center[0]+10, center[1]+10), (0, 0, 0, 255), 2)
        return img

    def update(self):
        self.x += self.direction * self.speed
        self.moved += self.direction * self.speed
        if abs(self.moved) >= self.move_range:
            self.direction *= -1

    def draw(self, canvas, camera_x):
        h, w = self.img.shape[:2]
        x1 = int(self.x - camera_x)
        y1 = int(self.y)
        x2 = x1 + w
        y2 = y1 + h
        cx1 = max(x1, 0)
        cy1 = max(y1, 0)
        cx2 = min(x2, canvas.shape[1])
        cy2 = min(y2, canvas.shape[0])
        ix1 = cx1 - x1
        iy1 = cy1 - y1
        ix2 = ix1 + (cx2 - cx1)
        iy2 = iy1 + (cy2 - cy1)
        if cx1 < cx2 and cy1 < cy2:
            alpha = self.img[iy1:iy2, ix1:ix2, 3] / 255.0
            for c in range(3):
                canvas[cy1:cy2, cx1:cx2, c] = (
                    alpha * self.img[iy1:iy2, ix1:ix2, c] +
                    (1 - alpha) * canvas[cy1:cy2, cx1:cx2, c]
                )

# 只保留座標，不要建立 enemies
enemy_positions = [
    (1400, 475),
    (2100, 475),
    (3200, 475),
    (3600, 475),
    (4080, 285),
    (4500, 475),
    (4880, 235),
    (5600, 475),
    (6780, 335),
    (7440, 475),
    (7680, 325),
    (8500, 475),
]