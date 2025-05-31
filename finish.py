import cv2
import time

def show_finish_screen(canvas, pass_time, score):
    h, w = canvas.shape[:2]
    cv2.putText(canvas, "You win!", (w//2 - 150, h//2 - 40), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 128, 0), 5, cv2.LINE_AA)
    cv2.putText(canvas, f"Time: {pass_time}s", (w//2 - 120, h//2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(canvas, f"Score: {score}", (w//2 - 120, h//2 + 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3, cv2.LINE_AA)
