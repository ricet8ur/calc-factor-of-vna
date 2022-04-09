import numpy as np


def prepare_data(freq, re, im):
    """the function takes raw data and gives vectors of eq (8)"""
    fl = freq[re.index(max(re))]
    # fl is the frequency of loaded resonance
    f0 = fl
    # f0 is the frequency of unloaded resonance
    e1, e2, e3, gamma, p = [], [], [], [], []
    for i in range(0, len(freq)):
        # filling vectors
        t = 2*(freq[i] - fl)/f0
        g = re[i] + im[i] * j
        e1.append(t)
        e2.append(1)
        e3.append(-t*g)
        gamma.append(g)
        p.append(1/(1 + t**2*(1 + re[i]**2 + im[i]**2)))
    data = np.array([e1, e2, e3, gamma, p], dtype=complex)
    return data

def scalar_product ():
    pass

