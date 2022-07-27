import  time
import board
import busio
import adafruit_vl53l0x

I2C = busio.I2C(board.SCL, board.SDA)
vl53l0x = adafruit_vl53l0x.VL53L0X(I2C)
vl53l0x.measurement_timing_budget = 200000

def detect():
    return vl53l0x.range
   
if __name__ =='__main__':
    while True:
        print(detect())

