import cv2
import numpy as np

img = np.ones((500, 500,4), dtype=np.uint8) * 255 
img[:, :, 3] = 255
en_speed=0
#固定範圍內左右移動
a=True
add = True
enemy_opsx = 150

while a:
    for i in range(200):
        if add:
            enemy_opsx += en_speed #簡單2 普通2 困難6
        elif not add:
            enemy_opsx -= en_speed #簡單2 普通2 困難6
        img = np.ones((500, 500,4), dtype=np.uint8) * 255 
        img[:, :, 3] = 255
        cv2.circle(img, (enemy_opsx, 250), 25, (0, 0, 255), -1)
        cv2.circle(img, (enemy_opsx-10, 243), 3, (0, 0, 0), -1)
        cv2.circle(img, (enemy_opsx+10, 243), 3, (0, 0, 0), -1)
        cv2.line(img, (enemy_opsx-10, 260), (enemy_opsx+10, 260), (0, 0, 0), 2)
        if enemy_opsx >=400:
            add = False
        if enemy_opsx<=150:
            add = True
        cv2.imshow("img", img)
        key = cv2.waitKey(1)
        if key == ord('q') or  key == 27 or key ==ord('Q'):
            a=False
        if key == ord('1'):
            en_speed = 2
        if key == ord('2'):
            en_speed = 4
        if key == ord('3'):
            en_speed = 6
    
    
cv2.destroyAllWindows()
