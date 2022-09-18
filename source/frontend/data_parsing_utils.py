import math
from typing import List, Tuple, Union
import numpy as np

from .circle_math import point_of_intersection

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


# check comments and translate data matrixes into lines
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


# for Touchstone .snp format
def parse_snp_header(
        data: List[str],
        is_data_format_snp: bool) -> Tuple[int, int, float, float]:
    if is_data_format_snp:
        for x in range(len(data)):
            if data[x].lstrip()[0] == '#':
                line = data[x].split()
                if len(line) == 6:
                    repr_map = {"ri": 0, "ma": 1, "db": 2}
                    para_map = {"s": 0, "z": 1}
                    hz_map = {
                        "ghz": 10**9,
                        "mhz": 10**6,
                        "khz": 10**3,
                        "hz": 1
                    }
                    hz, measurement_parameter, data_representation, _r, ref_resistance = (
                        x.lower() for x in line[1:])
                    try:
                        return hz_map[hz], para_map[
                            measurement_parameter], repr_map[
                                data_representation], int(
                                    float(ref_resistance))
                    except:
                        break
                break
    return 1, 0, 0, 50


def unpack_data(data: List[str], first_column:int, column_count:int, ref_resistance:float,
                measurement_parameter:int, data_representation:int):
    f, r, i = [], [], []
    return_status = 'data parsed'
    for x in range(len(data)):
        line = check_line_comments(data[x])
        if line is None:
            continue
        line = line.split()
        if column_count != len(line):
            return_status = "Wrong number of parameters on line № " + str(x)
            break

        # 1: process according to data_placement
        a, b, c = None, None, None
        try:
            a = line[0]
            b = line[first_column]
            c = line[first_column + 1]
        except:
            return_status = 'Can\'t parse line №: ' + \
                str(x) + ',\n not enough arguments'
            break
        if not ((is_float(a)) or (is_float(b)) or (is_float(c))):
            return_status = 'Wrong data type, expected number. Error on line: ' + \
                str(x)
            break

        # mark as processed?
        # for y in (a,b,c):
        #     ace_preview_markers.append(
        #         {"startRow": x,"startCol": 0,
        #         "endRow": x,"endCol": data[x].find(y)+len(y),
        #         "className": "ace_stack","type": "text"})

        a, b, c = (float(x) for x in (a, b, c))
        f.append(a)  # frequency

        # 2: process according to data_representation
        if data_representation == 'Frequency, real, imaginary':
            # std format
            r.append(b)  # Re
            i.append(c)  # Im
        elif data_representation == 'Frequency, magnitude, angle':
            r.append(b * np.cos(np.deg2rad(c)))
            i.append(b * np.sin(np.deg2rad(c)))
        elif data_representation == 'Frequency, db, angle':
            b = 10**(b / 20)
            r.append(b * np.cos(np.deg2rad(c)))
            i.append(b * np.sin(np.deg2rad(c)))
        else:
            return_status = 'Wrong data format'
            break

        # 3: process according to measurement_parameter
        if measurement_parameter == 'Z':
            # normalization
            r[-1] = r[-1] / ref_resistance
            i[-1] = i[-1] / ref_resistance
            # translate to S
            try:
                r[-1], i[-1] = point_of_intersection(r[-1] / (1 + r[-1]), 0,
                                                     1 / (1 + r[-1]), 1,
                                                     1 / i[-1], 1 / i[-1])
            except:
                r.pop()
                i.pop()
                f.pop()
                
    if return_status == 'data parsed':
        if len(f) < 3 or len(f) != len(r) or len(f) != len(i):
            return_status = 'Choosen data range is too small, add more points'
        elif max(abs(np.array(r) + 1j * np.array(i))) > 2:
            return_status = 'Your data points have an abnormality:\
                        they are too far outside the unit cirlce.\
                        Make sure the format is correct'

    return f, r, i, return_status