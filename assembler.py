import sys
import util
import traceback

"""
USAGE: python assembler.py assembly_code.s rom_file.bin
"""

INPUT_FILE_NAME = sys.argv[1]
OUTPUT_FILE_NAME = sys.argv[2]

### OPCODE DEFINITION ###
"""
addressing modes:
accumulator*
immediate*
implied*

relative*
absolute*
zero-page
indirect

absolute indexed
zero-page indexed
indirect-indexed
"""


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
    'inc': 0x1a,
    'rol': 0x2a,
    'dec': 0x3a,
    'lsr': 0x4a,
    'ror': 0x6a,
    'ldy': 0xac
}

opcodes_immediate = {
    'ora': 0x09,
    'and': 0x29,
    'eor': 0x49,
    'bit': 0x89,
    'ldy': 0xa0,
    'ldx': 0xa2,
    'lda': 0xa9,
    'cpy': 0xc0,
    'cmp': 0xc9,
    'cpx': 0xe0,
    'sbc': 0xe9
}

opcodes_relative = { # only used for branch instructions?
    'bbr0': 0x0f,
    'bpl': 0x10,
    'bbr1': 0x1f,
    'bbr2': 0x2f,
    'bmi': 0x30,
    'bbr3': 0x3f,
    'bbr4': 0x4f,
    'bvc': 0x50,
    'bbr5': 0x5f,
    'bbr6': 0x6f,
    'bvs': 0x70,
    'bbr7': 0x7f,
    'bra': 0x80,
    'bbs0': 0x8f,
    'bcc': 0x90,
    'bbs1': 0x9f,
    'bbs2': 0xaf,
    'bcs': 0xb0,
    'bbs3': 0xbf,
    'bbs4': 0xcf,
    'bne': 0xd0,
    'bbs5': 0xdf,
    'bbs6': 0xef,
    'beq': 0xf0,
    'bbs7': 0xff
}

opcodes_absolute = {
    'tsb': 0x0c,
    'ora': 0x0d,
    'als': 0x0e,
    'trb': 0x1c,
    'jsr': 0x20,
    'bit': 0x2c,
    'and': 0x2d,
    'rol': 0x2e,
    'jmp': 0x4c,
    'eor': 0x4d,
    'lsr': 0x4e,
    'adc': 0x6d,
    'ror': 0x6e,
    'sty': 0x8c,
    'sta': 0x8d,
    'stx': 0x8e,
    'stz': 0x9c,
    'lda': 0xad,
    'ldx': 0xae,
    'cpy': 0xcc,
    'cmp': 0xcd,
    'dec': 0xce,
    'cpx': 0xec,
    'sbc': 0xed,
    'inc': 0xee
}

opcodes_stack = {

}
### A S S E M B L Y ###
def assemble(line: str) -> bytearray:         # might need a refactor to assemble line by line to solve the stack vs implied addressing mode problem
    assembled = []

    line = line.split()
    print(line)
    if (len(line) < 1):
        return assembled
    opcode = line[0]
    parameters = []

    for i in range(1, len(line)):
        parameters.append(line[i])

    try:
        if (len(line) == 1):    # lines with only instruction are implied or stack addressing mode
            if (line[0][0] == "."):
                print("directive")
                # handle directives here

            for key in opcodes_implied:
                if (opcode == key):
                    assembled.append(opcodes_implied[opcode])
                    print("implied addressing mode")
                    return assembled

            for key in opcodes_stack:
                if (opcode == key):
                    assembled.append(opcodes_stack[opcode])
                    print("stack addressing mode")
                    return assembled

        elif (parameters[0][0] == "#"):   # lines containing '#' are immediate addressing mode
            assembled.append(opcodes_immediate[opcode])
            assembled.append(int(parameters[0][1:]))     # remove "#" prefixing immediate data
            print("immediate addressing mode")
            return assembled

        else:
            raise Exception("ILLEGAL OR UNSUPPORTED OPCODE")
    except:
        traceback.print_exc()
        util.error(opcode)

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

    print('\033[92m' + "[INFO]\t\tASSEMBLED " + str(current_byte) + " BYTES" '\033[0m')

    output[0x7ffc] = 0x00       # RESET VECTOR; BEGINNING OF ROM
    output[0x7ffd] = 0x80

    with open(OUTPUT_FILE_NAME, "wb") as file_out:   #write actual binary
        file_out.write(output)

    print('\033[92m' + "[SUCCESS]\tWROTE BINARY TO " + OUTPUT_FILE_NAME + "!" + '\033[0m')
