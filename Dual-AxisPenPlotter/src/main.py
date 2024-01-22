"""!
@file main.py
This is the main file for Lab 3, it contains a program that runs two motor tasks which includes closed loop control
for each motor. The code was adapted from Dr. Ridgely's basic task example.
@author Corey Agena
@author Luisa Chiu
@date 2-9-2022
"""

# Import the required modules.
import gc
import pyb
import cotask
import encoder_agena_chiu
import motor_agena_chiu
import controller_agena_chiu
import task_share
from pyb import USB_VCP
from nb_input import NB_Input
from micropython import const
import hpgl_agena_chiu
import sys

## State 0 of the user interface task
S0_CALIB            = const(0)
## State 1 of the user interface task
S1_HELP             = const(1)
## State 2 of the user interface task
S2_WAIT_FOR_CHAR    = const(2)
## State 3 of the user interface task
S3_READ             = const(3)
## State 4 of the user interface task
S4_PLOT             = const(4)

## Variable representing the input to the serial port.
nb_in = NB_Input (USB_VCP(), echo=True)   

def task_motor1(duty_cycle = 0):
    '''!
    Task which runs the motor, encoder, and controller drivers to 
    control the duty cycle for motor 1.
    @param duty_cycle The initial cycle of motor 1.
    '''
    while True:
        ## A variable that holds the position of encoder 1.
        enc1 = -encoder_drv1.read()
        ## A variable that defines duty cycle for the run funciton of controller 1.
        duty_cycle = controller_1.run(enc1, 100)
        motor_drv1.set_duty_cycle(duty_cycle)
        ## A flag that indicates that motor 1 reached the desired setpoint within the set limits.
        flag1 = controller_1.flag()
        if flag1 == True:
            move_flag1.put(1)
            flag1 = False
        yield()

def task_motor2(duty_cycle = 0):
    '''!  
    Task which runs the motor, encoder, and controller drivers to 
    control the duty cycle for motor 2.
    @param duty_cycle The initial cycle of motor 2.
    '''
    while True:
        ## A variable that holds the position of encoder 2.
        enc2 = -encoder_drv2.read()
        ## A variable that defines duty cycle for the run funciton of controller 2.
        duty_cycle = controller_2.run(enc2,75)
        motor_drv2.set_duty_cycle(-duty_cycle)
        ## A flag that indicates that motor 2 reached the desired setpoint within the set limits.
        flag2 = controller_2.flag()
        if flag2 == True:
            move_flag2.put(1)
            flag2 = False
        yield()
        
def input_task():
    '''! 
    Task which runs the non-blocking input object quickly to ensure
    that keypresses are handled not long after they've occurred.
    '''
    while True:
        nb_in.check ()
        yield ()

def task_user(state = S0_CALIB):
    '''!  
    Task which includes multiple states that guide the user through the
    use of the pen plotter system. This includes: calibration, help, read, and
    plot states.
    @param state The initial state of the user task.
    '''
    while True:
        if state == S0_CALIB:
            sol.low()
            print('\r\nReady to Calibrate? Press c and Enter')
            if nb_in.any ():
                ## Variable for the character read from the serial port.
                char_in = nb_in.get()
                if char_in == 'c':
                    print('\r\nCalibrating')
                    ## Pin variable for the limit switch.
                    pin = pyb.Pin(pyb.Pin.cpu.A0, pyb.Pin.IN)
                    ## ADC variable for the pin above.
                    adc = pyb.ADC(pin)
                    ## Value read from the ADC.
                    val = adc.read()
                    if val > 10:
                        motor_drv1.set_duty_cycle(-100)
                        while True:
                            val = adc.read()
                            if val <= 5:
                                encoder_drv1.zero()
                                encoder_drv2.zero()
                                motor_drv1.set_duty_cycle(0)
                                state = S1_HELP
                                break
                    else:
                        encoder_drv1.zero()
                        encoder_drv2.zero()
                        motor_drv1.set_duty_cycle(0)
                        state = S1_HELP
                        
        elif state == S1_HELP:
            print('\n\rWelcome, press:'
                  '\n\'p\' to plot from a HPGL file'
                  # '\n\'l\' to prompt the user to enter a setpoint for'
                  # ' lead screw'
                  '\n\'q\' to quit'
                  '\n\'h\' return to the welcome screen')
            state = S2_WAIT_FOR_CHAR
            
        elif state == S2_WAIT_FOR_CHAR:
            if nb_in.any ():
                ## Variable for the character read from the serial port.
                char_in = nb_in.get()
                if char_in == 'q':
                    motor_drv1.set_duty_cycle(0)
                    motor_drv2.set_duty_cycle(0)
                    print('\r\nThe program was exited')
                    sys.exit()
                elif char_in == 'h':
                    state = S1_HELP
                    print('\r\n')
                # elif char_in == 'l':
                #     print('\r\nLinear position adjustment')
                #     if nb_in.any():
                #         char_in = nb_in.get()
                #         if char_in == '+':
                #             print('\r\nPositve Linear Motion')
                #             motor_drv1.set_duty_cycle(100)
                #         elif char_in == '-':
                #             print('\r\nNegative Linear Motion')
                #             motor_drv1.set_duty_cycle(-100)
                #         elif char_in == 's':
                #             print('\r\nStopped Motion')
                #             motor_drv1.set_duty_cycle(0)
                elif char_in == 'p' or char_in == 'P':
                    state = S3_READ
                    i = 0
        
        elif state == S3_READ:
            if i == 0:
                print('\r\nEnter hpgl file name:')
            elif nb_in.any ():
                ## Variable holding the file name to be read.
                filename = nb_in.get()
                print('\r\n',filename)
                if '.hpgl' in filename or '.HPGL' in filename:
                    hpgl.read(filename)
                    state = S4_PLOT
                    ## Counter for the amount of times ran through the plot state.
                    plot_count = 0
                    move_flag1.put(1)
                    move_flag2.put(1)
                    print('Plotting')
                else:
                    print('\r\ninvalid file name')
            i += 1
        
        elif state == S4_PLOT:
            mflag1 = move_flag1.get()
            mflag2 = move_flag2.get()
            if mflag1 and mflag2:
                print('in loop')
                move_flag1.put(0)
                move_flag2.put(0)
                hpgl.process(plot_count)
                ## The ouptut from hpgl.run()
                output = hpgl.run(plot_count)
                ## The command or number in the 0 position of the output list.
                x = output[0]
                try:
                    float(x)
                except:
                    if x == 'PU':
                        print('ho')
                        sol.low()
                        plot_count += 1
                        move_flag1.put(1)
                        move_flag2.put(1)
                    elif x == 'PD':
                        print('he')
                        sol.high()
                        plot_count += 1
                        move_flag1.put(1)
                        move_flag2.put(1)
                    elif x == 'IN' and plot_count > 0:
                        print('Done')
                        state = S1_HELP
                    else:
                        print('hi')
                        move_flag1.put(1)
                        move_flag2.put(1)
                        plot_count += 1
                else:
                    print('uh')
                    if output[1]:
                        print('uhh')
                        ## The number in the second position of the output list.
                        y = output[1]
                        controller_1.set_setpoint(x)
                        controller_2.set_setpoint(y)
                        plot_count += 1
        yield ()

