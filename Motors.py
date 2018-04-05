import serial
import time


class Motors():
    def __init__(self, dev='/dev/ttyUSB0', baudrate=19200, xonxoff=True):
        self.ser = serial.Serial(dev, baudrate=baudrate, xonxoff=xonxoff)
        print('Connecting...', end=' ')
        self.ser.write(b'jmp 16\n')
        time.sleep(15)
        print('connected')
    
    def __del__(self):
        self.allstop()
        self.ser.close()

    @classmethod
    def __enter__(cls):
        return cls()

    @classmethod
    def __exit__(cls)
        del cls

    def allstop(self):
        self.stop(0)
        self.stop(1)

    def park(self):
        self.reset(0)
        self.reset(1)
        
    def reset(self, motor):
        self.move(motor, 0)

    def moveto(self, motor, position):
        self.ser.write('ma {} {}\n'.format(motor, position).encode())
    
    def stop(self, motor):
        self.move(motor, 0)

    def move(self, motor, distance):
        self.ser.write('mr {} {}\n'.format(motor, distance).encode())

if __name__=='__main__':
    with Motors() as m:
        try:
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
        except KeyboardInterrupt:
            m.allstop()