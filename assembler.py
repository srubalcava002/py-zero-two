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

addressing_modes = { # nested dictionary with addressing mode detected by parser as key and appropriate opcode dictionary as value
    '#': opcodes_immediate,
    '.': directives
}
### A S S E M B L Y ###

def assemble(line: str) -> bytearray:         # might need a refactor to assemble line by line to solve the stack vs implied addressing mode problem
    assembled = bytearray()

    line = parser.strip(line)
    opcode = line[1]
    parameters = line[-1]

        if (opcode[0] == "."):
            if (opcode[1:-1] == "org"):
                current_address = parameters[0]     # might need to convert this to decimal from hex?

        try:
            if not parameters:    # lines with only instruction are implied or stack addressing mode
                for key in opcodes_implied:
                    if (opcode == key):
                        assembled[0] = opcodes_implied[opcode]
                        return assesmbled
                for key in opcodes_implied:
                    if (opcode == key):
                        assembled[0] = opcodes_stack[opcode]
                        return assembled

            elif (parameters.find('#') <= 0):   # lines containing '#' are immediate addressing mode
                assembled[0] = opcodes_immediate[opcode]
                output[1] = int(parameters[0])
                return assembled

            else:
                raise Exception("ILLEGAL OR UNSUPPORTED OPCODE")
        except:
            traceback.print_exc()
            util.error(line_number)

### WRITING PROCESS ###
# might need a secondary write() function to handle .org directives

if __name__ == '__main__':
    output = bytearray([0xea] * 32768)       # prefill ENTIRE rom with nop instruction (could probably reduce memory use by just filling nop until iterator hits 32767? you already have current_byte)

    current_byte = 0

    with open(INPUT_FILE_NAME, "r") as asm:
        current_line = asm.readline()

        while current_line:
            current_line_raw = assemble(current_line)

            for binary in current_line_raw:        # write each byte in the returned list to the rom bytearray
                output[current_byte] = current_line_raw[element]
                current_byte += 1

            current_line = asm.readline()

    print('\033[92m' + "[INFO] ASSEMBLED " + str(current_byte) + " BYTES" '\033[0m')

    output[0x7ffc] = 0x00       # RESET VECTOR; BEGINNING OF ROM
    output[0x7ffd] = 0x80

    with open(OUTPUT_FILE_NAME, "wb") as file_out:   #write actual binary
        file_out.write(output)

    print('\033[92m' + "[SUCCESS] WROTE BINARY TO " + OUTPUT_FILE_NAME + "!" + '\033[0m')
