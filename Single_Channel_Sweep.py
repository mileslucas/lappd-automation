#!/usr/bin/env python

import argparse
import serial
import time
import TekFFM

# Argument Parsing
# Argument Parsing
parser = argparse.ArgumentParser(description='Move motors to n discrete points on an LAPPD channel to take data')
parser.add_argument('n', type=int, help='The number of samples to be taken on this channel')
parser.add_argument('-i', '--init', action='store_true', help='Initialize the IPC controller')
args = parser.parse_args()

# Initialize the motors
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, xonxoff=True)
if(args.init):
    print('Initializing')
    ser.write(b'jmp \n')
    time.sleep(15)

# Zero the motors
# TODO

# Move the motors
ser.write(b'mc 0 0\n')
ser.write(b'mc 1 0\n')

plate_width = 544990 # Motor encoder ticks #TODO
step = int(plate_width / args.n)
for i in range(args.n):
    print('Stop: {}'.format(i))
    ser.write('mr 0 {}\n'.format(step).encode())

    #Take Data #TODO
    TekFFM.take_data()

print('Finished')
ser.write(b'ma 0 0\n')
ser.write(b'ma 1 0\n')

ser.close()
