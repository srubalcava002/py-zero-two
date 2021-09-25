import serial
import sys
import time

INPUT_FILE = sys.argv[1]
SERIAL_PORT = sys.argv[2]

if __name__ == '__main__':
    ser = serial.Serial()   # ADD PARAMETERS TO THIS AND YOU SHOULD BE GOOD TO GO

    with open(INPUT_FILE, "rb") as byte:
        for current_byte in range(32768):
            data = byte.read(1)
            ser.write(data)
            time.sleep(0.25)    # wait long enough to ensure that data was written to the EEPROM
