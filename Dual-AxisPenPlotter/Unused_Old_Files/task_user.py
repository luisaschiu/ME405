""" @file        task_user.py
    @brief       User interface task for the encoders, motors, and controllers.
    @details     Implements a finite state machine to recieve inputs from
                 the keyboard and execute the corresponding task.
    @author      Corey Agena
    @author      Luisa Chiu
    @date        3-7-22
"""

# Import the required modules.
from pyb import USB_VCP
from nb_input import NB_Input
from micropython import const
import task_share
import hpgl_agena_chiu
import math

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

nb_in = NB_Input (USB_VCP(), echo=True)

op_queue = task_share.Queue('B', 1500, name = 'Operation Share')

def input_task():
        """!  Task which runs the non-blocking input object quickly to ensure
        that keypresses are handled not long after they've occurred. """
        while True:
            nb_in.check ()
            yield 0

def task_user(state = S0_CALIB):
     while True:
        if state == S0_CALIB:
            
            state = S1_HELP
            
        elif state == S1_HELP:
            print('\n\rWelcome, press:'
                  '\n\'p\' to plot from a HPGL file'
                  '\n\'d\' to set the both motors to a duty cycle of 0'
                  '\n\'l\' to prompt the user to enter a setpoint for'
                  ' lead screw'
                  '\n\'a\' to prompt the user to enter a setpoint for'
                  ' the wheel'
                  '\n\'q\' to quit'
                  '\n\'h\' return to the welcome screen')
            state = S2_WAIT_FOR_CHAR
            
        elif state == S2_WAIT_FOR_CHAR:
            if nb_in.any ():
                char_in = nb_in.get()
                if char_in == 'q':
                    print('\r\nThe program was exited')
                elif char_in == 'h':
                    state = S1_HELP
                    print('\r\n')
                elif char_in == 'l':
                    print('\r\nLinear position set')
                elif char_in == 'a':
                    print('\r\nAngular position set')
                elif char_in == 'm' or char_in == 'M':
                    print('\r\nPosition set')
                elif char_in == 'p' or char_in == 'P':
                    state = S3_READ
                    i = 0
        
        elif state == S3_READ:
            if i == 0:
                print('\r\nEnter hpgl file name:')
            elif nb_in.any ():
                filename = nb_in.get()
                print('\r\n',filename)
                if '.hpgl' in filename or '.HPGL' in filename:
                    hpgl = hpgl_agena_chiu(filename)
                    hpgl.read()
                else:
                    print('\r\ninvalid file name')
            i += 1
            state = S4_PLOT
        
        elif state == S4_PLOT:
            hpgl.run()
            x = hpgl.report_x()
            y = hpgl.report_y()
            x_scaled = (x/1016) - 3
            y_scaled = (y/1016) + 5.59
            r = math.sqrt(x_scaled^2 + y_scaled^2)
            duty1 = (r*16384)/0.04167
            duty2 = (16384*20.27*math.cosa(x_scaled*r))/2
            lin_set.put(duty1)
            ang_set.put(duty2)
        yield 0

if __name__ == "__main__":
    import cotask

    print ("\033[2JTesting Non-Blocking Input Class")
    in_task = cotask.Task (input_task, name = 'Input Task', priority = 1, 
                           period = 50, profile = True, trace = False)
    task_user = cotask.Task (task_user, name = 'User Task', priority = 2, 
                            period = 500, profile = True, trace = False)
    cotask.task_list.append (in_task)
    cotask.task_list.append (task_user)

    while True:
        try:
            cotask.task_list.pri_sched ()
        except KeyboardInterrupt:
            break

    print ('\n' + str (cotask.task_list))
    ## @endcond
