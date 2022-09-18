# from cmath import atan
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


def prepare_data(freq, re, im, fl=None):
    """the function takes raw data and gives vectors of eq (8)"""
    # finding fl from the point with smallest magnitude if argument not provided
    if fl is None:
        s = abs(np.array(re) + np.array(im) * 1j)
        # frequency of loaded resonance
        fl = freq[list(abs(s)).index(min(abs(s)))]

    # frequency of unloaded resonance.
    f0 = fl
    # f0 = fl does not decrease the accuracy if Q >> 100
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
    data = np.array([e1, e2, e3, gamma, p], dtype=np.cdouble)
    return data, fl


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
    # c = np.array(c)
    a = np.linalg.solve(c, b)
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
    eps = np.array(a[0] * data[0] + a[1] * data[1] - a[2] * data[0] * data[3] - data[3], dtype=complex)
    # eps is eq(7) line's errors
    S2 = np.dot(abs(data[4]), abs(eps) * abs(eps))  # the weighted squared sum of errors
    sigma2A = []  # the square of standart deviation coefficients a
    temp = c[0][0] * d[0][0] + c[1][1] * d[1][1] + c[2][2] * d[2][2]
    for i in range(3):
        sigma2A.append(d[i][i] * S2 / temp)
    for i in range(len(data[4])):  # recalculation of weight coefficients P
        data[4][i] = 1 / (
                    data[0][i] ** 2 * sigma2A[0] + sigma2A[1] + data[0][i] ** 2 * sigma2A[2] * (abs(data[3][i]) ** 2))
    if error:
        return abs(np.array(sigma2A))
    else:
        return data


def recalculating(data, a, c, d, n, printing=False):
    for i in range(2, n):
        data = recalculation_of_data(data, a, c, d)
        a, c, d = solution(data)
        Ql, diam, k, Q = q_factor(a)
        sigma2A = recalculation_of_data(data, a, c, d, error=True)
        sigmaQ0, sigmaQl = random_deviation(a, sigma2A, diam, k, Ql)
        if printing:
            print(f"Q = {Q} +- {sigmaQ0}, if i == {i}")
    return a, c, d, Ql, diam, k, Q, sigma2A, sigmaQ0, sigmaQl, data


def random_deviation(a, sigma2A, diam, k, Ql):
    """defines standart deviations of values"""
    sigmaQl = sigma2A[2] ** 0.5
    sigmaDiam = (sigma2A[0] / (abs(a[2]) ** 2) + sigma2A[1] + abs(a[0] / a[2] / a[2]) ** 2 * sigma2A[2]) ** 0.5
    sigmaK = 2 * sigmaDiam / ((2 - diam) ** 2)
    sigmaQ0 = ((1 + k) ** 2 * sigma2A[2] + Ql ** 2 * sigmaK ** 2) ** 0.5
    return sigmaQ0, sigmaQl


def apply(filename):
    freq, re, im = open_file(filename)
    data = prepare_data(freq, re, im)
    a, c, d = solution(data)
    a, c, d, Ql, diam, k, Q, sigma2A, sigmaQ0, sigmaQl, data = recalculating(data, a, c, d, 10, printing=True)


def fl_fitting(freq, re, im, correction):
    """providing an option to find actual fl"""

    data, fl = prepare_data(freq, re, im)
    a, c, d = solution(data)
    Ql, Q, sigmaQ0, sigmaQl = None, None, None, None
    # Repeated curve fitting
    # 1.189 of Qfactor Matlab
    # fl2 = 0
    # g_d=0
    # g_c=0
    for x in range(0, 3):
        g_c = (np.conj(a[2]) * a[1] - a[0]) / (np.conj(a[2]) - a[2])
        g_d = a[0] / a[2]
        g_2 = 2 * g_c - g_d
        dt = (a[1] - g_2) / (g_2 * a[2] - a[0])
        fl2 = fl * (1 + np.real(dt) / 2)
        data, fl = prepare_data(freq, re, im, fl2)
        a, c, d = solution(data)
    a, c, d, Ql, diam, k, Q, sigma2A, sigmaQ0, sigmaQl, data = recalculating(data, a, c, d, 20)

    # taking into account coupling losses on page 69 of Qfactor Matlab
    # to get results similar to example program
    ks = 0
    if correction:
        phi1 = np.arctan(np.double(g_d.imag / g_d.real))  # 1.239
        phi2 = np.arctan(
            np.double((g_c.imag - g_d.imag) / (g_c.real - g_d.real)))
        phi = -phi1 + phi2
        d_s = (1 - np.abs(g_d)**2) / (1 - np.abs(g_d) * np.cos(phi))
        diam = abs(a[1] - a[0] / a[2])

        qk = 1 / (d_s / diam - 1)
        k = qk

        ks = (2 / d_s - 1) / (2 / diam - 2 / d_s)

        sigma2A = recalculation_of_data(data, a, c, d, error=True)
        sigmaQ0, sigmaQl = random_deviation(a, sigma2A, diam, k, Ql)
        Q = Ql * (1 + k)  # Q-factor = result


    t = 2*(np.array(freq)-fl)/fl
    fitted_mag_s = abs((a[0]*t+a[1])/(a[2]*t+1))

    return Q, sigmaQ0, Ql, sigmaQl, k, ks, a, fl, fitted_mag_s
