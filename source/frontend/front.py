import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sys
  

import os
absolute_path = os.path.abspath(__file__)
# print("Full path: " + absolute_path)
# print("Directory Path: " + os.path.dirname(absolute_path))

# adding /backend to use its functions here
sys.path.append("/".join(os.path.dirname(absolute_path).split('/')[:-1]))
# print("/".join(os.path.dirname(absolute_path).split('/')[:-1]))
from backend.calc import *

def plot_data(r,i, g):
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
    ax.plot(r, i, 'b+')
    #

    #cirlce approximation
    t=np.linspace(0,1,100)
    z = (g[0]*t+g[1])/(g[2]+1)
    ax.plot(z.real,z.imag)
    #

    ax.grid(True)
    ax.axis('square')
    ax.set_yticks(np.arange(-1, 1.2, 0.2))
    ax.set_yticks(np.arange(-1, 1.2, 0.2))
    st.pyplot(fig)


# ../../resource/data/1_M450.MEA
# with open("/".join(os.path.dirname(absolute_path).split('/')[:-2]) + "/resource/data/1_M450.MEA") as f:
#     row = f.readlines()
#     f, r, i = [], [], []
#     for x in row:
#         a, b, c = (float(y) for y in x.split())
#         f.append(a)  # frequency
#         r.append(b)  # Re of something
#         i.append(c)  # Im of something
#     plot_data(r,i)


data = []
uploaded_file = st.file_uploader('Upload a csv')
if uploaded_file is not None:
    data = uploaded_file.readlines()


col1, col2 = st.columns(2)

select_data_format = col1.selectbox('Choose data format from a list',['Frequency, Re(S11), Im(S11)','Frequency, Re(Zin), Im(Zin)'])

select_separator = col2.selectbox('Choose separator',['","' ,'" "','";"'])


def unpack_data(data):
    f, r, i = [], [], []  
    for x in data:
        a, b, c = (float(y) for y in x.split())
        f.append(a)  # frequency
        r.append(b)  # Re of S11
        i.append(c)  # Im of S11
    return f, r, i, 'very nice'

validator_status = 'nice'
# calculate
circle_params=[]
if len(data) > 0:
    f,r,i,validator_status = unpack_data(data)
    
    Q0,sigmaQ0,QL,sigmaQl, circle_params =fl_fitting(f,r,i)
    st.write("Cable attenuation")
    st.write(f"Q0 = {Q0} +- {sigmaQ0}, epsilon Q0 ={sigmaQ0/Q0}")
    st.write(f"QL = {QL} +- {sigmaQl}, epsilon QL ={sigmaQl/QL}")


st.write("Status: " +validator_status)

if len(data) > 0:
    f,r,i,validator_status = unpack_data(data)
    plot_data(r,i,circle_params)
  
