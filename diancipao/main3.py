import math
import time
import RPi.GPIO as GPIO
import cv2 as cv
import ui
import vl53l0x
import pygame
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo


def setup():
    GPIO.setmode(GPIO.BCM)
    try:
        i2c_bus = busio.I2C(SCL, SDA)
        pwm = PCA9685(i2c_bus)  # 使用默认地址初始化PWM设备
        pwm.frequency = 50
    except ValueError:
        print('No i2c device is detected')
    # 创建一个级联分类器 加载一个 .xml 分类器文件. 它既可以是Haar特征也可以是LBP特征的分类器.
    face_cascade = cv.CascadeClassifier('/home/tony/.local/lib/python3.9/site-packages/cv2/data'
                                        '/haarcascade_frontalface_default.xml')
    eye_cascade = cv.CascadeClassifier('/home/tony/.local/lib/python3.9/site-packages/cv2'
                                       '/data/haarcascade_eye.xml')

    s = pygame.display.set_mode((10, 10)) #pygame setup
    pygame.key.set_repeat(100, 100)
    # pygame.display.iconify()
    cap = cv.VideoCapture(0)
    # cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    # cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    Sx = servo.Servo(pwm.channels[15])
    Sy = servo.Servo(pwm.channels[14])


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
        return (-1,-1)


def main():
    show()


if __name__ == '__main__':
    setup()
    try:
        while True:
            main()
    except Exception as e:
        print(' find an error ',e)
    finally:
        GPIO.cleanup()
        cap.release()
        cv.destroyAllWindows()
