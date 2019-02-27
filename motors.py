import serial
import time
import logging
import argparse

VELOCITY=13000 #ticks per second

class Motors():
    '''
    This class wraps all the serial commands for the LAPPD motors. It should not be directly instantiated.
    Instead a MotorConnection should be established using the with directive
    '''
    def __init__(self, port='/dev/ttyUSB0'):
        self.ser = serial.Serial(port, baudrate=19200, xonxoff=False)
        self.log = logging.getLogger(self.__class__.__name__)

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
            self.log.info('Connecting', end='')
            self.ser.write(b'jmp 16\n')
            for i in range(3):
                self.log.info('.', end='')
                time.sleep(5)
        except serial.SerialException:
            self.log.debug('Port Already Opened')
        self.log.info('Connected')

    def disconnect(self):
        '''
        Disconnect the serial connection
        '''
        self.ser.close()
        self.log.info('Disconnected')

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
        self.moveto(motor, 0)

    def get_position(self, motor='all'):
        """
        Returns the current position of the given motor

        Parameters
        ----------
        motor : int or 'all', optional
            The motor to query. 0 is parallel, 1 is transverse, if 'all' will return both
            as a tuple. Default is 'all'

        Returns
        -------
        pos : int or tuple
            if motor is 'all', will return tuple corresponding to 
            (parallel position, transverse position).
        """

        if isinstance(motor, int):
            self.ser.write('ma {}\r'.format(motor).encode())
            self.ser.readline()
            return int(self.ser.readline().strip())
        elif motor == 'all':
            self.ser.write('ma 0\r'.encode())
            self.ser.readline()
            xpos = int(self.ser.readline().strip())
            self.ser.write('ma 1\r'.encode())
            self.ser.readline()
            ypos = int(self.ser.readline().strip())
            return xpos, ypos
        else:
            raise ValueError('Improper motor given: {}'.format(motor))

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
        cur_pos = self.get_position(motor)
        self.ser.write('ma {} {}\n'.format(motor, position).encode())
        self.ser.readline()
        self.ser.readline()
        delay = abs(cur_pos - position) / VELOCITY
        time.sleep(delay)
    
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
        self.ser.readline()
        self.ser.readline()
        delay = distance / VELOCITY
        time.sleep(delay)

    def calibrate(self, motor, position):
        """
        Sets the absolute position for the given motor

        Parameters
        ----------
        motor : int
            The motor to move. 0 is parallel, 1 is transverse
        position : int
            The encoder position to set as current
        """
        self.ser.write('mc {} {}\n'.format(motor, position).encode())
        self.ser.readline()
        self.ser.readline()

def find_lims(parallel=True, transverse=True, recenter=True):
    """
    This function starts a feedback loop to determine the limits of the 
    transverse and parallel stages

    Parameters
    ----------
    parallel : bool, optional
        If True, will find limits for the parallel stage. Default is True
    transverse : bool, optional
        If True, will find limits for the transverse stage. Default is True
    recenter : bool, optional
        If True, will set the left parallel limit to encoder position 0 and
        the median of the transverse limits to 0. Default is True
    """
    lims = []
    with Motors() as m:
        if parallel:
            print('Begin finding left limit')
            while True:
                print('Current position: {}'.format(m.get_position(0)))
                cont = input('Move left? (y/[n] or ticks): ')
                try:
                    cont = int(cont)
                    m.move(0, -cont)
                except ValueError:
                    if cont.lower() in ['y', 'yes','t', 'true']:
                        m.move(0, -1000)
                    else:
                        break
            if recenter:
                m.calibrate(0, 0)
            left_lim = m.get_position(0)
            print('Begin finding right limit')
            while True:
                print('Current position: {}'.format(m.get_position(0)))
                cont = input('Move right? (y/[n] or ticks): ')
                try:
                    cont = int(cont)
                    m.move(0, cont)
                except ValueError:
                    if cont.lower() in ['y', 'yes','t', 'true']:
                        m.move(0, 1000)
                    else:
                        break
            right_lim = m.get_position(0)
            plim = (left_lim, right_lim)
            print('Parallel limits: {}'.format(plim))
            lims.append(plim)
        
        if transverse:
            print('Begin finding far limit')
            while True:
                print('Current position: {}'.format(m.get_position(1)))
                cont = input('Move farther? (y/[n] or ticks): ')
                try:
                    cont = int(cont)
                    m.move(1, -cont)
                except ValueError:
                    if cont.lower() in ['y', 'yes','t', 'true']:
                        m.move(1, -1000)
                    else:
                        break
            far_lim = m.get_position(1)
            print('Begin finding near limit')
            while True:
                print('Current position: {}'.format(m.get_position(1)))
                cont = input('Move closer? (y/[n] or ticks): ')
                try:
                    cont = int(cont)
                    m.move(1, cont)
                except ValueError:
                    if cont.lower() in ['y', 'yes','t', 'true']:
                        m.move(1, 1000)
                    else:
                        break
            near_lim = m.get_position(1)
            if recenter:
                diff = near_lim - far_lim
                m.calibrate(1, diff // 2)
                tlim = (-diff // 2, diff // 2)
            else:
                tlim = (far_lim, near_lim)
            print('Transverse limits: {}'.format(tlim))
            lims.append(plim)

    if len(lims):
        return lims
            
def interface():
    """
    This function acts as a terminal console for the motors
    """
    with Motors() as m:
        while True:
            command = input('Current {} @> '.format(m.get_position()))
            tokens = command.split()
            if len(tokens) == 0:
                continue
            if tokens[0] == 'ma':
                if len(tokens) == 2:
                    print(m.get_position(int(tokens[1])))
                else:
                    m.moveto(int(tokens[1]), int(tokens[2]))
            elif tokens[0] == 'mr':
                m.move(int(tokens[1]), int(tokens[2]))
            elif tokens[0] == 'mc':
                m.calibrate(int(tokens[1]), int(tokens[2]))
            elif tokens[0] in ['as', 'stop']:
                m.allstop()
            elif tokens[0] in ['quit', 'exit']:
                break
            else:
                print('Invalid input')

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--console', action='store_true', help='Run the motor interface console')
    parser.add_argument('-l', '--limit', action='store_true', help='Run the motor limit finding script')
    parser.add_argument('--xlimit', action='store_true', help='run parallel motor limit script')
    parser.add_argument('--ylimit', action='store_true', help='run transverse motor limit script')
    args = parser.parse_args()
    if args.limit:
        find_lims()
    elif args.xlimit:
        find_lims(transverse=False)
    elif args.ylimit:
        find_lims(parallel=True)
    if args.console:
        interface()
