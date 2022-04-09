import numpy as np


def open_file(path):
    """depends on the format of file we open"""
    freq, re, im = [], [], []
    with open(path) as f:
        for line in f:
            temp = line[:-1].split('   ')
            for i in range(3):
                temp[i] = temp[i].replace(" ", "")
            freq.append(float(temp[0]))
            re.append(float(temp[1]))
            im.append(float(temp[2]))
    return freq, re, im


def prepare_data(freq, re, im):
    """the function takes raw data and gives vectors of eq (8)"""
    fl = freq[re.index(max(re))]
    # fl is the frequency of loaded resonance
    f0 = fl
    # f0 is the frequency of unloaded resonance
    e1, e2, e3, gamma, p = [], [], [], [], []
    for i in range(0, len(freq)):
        # filling vectors
        t = 2 * (freq[i] - fl) / f0
        g = re[i] + im[i] * 1j
        e1.append(t)
        e2.append(1)
        e3.append(-t * g)
        gamma.append(g)
        p.append(1 / (1 + t ** 2 * (1 + re[i] ** 2 + im[i] ** 2)))
    data = np.array([e1, e2, e3, gamma, p], dtype=complex)
    return data


def solution(data):
    """ takes projections of equation (8) on vectors e1, e2, e3 and solves the equations"""
    c = []  # matrix of the system
    b = []  # matrix extension
    for i in range(3):
        c1 = np.vdot(data[i], data[4] * data[0])
        c2 = np.vdot(data[i], data[4] * data[1])
        c3 = np.vdot(data[i], data[4] * data[2])
        c.append([c1, c2, c3])
        b.append(np.vdot(data[i], data[4] * data[3]))
    a = np.linalg.solve(c, b)
    return a


def q_factor(a):
    """calculation of result"""
    Ql = a[2].imag  # Q-factor of loaded resonator
    d = abs(a[1] - a[0] / a[2])  # diameter of circle
    k = 1 / (2 / d - 1)
    Q = Ql * (1 + k)  # Q-factor = result
    return Q


def calculate(path):
    """applies all functions"""
    freq, re, im = open_file(path)
    data = prepare_data(freq, re, im)
    a = solution(data)
    Q = q_factor(a)
    return Q

