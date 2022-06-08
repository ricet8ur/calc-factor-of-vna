import math
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

XLIM = [-1.1, 1.1]
YLIM = [-1.1, 1.1]


def round_up(x, n=7):
    if x == 0:
        return 0
    deg = math.floor(math.log(abs(x), 10))
    return (10 ** deg) * round(x / (10 ** deg), n - 1)


def circle(ax, x, y, radius, color='#1946BA'):
    from matplotlib.patches import Ellipse
    drawn_circle = Ellipse((x, y), radius * 2, radius * 2, clip_on=False,
                           zorder=2, linewidth=2, edgecolor=color, facecolor=(0, 0, 0, .0125))
    ax.add_artist(drawn_circle)


def plot_data(r, i, g):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot()
    ax.set_xlim(XLIM)
    ax.set_ylim(YLIM)
    major_ticks = np.arange(-1.0, 1.1, 0.25)
    minor_ticks = np.arange(-1.1, 1.1, 0.05)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    ax.grid(which='major', color='grey', linewidth=1.5)
    ax.grid(which='minor', color='grey', linewidth=0.5, linestyle=':')
    plt.xlabel(r'$Re(\Gamma)$', color='gray', fontsize=16, fontname="Cambria")
    plt.ylabel('$Im(\Gamma)$', color='gray', fontsize=16, fontname="Cambria")
    plt.title('Smith chart', fontsize=24, fontname="Cambria")
    # circle approximation
    radius = abs(g[1] - g[0] / g[2]) / 2
    x = ((g[1] + g[0] / g[2]) / 2).real
    y = ((g[1] + g[0] / g[2]) / 2).imag
    circle(ax, x, y, radius, color='#FF8400')
    #
    # unit circle
    circle(ax, 0, 0, 1)
    #
    # data
    ax.plot(r, i, '+', ms=10, mew=2, color='#1946BA')
    #

    st.pyplot(fig)


def plot_ref_from_f(r, i, f):
    fig = plt.figure(figsize=(10, 10))
    abs_S = list(math.sqrt(r[n] ** 2 + i[n] ** 2) for n in range(len(r)))
    xlim = [min(f) - abs(max(f) - min(f)) * 0.1, max(f) + abs(max(f) - min(f)) * 0.1]
    ylim = [min(abs_S) - abs(max(abs_S) - min(abs_S)) * 0.5, max(abs_S) + abs(max(abs_S) - min(abs_S)) * 0.5]
    ax = fig.add_subplot()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(which='major', color='k', linewidth=1)
    ax.grid(which='minor', color='grey', linestyle=':', linewidth=0.5)
    plt.xlabel(r'$f,\; 1/c$', color='gray', fontsize=16, fontname="Cambria")
    plt.ylabel('$|\Gamma|$', color='gray', fontsize=16, fontname="Cambria")
    plt.title('Modulus of reflection coefficient from frequency', fontsize=24, fontname="Cambria")
    ax.plot(f, abs_S, '+', ms=10, mew=2, color='#1946BA')
    st.pyplot(fig)


def run(calc_function):
    data = []
    uploaded_file = st.file_uploader('Upload a csv')
    if uploaded_file is not None:
        data = uploaded_file.readlines()

    col1, col2 = st.columns(2)

    select_data_format = col1.selectbox('Choose data format from a list',
                                        ['Frequency, Re(S11), Im(S11)', 'Frequency, Re(Zin), Im(Zin)'])

    select_separator = col2.selectbox('Choose separator', ['" "', '","', '";"'])
    select_coupling_losses = st.checkbox('Apply corrections for coupling losses (lossy coupling)')

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
        nonlocal select_separator
        nonlocal select_data_format
        f, r, i = [], [], []
        if select_data_format == 'Frequency, Re(S11), Im(S11)':
            for x in range(len(data)):
                # print(select_separator)
                select_separator = select_separator.replace('\"', '')
                if type(data[x])==bytes:
                    data[x]=data[x].decode()
                if select_separator == " ":
                    tru = data[x].split()
                else:
                    data[x] = data[x].replace(select_separator, ' ')
                    tru = data[x].split()

                if len(tru) != 3:
                    return f, r, i, 'Bad line in your file. №:' + str(x)
                a, b, c = (y for y in tru)
                if not ((is_float(a)) or (is_float(b)) or (is_float(c))):
                    return f, r, i, 'Bad data. Your data isn\'t numerical type. Number of bad line:' + str(x)
                f.append(float(a))  # frequency
                r.append(float(b))  # Re of S11
                i.append(float(c))  # Im of S11
        else:
            return f, r, i, 'Bad data format'
        return f, r, i, 'very nice'

    validator_status = 'nice'
    # calculate
    circle_params = []
    if len(data) > 0:
        f, r, i, validator_status = unpack_data(data)

        if validator_status == 'very nice':
            Q0, sigmaQ0, QL, sigmaQl, circle_params = calc_function(f, r, i)
            Q0 = round_up(Q0)
            sigmaQ0 = round_up(sigmaQ0)
            QL = round_up(QL)
            sigmaQl = round_up(sigmaQl)
            st.write("Cable attenuation")
            st.latex(r'Q_0 =' + f'{Q0} \pm {sigmaQ0},  ' + r'\;\;\varepsilon_{Q_0} =' + f'{round_up(sigmaQ0 / Q0)}')
            st.latex(r'Q_L =' + f'{QL} \pm {sigmaQl},  ' + r'\;\;\varepsilon_{Q_L} =' + f'{round_up(sigmaQl / QL)}')

    st.write("Status: " + validator_status)

    if len(data) > 0:
        f, r, i, validator_status = unpack_data(data)
        if validator_status == 'very nice':
            plot_data(r, i, circle_params)
            plot_ref_from_f(r, i, f)
