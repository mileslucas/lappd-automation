#!/usr/bin/env python
import vxi11
import argparse
import datetime
import sys
import time

inst_ip = '192.168.2.152'

# Argument Parsing
parser = argparse.ArgumentParser(description='Take Tek Oscilliscope data remotely')
parser.add_argument('fold', default=datetime.date, help='The folder name for the saved oscilliscope data')
parser.add_argument('volt', nargs=3, type=int, help='The voltages used on the HV stack')
parser.add_argument('nacq', type=int, help='The number of fastframe acquisitions to take')
parser.add_argument('-la', '--laser', type=int, default=100, help='The frequency of the laser')
parser.add_argument('-fil', '--filter', type=float, help='The neutral density of the filter applied to laser beam')

args = parser.parse_args()
filename = '{}_{}_{}_{}Hz'.format(args.volt[0], args.volt[1], args.volt[2], args.laser)
if(args.filter): filename += '_ND{}'.format(args.filter)

# Set up instrument
scope = vxi11.Instrument(inst_ip);
print(scope.ask('*IDN?'))

# Create Folder for data
fold = 'C:/' + args.fold
scope.write('FILES:MKD \'{}\''.format(fold))

# Set up fastframe and scope settings
scope.write('HOR:MAIN:SCA 10e-9') # 10 ns
scope.write('HOR:FAST:STATE 1')
scope.write('HOR:FAST:COUN 1000')

# Get acquisitions
for i in range(args.nacq):
    print('\nStarting acquisition {}/{} ...'.format(i + 1, args.nacq))
    scope.write('SAVE:WAVE ALL, \'{}/{}_{}.wfm\''.format(fold, filename, i))
    print('Data acquired, now writing...')
    time.sleep(20)
    print('Finished')

print('\nFinished\nFiles stored in \'{}/\' on scope'.format(fold))
