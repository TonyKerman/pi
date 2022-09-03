import math
import time
import RPi.GPIO as GPIO
import cv2 as cv
import ui
import adafruit_vl53l0x
import pygame
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo
from threading import Thread,RLock
from concurrent.futures import ThreadPoolExecutor
import traceback
import adafruit_pcf8591.pcf8591 as PCF
from adafruit_pcf8591.analog_in import AnalogIn

"""
接线：(BCM)
    i2c * 3
    发射 
    充电
"""
range = -1
vl53l0x_status = 1
bjv = 1.351
ajv = -9.6491

def setup():
    global cap,vl53l0x,pwm,s,Sx,Sy,face_cascade,face_cascade,pcf_in_x,pcf_in_y
    GPIO.setmode(GPIO.BCM)
    i2c = busio.I2C(SCL, SDA)
    try:
        pwm = PCA9685(i2c)  # 使用默认地址初始化PWM设备
        pwm.frequency = 50
        Sx = servo.Servo(pwm.channels[15])
        Sy = servo.Servo(pwm.channels[14])
        Sx.angle = 75
        Sy.angle = 30
    except ValueError:
        print('Cant find PCA9685')
    try:
        vl53l0x = adafruit_vl53l0x.VL53L0X(i2c)
        vl53l0x.measurement_timing_budget = 200000
    except ValueError:
        global vl53l0x_status
        vl53l0x_status = 0
        print('Cant find vl5310x ')
    try:
       pcf = PCF.PCF8591(i2c)
       pcf_in_x = AnalogIn(pcf, PCF.A0)
       pcf_in_y = AnalogIn(pcf,PCF.A1)
    except ValueError:
        print('Cant find PCF8591 ')
    # 创建一个级联分类器 加载一个 .xml 分类器文件. 它既可以是Haar特征也可以是LBP特征的分类器.
    face_cascade = cv.CascadeClassifier('/home/tony/.local/lib/python3.9/site-packages/cv2/data'
                                        '/haarcascade_frontalface_default.xml')
    eye_cascade = cv.CascadeClassifier('/home/tony/.local/lib/python3.9/site-packages/cv2'
                                       '/data/haarcascade_eye.xml')

    # s = pygame.display.set_mode((10, 10)) #pygame setup
    # pygame.key.set_repeat(100, 100)
    # pygame.display.iconify()
    cap = cv.VideoCapture(0)
    # cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    # cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)




def show():
    while True:
        ret, frame = cap.read()
        width, height = frame.shape[1],frame.shape[0]
        text = 'Range' + str(range)
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
            cv.waitKey(15)
            #return f1[0], f1[2]
        except :
            cv.imshow("frame", frame)
            cv.waitKey(15)
            #return (-1,-1)


def detect():
    global range
    while True:
        if vl53l0x_status:
            with RLock():
                range = vl53l0x.range
        time.sleep(0.2)


def yaim():
    l = range / 1000
    u = 120
    v = bjv * math.sqrt(u) + ajv
    try:
        sin2a = 9.8 * l / (v ** 2)
        a = math.asin(sin2a) / 2
        a = round(math.degrees(a) / 2)
        Sy.angle = a
    except ValueError:
        pass


def control():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    raise KeyboardInterrupt
                if event.key == pygame.K_e:
                    yaim()
                if event.key == pygame.K_RIGHT:
                    print("右")
                    Sx.angle -= 3
                if event.key == pygame.K_LEFT:
                    print("左")
                    Sx.angle += 3
                if event.key == pygame.K_SPACE:
                    self_aiming = 1


if __name__ == '__main__':
    setup()
    try:
        #     with ThreadPoolExecutor(max_workers=4) as pool:
        #     workers = ['show','detect']
        #     pool.submit(detect)
        #     pool.submit(show)
        t1 = Thread(target=show, daemon=True)
        t2 = Thread(target=detect, daemon=True)
        #t3 = Thread(target=control, daemon=True)
        t1.start()
        t2.start()
        #t3.start()
        while True:
            ux = (pcf_in_x.value / 65535) * pcf_in_x.reference_voltage
            uy = (pcf_in_y.value / 65535) * pcf_in_y.reference_voltage
            if ux > 3:
                print('左')
            elif ux <1:
                print('右')
            time.sleep(0.1)
    except Exception :
        traceback.print_exc()

    finally:
        t1.join()
        t2.join()
        print('___________________\n')
        GPIO.cleanup()
        cap.release()
        cv.destroyAllWindows()

