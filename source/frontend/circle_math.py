import numpy as np
from typing import Tuple


# nearest to (1,0) point is omitted
def point_of_intersection(x1: float, y1: float, r1: float, x2: float,
                          y2: float, r2: float) -> Tuple[float, float]:
    p1 = x1 + y1 * 1j
    p2 = x2 + y2 * 1j

    d = abs(p2 - p1)
    q = (r1**2 - r2**2 + d**2) / (2 * d)

    h = (r1**2 - q**2)**0.5

    p = p1 + q * (p2 - p1) / d

    intersect = [(p.real + h * (p2.imag - p1.imag) / d,
                  p.imag - h * (p2.real - p1.real) / d),
                 (p.real - h * (p2.imag - p1.imag) / d,
                  p.imag + h * (p2.real - p1.real) / d)]

    intersect = [x + 1j * y for x, y in intersect]
    intersect_shift = [p - (1 + 0j) for p in intersect]
    intersect_shift = abs(np.array(intersect_shift))
    p = intersect[0]
    if intersect_shift[0] < intersect_shift[1]:
        p = intersect[1]
    return p.real, p.imag


def point_of_intersection_with_unit(x: float, y: float,
                                    r: float) -> Tuple[float, float]:
    return point_of_intersection(x, y, r, 0, 0, 1)