import sys
import util
import traceback

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

opcodes_stack = {

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

### A S S E M B L Y ###
def assemble(line: str) -> bytearray:         # might need a refactor to assemble line by line to solve the stack vs implied addressing mode problem
    assembled = []

    line = util.strip_whitespace(line)
    opcode = line[0]
    parameters = []

    print("trying: " + str(line))
    for i in range(1, len(line)):
        parameters.append(line[i])
        print("appended to parameters[]: " + parameters[-1])

    try:
        if (len(line) == 1):    # lines with only instruction are implied or stack addressing mode
            for key in opcodes_implied:
                if (opcode == key):
                    assembled.append(opcodes_implied[opcode])
                    print("assembled: " + str(assembled))
                    return assembled

            for key in opcodes_stack:
                if (opcode == key):
                    assembled.append(opcodes_stack[opcode])
                    print("assembled: " + str(assembled))
                    return assembled

        elif (parameters[0][0] == "#"):   # lines containing '#' are immediate addressing mode
            assembled.append(opcodes_immediate[opcode])
            assembled.append(int(parameters[0][1:]))     # remove "#" prefixing immediate data
            print("assembled: " + str(assembled))
            return assembled

        else:
            raise Exception("ILLEGAL OR UNSUPPORTED OPCODE")
    except:
        traceback.print_exc()
        util.error(opcode[0])

### WRITING PROCESS ###
# might need a secondary write() function to handle .org directives

if __name__ == '__main__':
    output = bytearray([0xea] * 32768)

    current_byte = 0

    with open(INPUT_FILE_NAME, "r") as asm:
        current_line = asm.readline()

        while current_line:
            current_line_raw = assemble(current_line)

            for binary in current_line_raw:        # write each byte in the returned list to the rom bytearray
                output[current_byte] = binary
                current_byte += 1

            current_line = asm.readline()

    print('\033[92m' + "[INFO] ASSEMBLED " + str(current_byte) + " BYTES" '\033[0m')

    output[0x7ffc] = 0x00       # RESET VECTOR; BEGINNING OF ROM
    output[0x7ffd] = 0x80

    with open(OUTPUT_FILE_NAME, "wb") as file_out:   #write actual binary
        file_out.write(output)

    print('\033[92m' + "[SUCCESS] WROTE BINARY TO " + OUTPUT_FILE_NAME + "!" + '\033[0m')
