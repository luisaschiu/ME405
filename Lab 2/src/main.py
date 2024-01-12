'''!
@file main.py
This is the main file for Lab 2, where two motor driver and encoder driver objects are created to run functions,
such as setting duty cycles for the motors and printing encoder position.
@author Corey Agena
@author Luisa Chiu
@date 1-26-2022
'''

# Import the required modules to run the motor and encoder 
import motor_agena_chiu
import encoder_agena_chiu
import controller_agena_chiu
import pyb
import utime

if __name__ == '__main__':
    ## A variable that creates a encoder driver for encoder 1.
    encoder_drv1 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    # A variable that creates a encoder driver for encoder 2.
    # encoder_drv2 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.C6, pyb.Pin.cpu.C7, 8)
    ## A variable that creates a motor driver for motor 1.
    motor_drv1 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.A10, pyb.Pin.cpu.B4, pyb.Pin.cpu.B5, 3)
    # A variable that creates a motor driver for motor 2.
    # motor_drv2 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.C1, pyb.Pin.cpu.A0, pyb.Pin.cpu.A1, 5)
    ## A variable that creates a controller driver.
    controller = controller_agena_chiu.ControllerDriver(0, 0)
    # Enable both motors.
    motor_drv1.enable()
    # motor_drv2.enable()
    # Set the duty cycle for both motors.
    ## A variable that creates an empty list to be populated with time data.
    time = []
    ## A variable that creates an empty list to be populated with encoder position data.
    enc_pos = []
    while True:
        ## A variable that requests for proportional gain from the user.
        x = input('Input Kp to run step response, input s to stop: ')
        try:
            float(x)
        except:
            if x == 's':
                motor_drv1.set_duty_cycle(0)
                break
        else:
            ## A variable that requests for set point from the user.
            y = input('Input set point: ')
            controller.set_gain(x)
            controller.set_setpoint(y)
            encoder_drv1.zero()
            ## A variable that initializes the difference between start time and current time.
            difference = 0
            ## A variable that marks the start of the timer.
            start = utime.ticks_ms()
            while difference <= 1000:
                ## A variable that creates a timer which marks the current time.
                current = utime.ticks_ms()
                difference = current - start
                ## A variable that defines duty cycle for the controller's run function.
                duty_cycle = controller.run(encoder_drv1.read())
                motor_drv1.set_duty_cycle(duty_cycle)
                utime.sleep_ms(10)
                time.append(difference)
                enc_pos.append(encoder_drv1.read())
            ## A variable that initializes the index used for printing encoder position.
            i = 0
            motor_drv1.set_duty_cycle(0)
            for x in time:
                print('{:},{:}'.format(time[i],enc_pos[i]))
                i += 1
            break
