class EncoderDriver:  

    def __init__(self, timer, pin_IN1, pin_IN2, ch1, ch2):
        
        print('Creating encoder object')
        
        # Defines the timer variable for the motor.
        self.tim = pyb.Timer(timer, prescaler = 0, period = 65535)
        
        # Defines the pin variables to recieve the duty cycles.
        self.pin1 = pyb.Pin(pin_IN1, pyb.Pin.OUT_PP)
        self.pin2 = pyb.Pin(pin_IN2, pyb.Pin.OUT_PP)
        
        # Define two channel variables.
        self.ch1 = self.tim.channel(ch1, pyb.Timer.ENC_AB,
                                    pin = self.pin1)
        self.ch2 = self.tim.channel(ch2, pyb.Timer.ENC_AB,
                                    pin = self.pin2)
        
        self.pos = 0
        self.past = 0
    
    def read(self):
        ''' @brief          Reads the encoder position and returns the values.
            @details        Position is found without encoder overflow.
            @return          The position of the encoder.
        '''
        self.current = self.tim.counter()
        self.dlt = self.current - self.past
        if self.dlt < -32768:
            self.dlt += 65536
        elif self.dlt > 32768:
            self.dlt -= 65536
        self.pos += self.dlt
        self.past = self.current
        return self.pos

    def zero(self):
        self.pos.write(0)
    
    # def get_position(self):
    #     '''@brief           Gets the encoder's position.
    #        @details         Calls the value from update() and returns it.
    #        @return          The position of the encoder.
    #     '''
    #     return self.pos
    
    
if __name__ == '__main__':
    encoder_drv = EncoderDriver(4, 'B6', 'B7', 1, 2)
    while True:
        encoder_drv.update()
        print(encoder_drv.get_position())