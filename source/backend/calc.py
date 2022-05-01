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
    """ takes projections of equation (8) on vectors e1, e2, e3 and solves the equations.
     It is also gives matrix of equation"""
    c = []  # matrix of the system
    b = []  # matrix extension
    for i in range(3):
        c1 = np.vdot(data[i], data[4] * data[0])
        c2 = np.vdot(data[i], data[4] * data[1])
        c3 = np.vdot(data[i], data[4] * data[2])
        c.append([c1, c2, c3])
        b.append(np.vdot(data[i], data[4] * data[3]))
    a = np.linalg.solve(c, b)
    c = np.array(c)
    d = np.linalg.inv(c)  # inverse of matrix c
    return a, c, d


def q_factor(a):
    """calculation of result"""
    Ql = a[2].imag  # Q-factor of loaded resonator
    diam = abs(a[1] - a[0] / a[2])  # diameter of circle
    k = 1 / (2 / diam - 1)
    Q = Ql * (1 + k)  # Q-factor = result
    return Ql, diam, k, Q


def recalculation_of_data(data, a, c, d, error=False):
    """preparation data for the next iteration of solving system"""
    # data = np.array([e1, e2, e3, gamma, p], dtype=complex), t = e1, 1 = e2
    eps = np.array(a[0]*data[0] + a[1]*data[1] - a[2]*data[0]*data[3] - data[3], dtype=complex)
    # eps is eq(7) line's errors
    S2 = np.dot(abs(data[4]), abs(eps)*abs(eps))  # the weighted squared sum of errors
    sigma2A = []  # the square of standart deviation coefficients a
    temp = c[0][0]*d[0][0] + c[1][1]*d[1][1] + c[2][2]*d[2][2]
    for i in range(3):
        sigma2A.append(d[i][i] * S2 / temp)
    for i in range(len(data[4])):  # recalculation of weight coefficients P
        data[4][i] = 1/(data[0][i]**2 * sigma2A[0] + sigma2A[1] + data[0][i]**2 * sigma2A[2] * (abs(data[3][i])**2))
    if error:
        return abs(np.array(sigma2A))
    else:
        return data


def random_deviation(a, sigma2A, diam, k, Ql):
    """defines standart deviations of values"""
    sigmaQl = sigma2A[2]**0.5
    sigmaDiam = (sigma2A[0]/(abs(a[2])**2) + sigma2A[1] + abs(a[0]/a[2]/a[2])**2 * sigma2A[2])**0.5
    sigmaK = 2*sigmaDiam/((2-diam)**2)
    sigmaQ0 = ((1 + k)**2 * sigma2A[2] + Ql**2 * sigmaK**2)**0.5
    return sigmaQ0


def apply(filename):
    freq, re, im = open_file(filename)
    data = prepare_data(freq, re, im)
    a, c, d = solution(data)
    for i in range(2, 10):
        data = recalculation_of_data(data, a, c, d)
        a, c, d = solution(data)
        Ql, diam, k, Q = q_factor(a)
        sigma2A = recalculation_of_data(data, a, c, d, error=True)
        sigmaQ0 = random_deviation(a, sigma2A, diam, k, Ql)
        print(f"Q = {Q} +- {sigmaQ0}, if i == {i}".format(Q, sigmaQ0, i))

