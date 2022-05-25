import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

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
    ax.xlabel("x")
    ax.ylabel("y")
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


def run(calc_function):
    data = []
    uploaded_file = st.file_uploader('Upload a csv')
    if uploaded_file is not None:
        data = uploaded_file.readlines()


    col1, col2 = st.columns(2)

    select_data_format = col1.selectbox('Choose data format from a list',['Frequency, Re(S11), Im(S11)','Frequency, Re(Zin), Im(Zin)'])

    select_separator = col2.selectbox('Choose separator',['","' ,'" "','";"'])
    select_coupling_losses = st.checkbox('I want to apply corrections for coupling losses (lossy coupling)')
    def is_float(element) -> bool:
        try:
            float(element)
            val = float(element)
            if math.isnan(val) or math.isinf(val):
                raise ValueError
            return True
        except ValueError:
            return False
    def unpack_data(data):
        f, r, i = [], [], []
        if select_data_format == 'Frequency, Re(S11), Im(S11)':
            for x in range(len(data)):
                tru = data[x].split(select_separator)
                if len(tru)!=3:
                    return f, r, i, 'Bad line in your file. №:' + str(x)
                a, b, c = (y for y in tru)
                if not ((is_float(a)) or (is_float(b)) or (is_float(c))):
                    return f, r, i, 'Bad data. Your data isnt numerical type. Number of bad line:' + str(x)
                f.append(a)  # frequency
                r.append(b)  # Re of S11
                i.append(c)  # Im of S11
        else:
            return f, r, i, 'Bad data format'
        return f, r, i, 'very nice'


    validator_status = 'nice'
    # calculate
    circle_params=[]
    if len(data) > 0:
        f,r,i,validator_status = unpack_data(data)

        Q0,sigmaQ0,QL,sigmaQl, circle_params =calc_function(f,r,i)
        st.write("Cable attenuation")
        st.write(f"Q0 = {Q0} +- {sigmaQ0}, epsilon Q0 ={sigmaQ0/Q0}")
        st.write(f"QL = {QL} +- {sigmaQl}, epsilon QL ={sigmaQl/QL}")


    st.write("Status: " +validator_status)

    if len(data) > 0:
        f,r,i,validator_status = unpack_data(data)
        plot_data(r,i,circle_params)
    
