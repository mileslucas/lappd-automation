import serial
import time


class Motors():
    '''
    This class wraps all the serial commands for the LAPPD motors. It should not be directly instantiated.
    Instead a MotorConnection should be established using the with directive
    '''
    def __init__(self, port='/dev/ttyUSB0'):
        self.ser = serial.Serial(port, baudrate=19200, xonxoff=False)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.allstop()
        self.disconnect()
    
    def connect(self):
        '''
        Connects to the serial port given and issues jmp 16 every time
        '''
        try:
            self.ser.open()
        except serial.SerialException:
            print('Port Already Opened')
        print('Connecting...', end=' ')
        self.ser.write(b'jmp 16\n')
        time.sleep(15)
        print('connected')

    def disconnect(self):
        '''
        Disconnect the serial connection
        '''
        self.ser.close()    

    def allstop(self):
        '''
        Stop all motor motion
        '''
        self.stop(0)
        self.stop(1)

    def park(self):
        '''
        Move both motors to (0, 0)
        '''
        self.reset(0)
        self.reset(1)
        
    def reset(self, motor):
        '''
        Moves the given motor to its 0 position

        Params
        ------
        motor (int):
            0 or 1 for the x or y stage motor
        '''
        self.move(motor, 0)

    def moveto(self, motor, position):
        '''
        Moves the given motor to an absolute position

        Params
        ------
        motor (int):
            0 or 1 for the x or y stage motor
        position (int):
            the absolute motor position
        '''
        self.ser.write('ma {} {}\n'.format(motor, position).encode())
    
    def stop(self, motor):
        '''
        Stops the motion of the given motor

        Params
        ------
        motor (int):
            0 or 1 for the x or y stage motor
        '''
        self.move(motor, 0)

    def move(self, motor, distance):
        '''
        Moves the given motor to a relative position

        Params
        ------
        motor (int):
            0 or 1 for the x or y stage motor
        position (int):
            the relative motor position
        '''
        self.ser.write('mr {} {}\n'.format(motor, distance).encode())

if __name__=='__main__':
    with Motor() as m:
        while True:
            cmd = input('@ ')
            if cmd=='left':
                m.move(0, -10000)
            elif cmd=='right':
                m.move(0, 10000)
            elif cmd=='stop':
                m.stop(0)
            else:
                print('Invalid input')
