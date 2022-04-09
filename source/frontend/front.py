import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sys
  

import os
absolute_path = os.path.abspath(__file__)
# print("Full path: " + absolute_path)
# print("Directory Path: " + os.path.dirname(absolute_path))

# adding /backend to use functions from it here
sys.path.insert(0, "/".join(os.path.dirname(absolute_path).split('/')[:-1]))
from backend.calc import *

# ../../resource/data/1_M450.MEA
with open("/".join(os.path.dirname(absolute_path).split('/')[:-2]) + "/resource/data/1_M450.MEA") as f:
    row = f.readlines()
    f, r, i = [], [], []
    for x in row:
        a, b, c = (float(y) for y in x.split())
        f.append(a)  # frequency
        r.append(b)  # Re of something
        i.append(c)  # Im of something

    # unit circle
    unit_circle_x = []
    unit_circle_y = []
    for x in np.arange(-1, 1, 0.01):
        unit_circle_x.append(x)
        unit_circle_y.append((1-x**2)**0.5)

    unit_circle_x.append(1)
    unit_circle_y.append(0)

    for x in np.arange(-1, 1, 0.01)[::-1]:
        unit_circle_x.append(x)
        unit_circle_y.append(-(1-x**2)**0.5)

    fig, ax = plt.subplots()
    ax.plot(unit_circle_x, unit_circle_y)
    #

    # data
    ax.plot(r, i)
    #

    ax.grid(True)
    ax.axis('square')
    ax.set_yticks(np.arange(-1, 1.2, 0.2))
    ax.set_yticks(np.arange(-1, 1.2, 0.2))
    st.pyplot(fig)
