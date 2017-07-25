#!/usr/bin/env python

import argparse
import serial
import time
import TekFFM
import motor_functions as mf
import numpy as np
import sys

# Argument Parsing
# Argument Parsing
parser = argparse.ArgumentParser(
    description='Move motors to n discrete points on an LAPPD channel to take data')
parser.add_argument(
    'n', type=int, help='The number of samples to be taken on this channel')
parser.add_argument('-d', '--data', action='store_true',
                    help='Take data using the Tek oscilliscope')
parser.add_argument('-i', '--init', action='store_true',
                    help='Initialize the IPC controller')
args = parser.parse_args()

# Initialize the motors
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200, xonxoff=True)
if(args.init):
    mf.init(ser)

# Move the motor
start_tick = 20000
end_tick = 540000  # Motor encoder ticks #TODO


ser.write('ma 0 {}\n'.format(start_tick).encode())
time.sleep(1)
steps = np.linspace(start_tick, end_tick, args.n, dtype='int')
print(steps)
mf.stop(ser)

for i in range(args.n):
    step = steps[i]
    print('Stop: {}'.format(i))
    # sys.stdout.flush()
    ser.write('ma 0 {}\n'.format(step).encode())
    time.sleep(10)
    mf.stop(ser)
    # Take Data #TODO
    if args.data and not(i == 6 or i == 8):
        TekFFM.take_data('C:/6.30.17_testdata/No Filter', '2700_2600_1600_stop'+str(i), 10)

print('Finished')
ser.write('ma 0 {}\n'.format(start_tick).encode())
ser.close()
