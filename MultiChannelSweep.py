from Motors import MotorConnection
from TekFFM import take_data
from numpy import linspace, int32
import time
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)

REACH = 2810 # ticks per mm

VEL = 13000 # encoder ticks per second, approx (rounded down)
XLIM = (0, 495000)
YLIM = (-20000, 20000)

def MultiChannelSweep(stops, channels, xlims, ylims, **kwargs):
    '''
    MultiChannelSweep
    ------------------

    '''

    if 'folder' in kwargs and 'filename' in kwargs and 'nacq' in kwargs:
        takeData = True

    xstops = linspace(*xlims, stops, dtype=int32)
    xtime = (xstops[1] - xstops[0]) / VEL
    ystops = linspace(*ylims, channels, dtype=int32)
    ytime = (ystops[1] - ystops[0]) / VEL
    with MotorConnection() as m:
        logging.info('Moving to start position')
        m.moveto(0, xstops[0])
        m.moveto(1, ystops[0])
        time.sleep(15)
        for i, x in enumerate(xstops):
            idx, _ = enumerate(ystops)
            yseq = ystops if not i % 2 else reversed(ystops)
            idx = idx if not i % 2 else reversed(idx)
            for j, y in zip(idx, yseq):
                if j == 0:
                    logging.info('Moving x stage to {}'.format(x))
                    m.moveto(0, x)
                    time.sleep(xtime)
                else:
                    logging.info('Moving y stage to {}'.format(y))
                    m.moveto(1, y)
                    time.sleep(ytime)
                m.allstop()
                if takeData:
                    take_data('C:/' + kwargs['folder'], kwargs['filename'] + '_stop{}_channel{}'.format(i, j), kwargs['nacq'])


if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description='Move motors to n discrete points across c channels on an LAPPD channel to take data')
    parser.add_argument(
        'n', type=int, help='The number of samples to be taken on a channel')
    parser.add_argument('c', type=int, help='The number of channels to sample from' )
    parser.add_argument('-d', '--data', nargs=3, 
                        help='Take data using the Tek oscilliscope', metavar=('FOLDER', 'FILENAME', 'NACQS'))
    args = parser.parse_args()
    logging.debug('Parsed arguments: {}'.format(args))
    if args.data is not None:
        MultiChannelSweep(args.n, args.c, XLIM, YLIM, folder=args.data[0], filename=args.data[1], nacq=int(args.data[2]))
    else:
        MultiChannelSweep(args.n, args.c, XLIM, YLIM)
