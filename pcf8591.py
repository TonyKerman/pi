import time
import board

import adafruit_pcf8591.pcf8591 as PCF
from adafruit_pcf8591.analog_in import AnalogIn
from adafruit_pcf8591.analog_out import AnalogOut
'''
PCF8591 功能是模拟信号转成数字信号，为树莓派提供了5个模拟输入，1个模拟输出
'''
i2c = board.I2C()
pcf = PCF.PCF8591(i2c)

pcf_in_0 = AnalogIn(pcf, PCF.A0)
pcf_out = AnalogOut(pcf, PCF.OUT)

while True:

    print("Setting out to ", 65535)
    pcf_out.value = 65535
    raw_value = pcf_in_0.value
    scaled_value = (raw_value / 65535) * pcf_in_0.reference_voltage

    print("Pin 0: %0.2fV" % (scaled_value))
    print("")
    time.sleep(1)