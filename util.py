import sys

def error(opcode: str) -> None:
    sys.exit('\033[91m' + "[ERROR] INSTRUCTION: " + opcode + " NOT RECOGNIZED OR SUPPORTED!" + '\033[0m')

def strip_whitespace(line: str) -> list:
    line = line[:-1]    # remove endline at the end of the string
    line = line.split(" ")     # split by space. split by \t doesn't work for some reason

    for i in range(2):      # strip empty elements in array left by split()
        while not line[i]:
            del line[i]
        if (len(line) == 1):
            break
    
    if (len(line) == 3):    # remove comma (last char of second elemtent) if there's two parameters
        line[1] = line[1][:-1]

    print("returning: " + str(line))
    return line
