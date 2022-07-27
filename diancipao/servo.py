import RPi.GPIO as GPIO
import sg90
import pygame
import time


GPIO.setmode(GPIO.BCM)
sx = sg90.Servo(6)
sy = sg90.Servo(13)
x = 90
y = 60
sx.set(x)
sy.set(y)
try:
    s = pygame.display.set_mode((10, 10))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    print("右")
                    x += 5
                    sx.set(x)
                if event.key == pygame.K_UP:
                    print("上")
                    y += 5
                    sy.qset(y)
                if event.key == pygame.K_DOWN:
                    print("下")
                    y -= 5
                    sy.qset(y)
                if event.key == pygame.K_LEFT:
                    print("左")
                    x -= 5
                    sx.set(x)
                if x < 10:
                    x = 10
                elif x > 150:
                    x = 150
                if y < 25:
                    y = 25
                elif y > 125:
                    y = 125
                print('x=%d' % x)
                print('y=%d' % y)

except KeyboardInterrupt:
    print('quit')
sx.close()
GPIO.cleanup()

