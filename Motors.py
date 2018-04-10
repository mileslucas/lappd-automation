import serial
import time

class MotorConnection():
    def __enter__(self):
        ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, xonxoff=False)
        self.motor = Motors(ser)
        self.motor.connect()
        return self.motor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.motor.allstop()
        self.motor.disconnect()


class Motors():
    def __init__(self, ser):
        self.ser = ser
    
    def connect(self):
        try:
            self.ser.open()
        except serial.SerialException:
            print('Port Already Opened')
        print('Connecting...', end=' ')
        self.ser.write(b'jmp 16\n')
        time.sleep(15)
        print('connected')

    def disconnect(self):
        self.ser.close()    

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
    with MotorConnection() as m:
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
