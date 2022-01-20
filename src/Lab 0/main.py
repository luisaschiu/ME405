"""!
@file main.py
This file contains code that increases the brightess of an LED to
100% over 5 seconds then returns the brightness to 0% and repeats.
@author Corey Agena
@author Luisa Chiu
@date 06-Jan-2022
"""

import utime

def led_setup():
    """!
    Setup the pin, timer, and timer channel in order to control
    the brightness of the LED.
    """
    # Defines pin variable for PA0 on the Nucleo
    pinA0 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    # Defines a timer variable for timer 2 corresponding to A0.
    tim2 = pyb.Timer (2, freq=20000)
    # Creates a global variable for the channel
    global ch1
    # Defines the channel for timer 2 and pinA0. The PWM is
    # inverted so that the percentage is intuitive.
    ch1 = tim2.channel (1, pyb.Timer.PWM_INVERTED, pin=pinA0)
    
def led_brightness(PWM):
    """!
    Set the pulse width percentage of the LED, which controls
    LED brightness.
    @param PWM The pulse width percentage that correlates with
    the brightness.
    """
    ch1.pulse_width_percent (PWM)
    
if __name__ == '__main__':
    # Calls the led_setup function to create the pin, timer, and
    # channel objects.
    led_setup()
    ## Variable that marks the start of the loop.
    start = utime.ticks_ms()
    ## Variable that represents the time the loop takes to run.
    time = 0
    # This loop creates the variable PWM by finding a percentage
    # of 5 seconds and applies it as the PWM duty cycle. After
    # 5 seconds the brightness is set to zero then the process
    # repeats.
    while True:
        while time < 5000:
            ## Pulse width modulation percentage of the LED.
            PWM = time/5000*100
            led_brightness(PWM)
            ## Variable that represents the time after
            # one iteration of the loop has run.
            current = utime.ticks_ms()
            time = current - start
        led_brightness(0)
        start = utime.ticks_ms()
        time = 0
            
        
        