#!python
import argparse
import datetime
import sys
import time

import vxi11
import tqdm


inst_ip = '10.11.151.17'

def take_data(fold, filename, nacq, start=0, verbose=True):
    '''
    This function takes data using the tektronix oscilloscope set up in Matt's workspace

    params
    ------
    fold (string):
        This is the folder on the oscope below 'C:/' to store the data in. Note that folders cannot be 
        created recursively, so every folder except the last one listed must already exist on the machine
    filename (string):
        This will be the filename to prepend each sample with.
    nacq (int):
        This is the number of fast frame acquisitions to make
    start (int):
        The acquisition number to start at
    verbose (bool):
        Show outputs from acquisition
    '''
    


    folder = 'C:/' + fold

    # Set up instrument
    scope = vxi11.Instrument(inst_ip)
    print(scope.ask('*IDN?'))

    # Create Folder for data
    scope.write('FILES:MKD \'{}\''.format(folder))

    # Set up fastframe and scope settings
    # scope.write('HOR:MAIN:SCA 10e-9') # 10 ns
    scope.write('HOR:FAST:STATE 1')
    scope.write('HOR:FAST:COUN 1000')

    # Get acquisitions
    pbar = tqdm.trange(start, nacq, initial=start, total=nacq)
    for i in pbar:
        pbar.set_description('Starting acquisition')
        scope.write('ACQ:STATE RUN')
        while(int(scope.ask('ACQ:STATE?'))):
            time.sleep(1)
        pbar.set_description('Data acquired, now writing')
        scope.write('SAVE:WAVE ALL, \'{}/{}_{}_\''.format(folder, filename, i))
        time.sleep(20)

    print('\nFinished\nFiles stored in \'{}/\' on scope'.format(folder))

if __name__=='__main__':
    # Argument Parsing
    parser = argparse.ArgumentParser(description='Take Tek Oscilliscope data remotely')
    parser.add_argument('folder', default=datetime.date, help='The folder name below "C:/" for the saved oscilliscope data')
    parser.add_argument('filename', help='The filename base for the saved files')
    parser.add_argument('nacq', type=int, help='The number of fastframe acquisitions to take')
    parser.add_argument('-s', '--start', type=int, default=0, help='The iteration to start on. Helpful if resuming a previous run.')
    args = parser.parse_args()

    take_data(args.folder, args.filename, args.nacq, args.start)
