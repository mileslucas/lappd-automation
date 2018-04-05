from Motors import MotorConnection
from numpy import linspace
import time
import argparse

def MultiChannelSweep(stops, channels, x0, y0, x1, y1):
    '''
    MultiChannelSweep
    ------------------

    '''
    xstops = linspace(x0, x1, stops)
    ystops = linspace(y0, y1, channels)
    with MotorConnection() as m:
        for x in xstops:
            m.moveto(0, x)
            time.sleep(1)
            for y in ystops:
                m.moveto(1, y)
                time.sleep(1)
    

if __name__=='__main__':
    # Argument Parsing
    parser = argparse.ArgumentParser(
        description='Move motors to n discrete points across c channels on an LAPPD channel to take data')
    parser.add_argument(
        'n', type=int, help='The number of samples to be taken on a channel')
    parser.add_argument('c',help='The number of channels to sample from' )
    parser.add_argument('-d', '--data', default=False, action='store_true',
                        help='Take data using the Tek oscilliscope')
    args = parser.parse_args()
    MultiChannelSweep(args.n, args.c, -100000, -100000, 10000, 10000)

