"""!
@file main.py
This is the main file for Lab 4, it contains a program that measures voltage and prints to the
serial port.
@author Corey Agena
@author Luisa Chiu
@date 2-14-2022
"""

import pyb
import utime
import task_share

class Interrupt:
    '''! 
    This class implements an interrupt to measure the voltage at the specified frequency. 
    '''
    def __init__(self):

        ## A pin variable to recieve the duty cycles.
        self.pinC1 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
        self.pinC0 = pyb.Pin(pyb.Pin.cpu.C0, pyb.Pin.IN)
        
        ## A variable for the analog to digital conversion of pin C0.
        self.adc = pyb.ADC(self.pinC0)
        
        ## A queue that holds unsigned short (16-bit) integers.
        self.my_queue = task_share.Queue('h', 1000, name="My Queue")
        
        ## A variable that represents the number of runs.
        self.runs = 0
        
        ## A variable that indicates the end of the loop.
        self.end_flag = 0
        
        ## A variable for time.
        self.time = 0

    def read_adc(self,IRQ_src):
        if self.runs < 1500:
            v_out = self.adc.read()
            # Somewhere in one task, put data into the queue
            self.my_queue.put (v_out,in_ISR = True)
            self.runs += 1
        else:
            self.end_flag = 1
            
    def step(self):
        self.pinC1.high()
        while self.my_queue.any():
            utime.sleep_ms(1)
            print('{:},{:}'.format(self.time,self.my_queue.get(in_ISR = True)))
            self.time += 1
        if self.end_flag == 1:
            self.my_queue.put(-99,in_ISR = True)
            print(self.my_queue.get(in_ISR = True))
            self.pinC1.low()

if __name__ == '__main__':
    ## The timer variable for the motor.
    tim = pyb.Timer(1, freq = 1000)
    ## Object created for the interrupt class.
    interrupt = Interrupt()
    tim.callback(interrupt.read_adc)
    utime.sleep_ms(5)
    interrupt.step()
    
