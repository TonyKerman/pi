#!/usr/bin/python
#_*_ coding:utf-8 _*_
import RPi.GPIO as GPIO
import time 

LED = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED,GPIO.LOW)
try:
    while True:
        f = int(input("输入频率"))
        t = (1/f)/2
        print(t)
        for _ in range(f):
            GPIO.output(LED,GPIO.HIGH)
            time.sleep(t)
            GPIO.output(LED,GPIO.LOW)
            time.sleep(t)
except:
    print("over")
GPIO.cleanup()
