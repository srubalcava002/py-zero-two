import serial
import sys
import time

INPUT_FILE = sys.argv[1]
SERIAL_PORT = sys.argv[1]
BAUD_RATE = sys.argv[2]

if __name__ == '__main__':
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

    ser.reset_input_buffer()        # clear input buffer of any garbage that may be in it

    with open(INPUT_FILE, "rb") as byte:
        for current_byte in range(32768):
            status = ser.read()
            ser.reset_input_buffer()        # dont let the buffer fill up

            if (status == b'A') or (status == b'B'):    # write byte when ready signal is recieved
                ser.write(byte.read(1))     # read input file one byte at a time
                time.sleep(0.1)

                while (ser.read() != b'Q'):             # wait for confirmation signal before processing next byte
                    time.sleep(0.1)
            else:
                time.sleep(0.1)

    ser.reset_input_buffer()
    ser.reset_output_buffer()
