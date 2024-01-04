# https://play.arkanoid.online/?lang=en
# Код работает нестабильно и проблемно, но это неплохой прогресс
# Возможно стоит убрать потоки для ускорения, но не уверен, что они дадут значительного прироста
# Сейчас скорость обработки около 0.1 сек

import cv2
import keyboard
from threading import Thread
import time
import win32api
import dxcam


camera = dxcam.create(output_idx=0, output_color="GRAY", region=(505, 130, 1450, 1030))
camera.start(target_fps=60)


while True:
    if keyboard.is_pressed("c"):
        flag = True
        break


def exit_check():
    global flag
    while flag:
        if keyboard.is_pressed("x"):
            flag = False
            camera.stop()
            break


def locate_ball_coordinates():
    global flag
    template = cv2.imread('ball.bmp', 0)
    old_cord = -1
    while flag:
        try:
            frame = camera.get_latest_frame()
            start = time.time()
            # ball_center_x = pyautogui.locate("ball.png", frame, confidence=0.99).left

            result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
            print(time.time() - start)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            ball_center_x, _ = max_loc
            ball_center_x_corrected = ball_center_x

            if old_cord != -1:
                ball_center_x_corrected += ball_center_x - old_cord

            win32api.SetCursorPos((ball_center_x_corrected + 16 + 505, 1000))
            old_cord = ball_center_x
            print(ball_center_x)
        except Exception:
            pass


thread1 = Thread(target=exit_check)
thread1.start()

thread2 = Thread(target=locate_ball_coordinates)
thread2.start()

thread1.join()
thread2.join()
