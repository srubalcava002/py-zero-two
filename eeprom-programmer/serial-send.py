import serial
import sys
import time

# INPUT_FILE = sys.argv[1]
SERIAL_PORT = sys.argv[1]
BAUD_RATE = sys.argv[2]

if __name__ == '__main__':
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

    data = [0x41, 0x2b, 0xea, 0xff, 0x34, 0x23, 0x78, 0x88, 0x60, 0xff, 0x69, 0x54, 0xff]

    ln = 0

    index = 0;
    ser.reset_input_buffer()
    while (index < len(data)):
        status = ser.read()
        ser.reset_input_buffer()

        print(ln)
        print(status)
        print("IN WAITING: " + str(ser.in_waiting))

        ln += 1
        if (status == b'A') or (status == b'C'):
            ser.write(data[index])
            time.sleep(0.1)

            print("SENT: " + str(data[index]))

            while (ser.read() != b'Q'):
                print("WAITING ON CONFIRMATION...")
                time.sleep(0.1)

            index += 1

        else:
            time.sleep(0.1)

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    """
    with open(INPUT_FILE, "rb") as byte:
        for current_byte in range(32768):
            data = byte.read(1)
            while (ser.read() != "A"):
                time.sleep(0.25)
            ser.write(data)
            time.sleep(0.25)    # wait long enough to ensure that data was written to the EEPROM
    """