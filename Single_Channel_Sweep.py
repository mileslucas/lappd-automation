import serial
import time

# Argument Parsing
# Argument Parsing
parser = argparse.ArgumentParser(description='Move motors to n discrete points on an LAPPD channel to take data')
parser.add_argument('n', type=int, help='The number of samples to be taken on this channel')
args = parser.parse_args()

# Initialize the motors
ser = serial.Serial('/dev/ttyUSB0', baudrate=19200)
ser.write('jmp 16')
time.sleep(15)

# Zero the motors
# TODO

# Move the motors

plate_width = 500000 # Motor encoder ticks #TODO
step = plate_width / args.n

for i in range(args.n + 1):
    ser.write('mr 0 {}'.format(step).encode())

    #Take Data #TODO
    time.sleep(5)

print('Finished')
ser.close()    
