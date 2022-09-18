import math
from typing import List, Tuple, Union

def is_float(element) -> bool:
    try:
        float(element)
        val = float(element)
        if math.isnan(val) or math.isinf(val):
            raise ValueError
        return True
    except ValueError:
        return False


# (to utf-8)
# status returned
def read_data(data: list) -> str:
    for x in range(len(data)):
        if type(data[x]) == bytes:
            try:
                data[x] = data[x].decode('utf-8-sig', 'ignore')
            except:
                return 'Not an utf-8-sig line №: ' + str(x)
    return 'data read, but not parsed'


# check if line has comments
# first is a comment line according to .snp documentation,
# others detects comments in various languages
def check_line_comments(line: str) -> Union[str, None]:
    if len(line) < 2 or line[0] == '!' or line[0] == '#' or line[
            0] == '%' or line[0] == '/':
        return None
    else:
        # generally we expect these chars as separators
        line = line.replace(';', ' ').replace(',', ' ').replace('|', ' ')
        if '!' in line:
            line = line[:line.find('!')]
        return line

# unpack a few first lines of the file to get number of ports
def count_columns(data: List[str]) -> Tuple[int, str]:
    return_status = 'data parsed'
    column_count = 0
    for x in range(len(data)):
        line = check_line_comments(data[x])
        if line is None:
            continue
        line = line.split()
        # always at least 3 values for single data point
        if len(line) < 3:
            return_status = 'Can\'t parse line № ' + \
                str(x) + ',\n not enough arguments (less than 3)'
            break
        column_count = len(line)
        break
    return (column_count, return_status)


def prepare_snp(data: List[str], number: int) -> Tuple[List[str], str]:
    prepared_data = []
    return_status = 'data read, but not parsed'
    for x in range(len(data)):
        line = check_line_comments(data[x])
        if line is None:
            continue
        splitted_line = line.split()
        if number * 2 + 1 == len(splitted_line):
            prepared_data.append(line)
        elif number * 2 == len(splitted_line):
            prepared_data[-1] += line
        else:
            return_status = "Parsing error for .snp format on line №" + str(x)
    return prepared_data, return_status
