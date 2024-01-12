'''!
@file plot_agena_chiu.py
This is the file that writes to the serial port to run step response
tests and plot the results.
@author Corey Agena
@author Luisa Chiu
@date 2-2-2022
'''

# Import modules required to plot.
from matplotlib import pyplot
import serial
import time

# Create a figure to plot to.
pyplot.figure(1)

# Create empty lists.
## A variable that creates an empty list to be populated with time data.
x_val = []
## A variable that creates an empty list to be populated with encoder position data.
y_val = []

# Open the serial port to read from it and plot.
with serial.Serial('COM21', 115200) as f:
    f.write(b'\x03')
    f.write(b'\x04')
    ## A variable used to hold lines read from the serial port.
    text = f.readline()
    ## A variable for the amount of runs in the loop checking for CTRL-B.
    b_runs = 0
    while True:
        if b'CTRL-B' in text:
            f.write(b'\x02')
            f.write(b'\x04')
            break
        else:
            if b_runs == 5:
                break
            b_runs += 1
        text = f.readline()
    time.sleep(0.1)
    print('Creating Plot')

    while True:
        ## A variable that reads lines of code from the Nucleo.
        raw_data = f.readline()
        ## A variable that separates strings into ordered lists of data.
        data = raw_data.split(b',')
        try:
            float(data[0])
            float(data[1])
        except:
            if len(data) >= 2:
                if data[0].strip() == b' ' or data[1].strip() == b' ':
                    continue
                elif data[0].strip().isalpha() == True or data[1].strip().isalpha() == True:
                    continue             
            elif b'-99' in data[0]:
                break
        else:
            x_val.append(float(data[0].strip()))
            y_val.append(float(data[1].strip()))
    # Plot the values read from the serial port.
    pyplot.plot(x_val, y_val)
    # Label both axes.
    pyplot.xlabel('time [ms]')
    pyplot.ylabel('voltage [mV]')
    # Show the plot.
    pyplot.show()
