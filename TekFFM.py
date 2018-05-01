#!/usr/bin/env python
import vxi11
import argparse
import datetime
import sys
import time

def take_data(folder, filename, nacq):
    '''
    This function takes data using the tektronix oscilloscope set up in Matt's workspace

    params
    ------
    folder (string):
        This is the folder on the oscope to store the data in. The full folder path should
        be provided, e.g. 'C:/data'. Note that folders cannot be created recursively, so 
        every folder except the last one listed must already exist on the machine
    filename (string):
        This will be the filename to prepend each sample with.
    nacg (int):
        This is the number of fast frame acquisitions to make
    '''

    inst_ip = '192.168.2.152'


    # Set up instrument
    scope = vxi11.Instrument(inst_ip);
    print(scope.ask('*IDN?'))

    # Create Folder for data
    scope.write('FILES:MKD \'{}\''.format(folder))

    # Set up fastframe and scope settings
    # scope.write('HOR:MAIN:SCA 10e-9') # 10 ns
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
    parser.add_argument('folder', default=datetime.date, help='The folder name below "C:/" for the saved oscilliscope data')
    parser.add_argument('filename', help='The filename base for the saved files')
    parser.add_argument('nacq', type=int, help='The number of fastframe acquisitions to take')
    args = parser.parse_args()

    fold = 'C:/' + args.folder

    take_data(fold, args.filename, args.nacq)
