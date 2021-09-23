# py-zero-two

A 6502 assembler targeted at the wd65c02, written in python. Inspired by Ben Eater's DIY 6502 project.

## assembler usage
```
python assembler.py assembly_code.s raw_binary.bin
```

## eeprom-programmer
A tool for programming the EEPROM. Targeted at the Arduino MEGA 2560, but can easily be ported to an Arduino compatible dev board with fewer digital outputs via shift registers.

### eeprom-programmer usage
The EEPROM programmer works via two scripts running simultaneously: serial.py sequentially sends each byte of the assembled, raw binary to the specified serial port and the eeprom-programmer.ino runs on the Arduino and listens for each individual byte to write to the EEPROM.

Usage for serial.py:
```
python serial.py raw_binary.bin [serial port]
```

eeprom-programmer.ino should be running and listening for bytes on the serial port *before* starting serial.py. 