# This code creates driver and task objects required for the pen ploter.
# It also runs a task scheduler that allows multitasking.
if __name__ == "__main__":
    ## A variable that creates a encoder driver for encoder 1.
    encoder_drv1 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    ## A variable that creates a encoder driver for encoder 2.
    encoder_drv2 = encoder_agena_chiu.EncoderDriver(pyb.Pin.cpu.C6, pyb.Pin.cpu.C7, 8)
    ## A variable that creates a motor driver for motor 1.
    motor_drv1 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.A10, pyb.Pin.cpu.B4, pyb.Pin.cpu.B5, 3)
    ## A variable that creates a motor driver for motor 2.
    motor_drv2 = motor_agena_chiu.MotorDriver(pyb.Pin.cpu.C1, pyb.Pin.cpu.A0, pyb.Pin.cpu.A1, 5)
    ## A variable that creates a controller driver for motor 1.
    controller_1 = controller_agena_chiu.ControllerDriver(0, 0)
    ## A variable that creates a controller driver for motor 2.
    controller_2 = controller_agena_chiu.ControllerDriver(0, 0)
    # Enable both motors.
    motor_drv1.enable()
    motor_drv2.enable()
    
    ## A variable that creates a hpgl driver to read the hpgl file.
    hpgl = hpgl_agena_chiu.hpglDriver()
    
    ## A shared variable that indicates that motor 1 arrived at the desired position.
    move_flag1 = task_share.Share('B', name = 'Movement Flag 1')
    ## A shared variable that indicates that motor 2 arrived at the desired position.
    move_flag2 = task_share.Share('B', name = 'Movement Flag 2')
    
    sol = pyb.Pin(pyb.Pin.cpu.B3, pyb.Pin.OUT_PP)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()
    
    # Set the controller gains and initial setpoints for both motors.
    controller_1.set_gain(0.1)
    controller_1.set_setpoint(0)
    controller_2.set_gain(0.1)
    controller_2.set_setpoint(0)
    
    # Set both encoders to zero.
    encoder_drv1.zero()
    encoder_drv2.zero()
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task_motor1, name = 'Task_Motor1', priority = 2, 
                         period = 10, profile = True, trace = False)
    task2 = cotask.Task (task_motor2, name = 'Task_Motor2', priority = 2, 
                         period = 10, profile = True, trace = False)
    in_task = cotask.Task (input_task, name = 'Input Task', priority = 1, 
                           period = 50, profile = True, trace = False)
    task_user = cotask.Task (task_user, name = 'User Task', priority = 0, 
                           period = 100, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (in_task)
    cotask.task_list.append (task_user)
    while True:
        # Run the scheduler with the chosen scheduling algorithm. 
        cotask.task_list.pri_sched ()
    
