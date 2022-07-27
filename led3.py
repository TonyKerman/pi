#!/usr/bin/python
#_*_ coding:utf-8 _*_
import RPi.GPIO as GPIO
import time
LED = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)

try:
    t = int(input("输入时间"))
    while True:
        GPIO.output(LED,GPIO.HIGH)
        time.sleep(t)
        GPIO.output(LED,GPIO.LOW)
        time.sleep(t)
except:
    print("except")
GPIO.cleanup()

#注：（1）#!/usr/bin/env python，定义python解析脚本的绝对路径。
#    （2）# -*- coding: utf-8 -*- ，python文件为utf-8格式，否则无法写入中文注释。
#     (3)  GPIO.setmode(GPIO.BCM)，采用bcm编号方式。