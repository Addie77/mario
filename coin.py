import cv2
import numpy as np

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, camera_x=0):
        radius = 10
        cv2.circle(canvas, (self.x - camera_x, self.y), radius, (23,154,255), -1)
        cv2.circle(canvas, (self.x - camera_x, self.y), radius - 3, (0, 215, 255), -1)

# 直接在這裡定義 coins 清單
coins = [
    Coin(520, 360),
    Coin(550, 360),
    Coin(580, 360),
    Coin(610, 360),

    Coin(1240, 170),
    Coin(1270, 170),
    Coin(1300, 170),

    Coin(1800,250),
    Coin(1830,210),
    Coin(1860,170),
    Coin(1900, 130),

    Coin(2830, 260),
    Coin(2860, 260),
    Coin(2900, 260),

    Coin(3500, 510),
    Coin(3530, 510),
    Coin(3560, 510),
    Coin(3600, 510),
    Coin(3640, 510),

    Coin(4900,130),
    Coin(4930,130),

    Coin(5300,210),
    Coin(5330,170),
    Coin(5360,130),

    Coin(6400, 160),
    Coin(6430, 160),
    Coin(6460, 160),

    Coin(7000, 120),
    Coin(7030, 120),
    Coin(7060, 120),
    Coin(7100, 120),
    Coin(7140, 120),

    Coin(8400, 200),
    Coin(8430, 180),
    Coin(8460, 160),
    Coin(8500, 140),
]


