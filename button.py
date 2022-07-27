#!/usr//bin/python
#_*_ coding: utf-8 _*_
import RPi.GPIO as GPIO
import time

KEY = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY, GPIO.IN,GPIO.PUD_UP)#设置上拉模式,断开时为高电平
while True:
    time.sleep(0.05)
    if GPIO.input(KEY) == 0:
        print("PRESS")
    else:
        print("not PRESS")

