'''!
@file hpgl_agena_chiu.py
This is the file that serves as a module to be imported in main. It creates a class for a hpgl
driver that opens and reads from a specified hpgl file.
@author Corey Agena
@author Luisa Chiu
@date 1-27-2022
'''

# Import the required modules.
import math

class hpglDriver:  
    '''! 
    This class implements a hpgl driver to open and read from a hpgl file. 
    '''
    def __init__(self):
        '''! 
        Creates a hpgl driver and initializes a few important variables that
        will be used throughouth the class.
        '''
        ## A pre-allocated list used for storing the data read from the hpgl file.
        self.operation = [0]*500
        
        ## A variable that represents the setpoint of the first motor.
        self.x = 0
        
        ## A variable that represents the setpoint of the second motor.
        self.y = 0
        
    def read(self,filename):
        '''!
        A generator that reads from the hpgl file and does the initial
        processing of the data.
        @param filename The name of the hpgl file.
        @return operation The list holding the data post process.
        '''
        
        ## A string that holds the raw data read from the hpgl file.
        raw_st = ''
        
        ## A string that holds the data after the initial process.
        st = ''
        
        ## A flag that indicates a comma was read in a pen up operation.
        cu = 0
        
        ## A flag that indicates a comma was read in a pen down operation.
        cd = 0
        
        ## A counter that increases as values are added to the operation list.
        op_count = 0
        
        with open(filename) as f:
            ## A variable that reads lines of code from the Nucleo.
            raw_data = f.readlines()
            data = ''.join(raw_data)
            ## A variable that separates strings into ordered lists of data.
            data = data.split(';')
            for x in data:
                try:
                    float(x)
                except:
                    if 'PU' in x:
                        self.operation[op_count] = 'PU'
                        op_count += 1
                        raw_st = x
                        for y in raw_st:
                            try:
                                float(y)
                            except:
                                if y == ',' and cu == 0:
                                    st += ','
                                    cu = 1
                                elif y == ',' and cu == 1:
                                    self.operation[op_count] = st
                                    op_count += 1
                                    cu = 0
                                    st = ''
                            else:
                                st += y
                        self.operation[op_count] = st
                        op_count += 1
                        st = ''
                        cu = 0
                    elif 'PD' in x:
                        self.operation[op_count] = 'PD'
                        op_count += 1
                        raw_st = x
                        for y in raw_st:
                            try:
                                float(y)
                            except:
                                if y == ',' and cd == 0:
                                    st += ','
                                    cd = 1
                                elif y == ',' and cd == 1:
                                    self.operation[op_count] = st
                                    cd = 0
                                    st = ''
                                    op_count += 1
                            else:
                                st += y
                        self.operation[op_count] = st
                        st = ''
                        cd = 0
                        op_count += 1
                    else:
                        self.operation[op_count] = x
                        op_count += 1         
        return self.operation
    
    def process(self,i):
        '''!
        A generator that processes the data read from the hpgl file into data
        more readable by the plotter itself.
        @param i A counter that determines the amount of times that the generator ran.
        @return x Both motor setpoints after this stage of the processing.
        '''
        ## A string variable that is appended to as new characters are read.
        st = ''
        
        ## A variable that holds the data from the operation list directly from the hpgl file.
        var = str(self.operation[i])
        
        if ',' in var:
            for y in var:
                try:
                    float(y)
                except:
                    if y == ',':
                        self.x = st
                        st = ''
                else:
                    st += y
            self.y = st
            st = ''
        else:
            for y in str(self.operation[i]):
                st += y
            self.x = st
            st = ''
        return [self.x, self.y]
            
    def run(self,i):
        '''!
        A generator that scales the data from the previous step in processing
        to make it applicable to the physical system.
        @param i A counter that determines the amount of times that the generator ran.
        @return x Both motor setpoints after this stage of the processing.
        '''        
        try:
            float(self.x)
        except:
            return [self.x,0]
        else:
            ## The scaled x coordinate that converts the hpgl units to inches.
            x_scaled = (int(self.x)/1016) - 3
            ## The scaled y coordinate that converts the hpgl units to inches.
            y_scaled = (int(self.y)/1016)
            ## The radius value used for polar coordinates, derived from the scaled variables.
            r = math.sqrt(x_scaled**2 + y_scaled**2)
            ## The setpoint of the first motor.
            setpoint1 = (r*16384)/0.04167
            ## The setpoint of the second motor.
            setpoint2 = (16384*r*math.acos(x_scaled/r))/(2*3.14)
            self.x = setpoint1
            self.y = setpoint2
            return [self.x,self.y]
    
    def report_x(self):
        '''!
        A function that returns the setpoint of the first motor.
        @return x The setpoint of motor 1.
        ''' 
        return self.x
    
    def report_y(self):
        '''!
        A function that returns the setpoint of the second motor.
        @return y The setpoint of motor 2.
        ''' 
        return self.y
    
    def length(self):
        '''!
        A function that returns the length of the operation list.
        @return length The length of the operation list.
        ''' 
        return len(self.operation)
    
# This code creates a driver object then tests the functions of the hpgl class
# to ensure that it works properly.
if __name__ == "__main__":
    ## Driver object for the hpgl class.
    hpgl = hpglDriver()
    ## Output of the read function.
    operation = hpgl.read('lines.hpgl')
    for i in range(len(operation)):
        hpgl.process(i)
        ## Output of the run function.
        x = hpgl.run(i)
        print(x[0],x[1])