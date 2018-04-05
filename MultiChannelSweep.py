from Motors import MotorConnection
import argparse

def MultiChannelSweep(stops, channels, x0, y0, x1, y1):
    '''
    MultiChannelSweep
    ------------------

    '''

    pass

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
    MultiChannelSweep(args.n, args.c, 0, 0, 0, 0)

