import sys
import util
import traceback
import parser

"""
USAGE: python assembler.py assembly_code.s rom_file.bin
"""

INPUT_FILE_NAME = sys.argv[1]
OUTPUT_FILE_NAME = sys.argv[2]

### OPCODE DEFINITION ###
opcodes_implied = {
    'nop': 0xea,
    'clc': 0x18,
    'sec': 0x38,
    'cli': 0x58,
    'sei': 0x78,
    'dey': 0x88,
    'txa': 0x8a,
    'tya': 0x98,
    'txs': 0x9a,
    'tay': 0xa8,
    'tax': 0xaa,
    'clv': 0xb8,
    'tsx': 0xba,
    'iny': 0xc8,
    'dex': 0xca,
    'wai': 0xcb,    # new instruction for wd65c02
    'cld': 0xd8,
    'stp': 0xdb,    # new instruction for wd65c02
    'inx': 0xe8,
    'sed': 0xf8,
}

opcodes_accumulator = {
    'asl': 0x0a,
    'inc': 0x1a
}

opcodes_immediate = {
    'lda': 0xa9,
    'ora': 0x09,
    'and': 0x29,
    'eor': 0x49
}

opcodes_zero_page = {

}

opcodes_internal = {

}

directives = {

}

addressing_modes = { # nested dictionary with addressing mode detected by parser as key and appropriate opcode dictionary as value
    '#': opcodes_immediate,
    '.': directives
}
### A S S E M B L Y ###

def assemble():
    line_number = 0
    current_byte = 0

    with open(INPUT_FILE_NAME, "r") as asm:
        line = asm.readline()
        print("OPENED FILE " + INPUT_FILE_NAME)

        while line:
            line = parser.strip(line)
            opcode = line[0]
            parameters = line[-1]

            try:
                if not parameters:    # lines with only instruction are implied or stack addressing mode
                    output[current_byte] = opcodes_implied[line]
                    current_byte += 1
                elif (parameters.find('#') <= 0):   # lines containing '#' are immediate addressing mode
                    output[current_byte] = opcodes_immediate[opcode]
                    output[current_byte + 1] = int(parameters[1:-1])
                    current_byte += 2               # move two bytes to accomodate immediate data
                else:
                    output[current_byte] = opcodes_internal[opcode]
                    current_byte += 1
            except:
                traceback.print_exc()
                util.error(line_number)

            line_number += 1
            line = asm.readline()
             
    print('\033[92m' + "[INFO] ASSEMBLED " + str(current_byte) + " BYTES" '\033[0m')

### WRITING PROCESS ###

if __name__ == '__main__':
    output = bytearray([0xea] * 32768)       #prefill ENTIRE rom with nop instruction (could probably reduce memory use by just filling nop until iterator hits 32767? you already have current_byte)
    assemble()

    output[0x7ffc] = 0x00       # RESET VECTOR; BEGINNING OF ROM
    output[0x7ffd] = 0x80

    with open(OUTPUT_FILE_NAME, "wb") as file_out:   #write actual binary
        file_out.write(output)

    print('\033[92m' + "[SUCCESS] WROTE BINARY TO " + OUTPUT_FILE_NAME + "!" + '\033[0m')
