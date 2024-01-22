import pyb
import utime

pin = pyb.Pin(pyb.Pin.cpu.A0, pyb.Pin.IN)
adc = pyb.ADC(pin)
while True:
    val = adc.read()
    print(val)
    utime.sleep(0.5)
    if adc <= 5:
        break
print("ah")