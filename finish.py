import cv2
from history import save_history, get_best_history

def show_finish_screen(canvas, pass_time, score):
    h, w = canvas.shape[:2]
    canvas[:] = (255, 255, 255)  # 設為全白背景

    # 寫入資料庫
    save_history(pass_time, score)
    # 查詢排行榜
    best_times, best_scores = get_best_history()

    # 補足三筆
    while len(best_times) < 3:
        best_times.append('-')
    while len(best_scores) < 3:
        best_scores.append('-')

    cv2.putText(canvas, "You win!", (w//2 - 150, h//2 - 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 128, 0), 5, cv2.LINE_AA)
    cv2.putText(canvas, f"Time: {pass_time}s", (w//2 - 120, h//2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(canvas, f"Score: {score}", (w//2 - 120, h//2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3, cv2.LINE_AA)

    # 顯示排行榜
    cv2.putText(canvas, "Best Times:", (w//2 - 120, h//2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 128), 2, cv2.LINE_AA)
    for i, t in enumerate(best_times):
        cv2.putText(canvas, f"{i+1}. {t}s", (w//2 - 60, h//2 + 110 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 128), 2, cv2.LINE_AA)

    cv2.putText(canvas, "Best Scores:", (w//2 + 80, h//2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 0, 0), 2, cv2.LINE_AA)
    for i, s in enumerate(best_scores):
        cv2.putText(canvas, f"{i+1}. {s}", (w//2 + 100, h//2 + 110 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 0, 0), 2, cv2.LINE_AA)
