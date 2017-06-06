#!/usr/bin/env python

import argparse
import serial
import time
import TekFFM
import motor_functions as mf

# Argument Parsing
# Argument Parsing
parser = argparse.ArgumentParser(description='Move motors to n discrete points on an LAPPD channel to take data')
parser.add_argument('n', type=int, help='The number of samples to be taken on this channel')
parser.add_argument('-d', '--data', action='store_true', help='Take data using the Tek oscilliscope')
parser.add_argument('-i', '--init', action='store_true', help='Initialize the IPC controller')
args = parser.parse_args()

# Initialize the motors
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, xonxoff=True)
if(args.init):
    mf.init(ser)

# Zero the motors
# TODO

# Move the motors
ser.write(b'mc 0 0\n')
ser.write(b'mc 1 0\n')

plate_width = 545000 # Motor encoder ticks #TODO
step = int(plate_width / args.n)
TekFFM.take_data('Delete_this', '1_2_3___0', 1)
for i in range(args.n):
    print('Stop: {}'.format(i))
    ser.write('mr 0 {}\n'.format(step).encode())

    #Take Data #TODO
    TekFFM.take_data('C:/Delete_this', '1_2_3__'+str(i+1), 1)

print('Finished')
mf.reset(ser)

ser.close()
