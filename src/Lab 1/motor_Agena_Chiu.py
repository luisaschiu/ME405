import utime
import pyb
    
class MotorDriver:  

    def __init__(self, en_pin, in1pin, in2pin, timer):
        # Defines pin variables for the enable pin on the Nucleo
        self.EN = pyb.Pin(en_pin, mode = pyb.Pin.OUT_OD,
                          pull = pyb.Pin.PULL_UP)
        
        # Defines the timer variable for the motor.
        self.tim = pyb.Timer(timer, freq = 20000)
        
        # Defines the pin variables to recieve the duty cycles.
        self.pin1 = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        self.pin2 = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        
        # Define two channel variables.
        self.ch1 = self.tim.channel(1, mode = pyb.Timer.PWM,
                                    pin = self.pin1)
        self.ch2 = self.tim.channel(2, mode = pyb.Timer.PWM,
                                    pin = self.pin2)
        print ('Creating a motor driver')
        
    def enable(self):
        self.EN.high()
        
    def disable(self):
        self.EN.low()
        
    def set_duty_cycle(self, duty):
        if duty > 0:
            self.ch1.pulse_width_percent(duty)
            self.ch2.pulse_width_percent(0)
        elif duty < 0:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(-duty)  
        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0) 
            
        print ('Setting duty cycle to ' + str (duty))

class EncoderDriver:  

    def __init__(self, in1pin, in2pin, timer):
        
        # Defines the timer variable for the motor.
        self.tim = pyb.Timer(timer, prescaler = 0, period = 65535)
        
        # Defines the pin variables to recieve the duty cycles.
        self.pin1 = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        self.pin2 = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        
        # Define two channel variables.
        self.ch1 = self.tim.channel(1, pyb.Timer.ENC_AB,
                                    pin = self.pin1)
        self.ch2 = self.tim.channel(2, pyb.Timer.ENC_AB,
                                    pin = self.pin2)
        self.pos = 0
        self.past = 0
    
    def read(self):
        ''' @brief          Reads the encoder position and returns the values.
            @details        Position is found without encoder overflow.
            @return          The position of the encoder.
        '''
        self.current = self.tim.counter()
        self.delta = self.current - self.past
        if self.delta < -32768:
            self.delta += 65536
        elif self.delta > 32768:
            self.delta -= 65536
        self.pos += self.delta
        self.past = self.current
        return self.pos

    def zero(self):
        self.pos = 0   
    
