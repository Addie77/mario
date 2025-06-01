import cv2
import numpy as np

class Castle:
    brick = (45,82,160)
    deep_brick = (32,58,112)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, camera_x):
        x = self.x - camera_x
        y = self.y
        # 主體
        cv2.rectangle(canvas, (x+0, y+0), (x+200, y+150), self.brick, -1)  # Base
        cv2.rectangle(canvas, (x+40, y-50), (x+160, y+0), self.brick, -1)  # Main tower
        cv2.rectangle(canvas, (x+70, y-80), (x+130, y-50), self.brick, -1)
        # 門窗
        cv2.rectangle(canvas, (x+20, y+25), (x+60, y+70), (0,0,0), -1)
        cv2.rectangle(canvas, (x+140, y+25), (x+180, y+70), (0,0,0), -1)
        cv2.rectangle(canvas, (x+70, y+80), (x+130, y+150), (0,0,0), -1)
        cv2.rectangle(canvas, (x+80, y+95), (x+120, y+150), (40,40,40), -1)
        # 側塔
        cv2.rectangle(canvas, (x-55, y-75), (x+0, y+150), self.deep_brick, -1)
        cv2.rectangle(canvas, (x-65, y-95), (x+10, y-75), self.brick, -1)
        cv2.rectangle(canvas, (x-65, y-110), (x-50, y-95), self.brick, -1)
        cv2.rectangle(canvas, (x-40, y-110), (x-15, y-95), self.brick, -1)
        cv2.rectangle(canvas, (x-5, y-110), (x+10, y-95), self.brick, -1)

        cv2.rectangle(canvas, (x+200, y-75), (x+255, y+150), self.deep_brick, -1)
        cv2.rectangle(canvas, (x+190, y-95), (x+265, y-75), self.brick, -1)
        cv2.rectangle(canvas, (x+190, y-110), (x+205, y-95), self.brick, -1)
        cv2.rectangle(canvas, (x+215, y-110), (x+240, y-95), self.brick, -1)
        cv2.rectangle(canvas, (x+250, y-110), (x+265, y-95), self.brick, -1)
class Flag:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, camera_x):
        x = self.x - camera_x
        y = self.y
        # 旗桿
        cv2.rectangle(canvas, (x, y), (x+20, y+375), (150,150,150), -1)
        # 旗子
        cv2.rectangle(canvas, (x+20, y), (x+140, y+70), (0,0,0), -1)

if __name__ == "__main__":
    canva = np.ones((600, 800, 3), dtype=np.uint8) * 255
    flag = Flag(120, 150)
    castle = Castle(400, 375)
    castle.draw(canva, 0)
    flag.draw(canva, 0)
    cv2.imshow("Flag", canva)
    cv2.waitKey()
    cv2.destroyAllWindows()