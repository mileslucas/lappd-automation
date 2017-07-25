#!/usr/bin/env python
import vxi11
import argparse
import time
import sys
import matplotlib.pyplot as plt
import numpy as np

def main(nacq):
    plt.style.use('seaborn')
    plt.figure()
    plt.ylabel('Frequency (Hz)')
    hl = plt.plot([], [])
    inst_ip = '192.168.2.152'

    # Set up instrument
    scope = vxi11.Instrument(inst_ip);
    print(scope.ask('*IDN?'))
    scope.write('ACQ:STATE 0')
    scope.write('HOR:FAST:STATE 1')
    scope.write('HOR:FAST:COUN {}'.format(nacq))
    rate = []
    ma = []
    try:
        while True:
            inst_rate = get_rate(scope, nacq)
            rate.append(inst_rate)
            avg_rate = np.asarray(rate)[-10:].mean()
            ma.append(avg_rate)
            print('Rate: {:.2f} Hz  Avg Rate: {:.2f} Hz'.format(inst_rate, avg_rate), end='\r')
    except KeyboardInterrupt:
        plt.plot(rate, c='C0', label='FFA')
        plt.plot(ma, '--', c='C0', label='10 MA')
        plt.legend(loc='best')
        plt.show()
        sys.exit()


def get_rate(scope, nacq):
    # Get acquisitions
    scope.write('ACQ:STATE RUN')
    while(int(scope.ask('ACQ:STATE?'))):
        time.sleep(1)
    total = float(scope.ask('HOR:FAST:TIMES:BETW:CH3? {},1'.format(nacq))[7:-1].replace(' ', ''))
    avg = total / nacq
    # Return the frequency (1 / Period)
    return 1 / avg

if __name__=='__main__':
    # Argument Parsing
    parser = argparse.ArgumentParser(description='Take Tek Oscilliscope data remotely')
    parser.add_argument('nacq', type=float, default=100, help='Number of events to use for average')
    args = parser.parse_args()
    main(args.nacq)
