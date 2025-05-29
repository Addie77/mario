import cv2
import numpy as np
import random

star_img = cv2.imread("images/star.png", cv2.IMREAD_UNCHANGED)
mushroom_img = cv2.imread("images/mushroom.png", cv2.IMREAD_UNCHANGED)
star_img = cv2.resize(star_img, (50, 50)) 
mushroom_img = cv2.resize(mushroom_img, (50, 50))
class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(['star', 'mushroom'])
        self.img = star_img if self.type == 'star' else mushroom_img

    def draw(self, canvas, camera_x=0):
        if self.img is not None:
            h, w = self.img.shape[:2]
            x1 = self.x - camera_x
            y1 = self.y
            # 確保不會超出畫布
            if 0 <= x1 < canvas.shape[1] and 0 <= y1 < canvas.shape[0]:
                # 若有透明通道
                if self.img.shape[2] == 4:
                    overlay = self.img
                    bgr = overlay[:, :, :3]
                    alpha = overlay[:, :, 3] / 255.0
                    for c in range(3):
                        canvas[y1:y1+h, x1:x1+w, c] = (
                            alpha * bgr[:, :, c] +
                            (1 - alpha) * canvas[y1:y1+h, x1:x1+w, c]
                        )
                else:
                    canvas[y1:y1+h, x1:x1+w] = self.img

# 你可以自訂生成位置
item_positions = [
    (600, 400),
    (200, 350),
]

items = [Item(x, y) for x, y in item_positions]

if __name__ == "__main__":
    canva = np.ones((600, 800, 3), dtype=np.uint8) * 255
    for item in items:
        item.draw(canva)
    cv2.imshow("Items", canva)
    cv2.waitKey(0)
    cv2.destroyAllWindows()