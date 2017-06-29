import serial

def init(ser):
    print('Initializing')
    ser.write(b'jmp 16\n')
    time.sleep(15)

def reset(ser, motor):
    ser.write('ma {} 0\n'.format(motor).encode())

def stop(ser):
    ser.write(b'mr 0 0\n')
    ser.write(b'mr 1 0\n')
