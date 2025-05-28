import cv2
import numpy as np

class Flag:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, camera_x):
        x = self.x - camera_x
        y = self.y
        # 旗桿
        cv2.rectangle(canvas, (x, y), (x+20, y+375), (168,168,168), -1)
        # 旗子
        cv2.rectangle(canvas, (x+20, y), (x+140, y+70), (0,0,0), -1)

if __name__ == "__main__":
    canva = np.ones((600, 800, 3), dtype=np.uint8) * 255
    flag = Flag(120, 150)
    flag.draw(canva, 0)
    cv2.imshow("Flag", canva)
    cv2.waitKey()
    cv2.destroyAllWindows()