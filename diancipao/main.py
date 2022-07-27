'''
单位 mm
l = 19.78mm
depth =77.30
hguan=104.39
h = 1309.4-n
'''
import math
import time
import sg90
import RPi.GPIO as GPIO
import cv2 as cv
import ui
import vl53l0x
import pygame

GPIO.setmode(GPIO.BCM)
ax0 = 75
ay0 = 30
ax = 0
ay = 0
ax1 = 0
ay1 = 0
bjv = 1.351
ajv = -9.6491


def direct():
    global ax1, ay1
    if ax1 != ax:
        x = ax + ax0
        if x < 10:
            x = 10
        elif x > 150:
            x = 150
        Sx.set(x)
        ax1 = ax
    if ay1 != ay:
        y = ay + ay0
        if y < 25:
            y = 25
        elif y > 125:
            y = 125
        Sy.qset(y)
        ay1 = ay


def uaim(mode, cartesian=(0, 0), polar=(0, 0), ):
    global ax, ay
    if mode == 'l':
        ay = 15
        sin = 0.259
        cos = 0.966
    elif mode == 'm':
        ay = 30
        sin = 0.5
        cos = 0.866
    elif mode == 'h':
        ay = 45
        sin = 0.707
        cos = 0.707
    if cartesian != (0, 0):
        l = math.sqrt(cartesian[0] ** 2 + cartesian[1] ** 2)
        ax = round(math.degrees(math.atan2(-cartesian[0], cartesian[1])))
    else:
        l = polar[0]
        ax = polar[1]
    print(l, ax)

    v = math.sqrt(9.8 * l / (2 * sin * cos))
    u = round(((v - ajv) / bjv) ** 2)
    print('转角为', ax)
    print("电压为", u)


def yaim(l):
    global ay
    l = l / 1000
    u = 120
    v = bjv * math.sqrt(u) + ajv
    try:
        sin2a = 9.8 * l / (v ** 2)
        a = math.asin(sin2a) / 2
        a = round(math.degrees(a) / 2)
        ay = a
    except ValueError:
        ay = 45
    print('..')


def wait_for_aim():
    a = float(input('x'))
    b = float(input('y'))
    uaim('m', cartesian=(a, b))


def show(l):
    ret, frame = cap.read()
    width, height = frame.shape[1],frame.shape[0]
    text = 'Range' + str(l)
    # ui
    ui.ui(frame, width, height, text=text)
    # 人脸检测
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
    try:
        f1 = faces[0]
        for (x, y, w, h) in faces:
            # 在原图像上绘制矩形
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # 旋转
        # frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
        cv.imshow("frame", frame)
        cv.waitKey(10)
        return f1[0], f1[2]
    except :
        cv.imshow("frame", frame)
        cv.waitKey(10)
        return (0,0)

# 创建一个级联分类器 加载一个 .xml 分类器文件. 它既可以是Haar特征也可以是LBP特征的分类器.
face_cascade = cv.CascadeClassifier('/home/tony/.local/lib/python3.9/site-packages/cv2/data'
                                    '/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('/home/tony/.local/lib/python3.9/site-packages/cv2/data/haarcascade_eye.xml')
s = pygame.display.set_mode((10, 10))
print('wait')
cap = cv.VideoCapture(0)

# cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
print('begin')
GPIO.setmode(GPIO.BCM)
Sx = sg90.Servo(6)
Sy = sg90.Servo(13)
Sx.qset(ax0)
Sy.qset(ay0)
self_aiming=0
try:
    while True:
        #l = vl53l0x.detect()
        l=111
        xw=show(l)
        if xw:
            fx, fw = xw[0],xw[1]
            print(fx, fw)
            fx = fx + fw / 2
            if self_aiming == 1 and abs(fx - 640) > 10:
                if fx - 640 < 0:
                    ax += 1
                if fx - 640 > 0:
                    ax -= 1
            elif abs(fx - 640) < 10:
                self_aiming = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    raise KeyboardInterrupt
                if event.key == pygame.K_e:
                    yaim(l)
                if event.key == pygame.K_RIGHT:
                    print("右")
                    ax -= 3
                if event.key == pygame.K_LEFT:
                    print("左")
                    ax += 3
                if event.key == pygame.K_SPACE :
                    self_aiming = 1

        direct()
        #print(ax, "   ", ay)
except Exception as e:
    print('over           ',e)
Sx.stop()
Sy.stop()
# 结束进程，释放GPIO引脚
GPIO.cleanup()
cap.release()
cv.destroyAllWindows()
