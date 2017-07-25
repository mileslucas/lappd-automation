#!/usr/bin/env python
import vxi11
import argparse
import datetime
import sys
import time

def take_data(folder, filename, nacq):
    # if '/' in folder or filename:
    #     print('Data will not be saved if parent directories do not exist')

    inst_ip = '192.168.2.152'


    # Set up instrument
    scope = vxi11.Instrument(inst_ip);
    print(scope.ask('*IDN?'))

    # Create Folder for data
    scope.write('FILES:MKD \'{}\''.format(folder))

    # Set up fastframe and scope settings
    scope.write('HOR:MAIN:SCA 10e-9') # 10 ns
    scope.write('HOR:FAST:STATE 1')
    scope.write('HOR:FAST:COUN 1000')

    # Get acquisitions
    for i in range(nacq):
        print('\nStarting acquisition {}/{} ...'.format(i + 1, nacq))
        scope.write('ACQ:STATE RUN')
        while(int(scope.ask('ACQ:STATE?'))):
            time.sleep(1)
        print('Data acquired, now writing...')
        scope.write('SAVE:WAVE ALL, \'{}/{}_{}.wfm\''.format(folder, filename, i))

        time.sleep(20)
        print('Finished')

    print('\nFinished\nFiles stored in \'{}/\' on scope'.format(folder))

if __name__=='__main__':
    # Argument Parsing
    parser = argparse.ArgumentParser(description='Take Tek Oscilliscope data remotely')
    parser.add_argument('fold', default=datetime.date, help='The folder name for the saved oscilliscope data')
    parser.add_argument('volt', nargs=3, type=int, help='The voltages used on the HV stack')
    parser.add_argument('nacq', type=int, help='The number of fastframe acquisitions to take')
    parser.add_argument('-la', '--laser', type=int, default=100, help='The frequency of the laser')
    parser.add_argument('-fil', '--filter', type=float, help='The neutral density of the filter applied to laser beam')
    args = parser.parse_args()

    fold = 'C:/' + args.fold
    filename = '{}_{}_{}_{}Hz'.format(args.volt[0], args.volt[1], args.volt[2], args.laser)
    if(args.filter): filename += '_ND{}'.format(args.filter)

    take_data(fold, filename, args.nacq)
