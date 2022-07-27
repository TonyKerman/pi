#!/usr//bin/python
#_*_ coding: utf-8 _*_
import RPi.GPIO as GPIO
import time
#中断模式编程


KEY = 20


def MyInterrupt(KEY):
    print("KEY PRESS")


GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY,GPIO.IN,GPIO.PUD_UP)
GPIO.add_event_detect(KEY,GPIO.FALLING,MyInterrupt,200)
#增加事件检测，下降沿触发，忽略由于开关抖动引起的小于200ms的边缘操作

while True:
    time.sleep(1)