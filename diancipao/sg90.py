
import RPi.GPIO as GPIO
import time


class Servo(object):
    def __init__(self, signal):
        self.signal = signal
        GPIO.setup(signal, GPIO.OUT)
        self.frequency = 50
        self.pwm = GPIO.PWM(self.signal, self.frequency)
        # 设置输出模式
        # PWM信号频率（1000/周期T）
        # 创建PWM对象，并设置频率为50
        self.pwm.start(0)
    def set(self, direction=0):
        duty = (1 / 18) * direction + 2.5
        self.pwm.ChangeDutyCycle(duty)
    def qset(self,direction=0):
        duty = (1 / 18) * direction + 2.5
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.2)
        self.pwm.ChangeDutyCycle(0)
    def stop(self):
        self.pwm.stop()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    try:
        # 启动PWM，并设置初始占空比0
        s = Servo(13)
        while True:
            direction = float(input("Pleas input a direction between 0 an 180:"))
            s.qset(direction)
    except Exception as e:
        print('quit', e)

    finally:
        # 停止PWM
        s.stop()
        # 结束进程，释放GPIO引脚
        GPIO.cleanup()
