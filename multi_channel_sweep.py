from motors import Motors
from TekFFM import take_data
from slack_bot import send_message
import numpy as np
import tqdm.auto as tqdm
import time
import argparse
import logging
logging.basicConfig(level=logging.INFO)

REACH = 2810 # ticks per mm

XLIM = (0, 490000)
YLIM = (-20000, 20000)

def multi_channel_sweep(num_parallel, num_transverse, xlims, ylims, verbose=True, **kwargs):
    '''
    This will do a multi channel motor sweep

    params
    ------
    stops (int):
        The number of stops to make in the x direction
    channels (int):
        The number of stops to make across the channel limits
    xlims (2-tuple of int):
        The limits of the x stage, inclusive
    ylims (2-tuple of int):
        The limits of the y stage, inclusive
    
    [**kwargs]
    folder, filename, nacg:
        The parameters for TekFFM if provided will save data at each stop

    '''

    takeData = 'folder' in kwargs and 'filename' in kwargs and 'nacq' in kwargs

    xstops = np.linspace(*xlims, num_parallel, dtype=np.int32)
    if num_transverse > 1:
        ystops = np.linspace(*ylims, num_transverse, dtype=np.int32)
    else:
        ystops = [0]
    if verbose:
        send_message('Beginning a multi channel sweep with {} parallel stops and {} transverse stops'.format(num_parallel, num_transverse))
    with Motors() as m:
        logging.info('Moving to initial position')
        m.moveto(0, xstops[0])
        m.moveto(1, ystops[0])
        for i, x in enumerate(tqdm.tqdm(xstops)):
            if num_transverse > 1:
                idx = range(num_transverse)
                yseq = ystops if not i % 2 else reversed(ystops)
                idx = idx if not i % 2 else reversed(idx)
                for j, y in tqdm.tqdm(zip(idx, yseq)):
                    pos_info = 'Stop {}/{}'.format((i * num_transverse + j + 1), num_parallel * num_transverse)
                    if verbose:
                        send_message(pos_info)
                    if j == 0:
                        logging.debug('Moving x stage to {}'.format(x))
                        m.moveto(0, x)
                    else:
                        logging.debug('Moving y stage to {}'.format(y))
                        m.moveto(1, y)
                    m.allstop()
                    if takeData:
                        xpos, ypos = m.get_position()
                        take_data('{}/stop{}_channel{}_pos-{}-{}'.format(kwargs['folder'], i, j, xpos, ypos), kwargs['filename'], kwargs['nacq'], verbose=False)
            else:
                pos_info = 'Stop {}/{}'.format(i + 1, num_parallel)
                if verbose:
                    send_message(pos_info)
                logging.debug('Moving x stage to {}'.format(x))
                m.moveto(0, x)
                m.allstop()
                if takeData:
                    xpos, ypos = m.get_position()
                    take_data('{}/stop{}_pos-{}-{}'.format(kwargs['folder'], i, xpos, ypos), kwargs['filename'], kwargs['nacq'], verbose=False)
        logging.info('Moving home')
        m.park()
        m.allstop()
        finish_message = '\U00002714 Completed multi channel sweep'
        if verbose:
            send_message(finish_message)
        logging.info(finish_message)

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description='Move motors to n discrete points across c channels on an LAPPD channel to take data')
    parser.add_argument(
        'n', type=int, help='The number of samples to be taken on a channel')
    parser.add_argument('c', type=int, help='The number of channels to sample from' )
    parser.add_argument('-d', '--data', nargs=3, 
                        help='Take data using the Tek oscilliscope', metavar=('FOLDER', 'FILENAME', 'NACQS'))
    parser.add_argument('-q', '--quiet', action='store_true', help='Do not send slack messages')
    args = parser.parse_args()
    logging.debug('Parsed arguments: {}'.format(args))
    if args.data is not None:
        multi_channel_sweep(args.n, args.c, XLIM, YLIM, not args.quiet, folder=args.data[0], filename=args.data[1], nacq=int(args.data[2]))
    else:
        multi_channel_sweep(args.n, args.c, XLIM, YLIM, not args.quiet)
