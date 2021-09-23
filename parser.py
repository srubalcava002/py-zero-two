def strip(line: str) -> list:
    line = line.split('\t')     # split by tabs
    line[-1] = line[-1].split(", ")     # generate a second list of operands if more than one
    return line

def sanitize_endline(string: str) -> str:
    corrected_index = len(string) - 1
    return string[0:corrected_index]