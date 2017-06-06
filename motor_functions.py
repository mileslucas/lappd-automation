import serial

def init(ser):
    print('Initializing')
    ser.write(b'jmp 16\n')
    time.sleep(15)

def reset(ser):
    ser.write(b'ma 0 0\n')
    ser.write(b'ma 1 0\n')

def stop(ser):
    ser.write(b'mr 0 0\n')
    ser.write(b'mr 0 0\n')
