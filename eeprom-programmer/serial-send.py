import serial
import sys
import time


"""
USAGE: python serial-send.py raw_binary.bin <serial_port>
"""

INPUT_FILE = sys.argv[1]
SERIAL_PORT = sys.argv[2]
BAUD_RATE = 57600

if __name__ == '__main__':
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

    ser.reset_input_buffer()        # clear input buffer of any garbage that may be in it

    with open(INPUT_FILE, "rb") as byte:
        for current_byte in range(32768):
            print("Writing.", end='\r')
            status = ser.read()
            ser.reset_input_buffer()        # dont let the buffer fill up

            print("Writing.", end='\r')
            if (status == b'A') or (status == b'B'):    # write byte when ready signal is recieved
                ser.write(byte.read(1))     # read input file one byte at a time
                time.sleep(0.001)

                while (ser.read() != b'Q'):             # wait for confirmation signal before processing next byte
                    time.sleep(0.001)
            else:
                time.sleep(0.001)
            print("Writing...", end='\r')

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    print('\033[92m' + "[SUCCESS]\tFINISHED WRITING TO EEPROM!" + '\033[0m')
