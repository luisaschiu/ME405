"""!
@file mainpage.py
File that holds the main page.
@mainpage
@section intro Introduction
The term project is to design and build a 2.5 degree of freedom pen plotter.
The plotter was designed, built, and codedwithin a 3 week period. The code will
be explained here.

@section software Software Design
Throughout the quarter, software was developed for motion control,
multitasking, and program organization.There are 8 distinct .py files used for
the control of the pen plotter. The main.py file consists of the different
task generators and a main function portion. The tasks include two motor tasks,
a user task, and a input task. The main program initializes the drivers and 
runs the task manager that allows multitasking. The drivers operate hardware
including the motor and encoder; and also do some stand alone processing in
the form of a closed loop controller and hpgl file reader. More detail on the
driver files can be found at motor_agena_chiu.py, encoder_agena_chiu.py,
controller_agena_chiu.py, and hpgl_agena_chiu.py. The final three files were
provided by Dr. Ridgely. They are the cotask.py, task_share.py, and
nb_input.py. The cotask file allows for multitasking, the task share file
allows the use of shares and queues across tasks, and the nb_input allows the
reading of the serial port using non-blocking methods. The software was 
outlined in the form of a task diagram and multiple state transition
diagrams shown below.

@subsection task Task Diagram
The task diagram below shows how the tasks were implemented with the use of a
single share. The rest of the communication was completed using drivers. There
was a bug in the communication, that can be solved with the implementation of
a queue for each motor. Data allocation errors were apparent and an issue with
adding non-integer values caused attempt at different methods. After reworking
this task diagram it is apparent that in the attempt to fix the errors and
simplify the code the functionality and required components were lost. This
means that with some extra time, work, and the implementation of queues the
final bug could be resolved.
\image html Task_Diagram.png

@subsection user User Task
The user task is run on the microcontroller and it leads the user through the
proper use of the pen plotter. It starts with calibration, moving the pen to
its zero point along the radial direction. Then it prints the help screen with
the different commands that can be input to the serial port. Depending on the
command the help window will be printed again, the entire program will quit, 
or it will continue to the read state. The read state is where the hpgl file
is opened and read from using the hpgl driver. Once the file is found and 
read from then the program transitions to the plot state. This is where the
pen plotter is controlled toward the positions read from the hpgl file. The 
current software structure runs one location at a time, requiring a counter
input into the driver to keep track of which position has already been sent to
the plotter.
\image html User_FSM.png

@subsection motor Motor Task
The motor task has been simplified greatly. It handles the actuation of the
motors, reading from the encoders, and controlling the motors with a closed
loop controller. However, all of this continuously happens and does not
require input until a new setpoint is provided. So there are two states: set
duty and control. The finite state machine starts at set duty if the duty is
not changed then it is considered 0 and the motors are not actuated. If a
setpoint is entered then a new duty cycle will be calculated as a result and
the motors will acuate. When this happens the program enters the control state 
where the controller will approach the setpoint and raise a flag when the
encoders read within the specified tolerances. When the flag is raised then
the program waits for another setpoint and duty cycle.
\image html Motor_FSM.png

@subsection other Other Features
Other features include the solenoid, limit switch, and hpgl driver. The
solenoid is connected to a analog pin that is initialized then set high or low.
Since the position is remembered a task is not required for this piece of
hardware. The limit switch was used in the calibration state of the user task,
where the motor is actuated until the limit switch is hit and sets that point
to zero. The limit switch is connected to a analog pin that is initialized and
read from using the pyb.adc module and stoping the motor when that value
decreased below a set value of 5. Finally the hpgl driver reads the file and
processes the information multiple times to get them in the proper units and
scaled to fit the geometry and mechanics of the physical system.

@author Corey Agena
@author Luisa Chiu
@date Winter 2022
"""