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

            # 計算實際要貼的範圍
            x1_clip = max(x1, 0)
            y1_clip = max(y1, 0)
            x2_clip = min(x1 + w, canvas.shape[1])
            y2_clip = min(y1 + h, canvas.shape[0])

            # 計算貼圖要裁切的範圍
            img_x1 = x1_clip - x1
            img_y1 = y1_clip - y1
            img_x2 = img_x1 + (x2_clip - x1_clip)
            img_y2 = img_y1 + (y2_clip - y1_clip)

            if x2_clip > x1_clip and y2_clip > y1_clip:
                region = canvas[y1_clip:y2_clip, x1_clip:x2_clip]
                overlay = self.img[img_y1:img_y2, img_x1:img_x2]
                bgr = overlay[:, :, :3]
                alpha = overlay[:, :, 3] / 255.0
                for c in range(3):
                    region[..., c] = (
                        region[..., c] * (1 - alpha) + bgr[..., c] * alpha
                    )

# 你可以自訂生成位置
item_positions = [
    (2480, 280),
    (6480, 190),
]

items = [Item(x, y) for x, y in item_positions]

if __name__ == "__main__":
    canva = np.ones((600, 800, 3), dtype=np.uint8) * 255
    for item in items:
        item.draw(canva)
    cv2.imshow("Items", canva)
    cv2.waitKey(0)
    cv2.destroyAllWindows()