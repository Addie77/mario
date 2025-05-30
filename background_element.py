import cv2

brick = (45, 82, 160)
platforms = [
    #(200,350,350,320),
    (500,400,700,370),
    (800,250,1000,220),
    (1200,230,1400,200),
    (1600,300,1800,270),
    #(2000,400,2200,370),
    (2400,350,2600,320),
    (2800,300,3000,270),
    #(3200,250,3400,220),
    #(3600,300,3800,270),
    (4000,350,4200,320),
    (4400,250,4600,220),
    #(4700,350,4800,320),
    (4800,300,5000,270),
    (5200,400,5400,370),
    #(5600,350,5800,320),
    (6000,300,6200,270),
    (6400,250,6600,220),
    (6700,400,6900,370),
    (6800,200,7000,170),
    (7200,300,7400,270),
    (7600,390,7800,360),
    (8000,230,8200,200),
    (8400,260,8600,230),
    #(8800,350,9000,320)
]

pipe_infos = [
    (1050, 150), (2650, 250), (5050, 400),
    (6280, 300), (7100, 290), (7900, 350), (8700, 250)
]

def draw_platforms(canvas, camera_x):
    for x1, y1, x2, y2 in platforms:
        cv2.rectangle(canvas, (x1 - camera_x, y1+15), (x2 - camera_x, y2+15), brick, -1)

def draw_pipes(canvas, camera_x):
    pipe_width = 50
    pipe_top_height = 30
    pipe_top_width = 70

    for pipe_x_world, pipe_height in pipe_infos:
        pipe_x = pipe_x_world - camera_x
        pipe_base_y = 525
        pipe_top_y = pipe_base_y - pipe_height - pipe_top_height

        if -pipe_width < pipe_x < canvas.shape[1]:
            cv2.rectangle(canvas, #畫水管底部
                          (pipe_x, pipe_base_y - pipe_height-10),
                          (pipe_x + pipe_width, pipe_base_y),
                          (0, 150, 0), -1)
            cv2.rectangle(canvas, #畫水管頂部
                          (pipe_x - (pipe_top_width - pipe_width) // 2, pipe_top_y-10),
                          (pipe_x + pipe_width + (pipe_top_width - pipe_width) // 2, pipe_top_y + pipe_top_height-10),
                          (0, 180, 0), -1)
def draw_clouds(canvas, camera_x, world_w):
    for base_x in range(150, world_w, 800):
        cv2.ellipse(canvas, (base_x - camera_x, 100), (60, 40), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(canvas, (base_x + 50 - camera_x, 90), (50, 35), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(canvas, (base_x + 100 - camera_x, 100), (60, 40), 0, 0, 360, (255, 255, 255), -1)

        cv2.ellipse(canvas, (base_x + 350 - camera_x, 80), (50, 30), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(canvas, (base_x + 390 - camera_x, 70), (40, 25), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(canvas, (base_x + 430 - camera_x, 80), (50, 30), 0, 0, 360, (255, 255, 255), -1)
