#! /usr/bin/python
import serial
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, xonxoff=True)

left_side= 0
right_side = 460000

def left():
    ser.write('ma 0 {}\n'.format(left_side).encode())

def right():
    ser.write('ma 0 {}\n'.format(right_side).encode())

def stop():
    ser.write('mr 0 0\n'.encode())
try:
    while True:
        cmd = input('@ ')
        if cmd=='left':
            left()
        elif cmd=='right':
            right()
        elif cmd=='stop':
            stop()
        else:
            print('Invalid input')
except KeyboardInterrupt:
    stop()
