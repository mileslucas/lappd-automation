#!/usr/bin/env python
import vxi11
import argparse
import datetime
import sys
import time
import matplotlib.pyplot as plt

def main(nacq):
    plt.style.use('seaborn')
    plt.figure()
    plt.ylabel('Frequency (Hz)')
    hl = plt.plot([], [])
    inst_ip = '192.168.2.152'

    # Set up instrument
    scope = vxi11.Instrument(inst_ip);
    print(scope.ask('*IDN?'))
    scope.write('HOR:FAST:STATE 1')
    scope.write('HOR:FAST:COUN {}'.format(nacq))
    rate = []
    while True:
        rate.append(get_rate(scope))
        avg_rate = np.asarray(rate).mean()
        print('{} Hz'.format(avg_rate), end='\r', flush=True)
        hl.set_ydata(rate)
        plt.axhline(avg_rate, ls='--')
        plt.draw()

def update_line(hl, new_data):

def get_rate(scope):
    # Get acquisitions
    scope.write('ACQ:STATE RUN')
    total = scope.ask('HOR:FAST:TIMES:BETW:CH1 {}-1'.format(nacq))
    avg = total / nacq
    # Return the frequency (1 / Period)
    return 1 / avg

if __name__=='__main__':
    # Argument Parsing
    parser = argparse.ArgumentParser(description='Take Tek Oscilliscope data remotely')
    parser.add_argument('nacq', default=100, help='Number of events to use for average')
    args = parser.parse_args()
    main(args.nacq)
