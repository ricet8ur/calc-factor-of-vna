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
    ax.set_xlim(XLIM)
    ax.set_ylim(YLIM)
    st.pyplot(fig)


from streamlit_echarts import st_echarts, JsCode
interval_range = (0,100)
interval_start,interval_end=0,0
def plot_interact_abs_from_f(f,r,i):
    abs_S = list((r[n] ** 2 + i[n] ** 2)**0.5 for n in range(len(r)))
    global interval_range,interval_start,interval_end
    # echarts for datazoom https://discuss.streamlit.io/t/streamlit-echarts/3655
    # datazoom https://echarts.apache.org/examples/en/editor.html?c=line-draggable&lang=ts
    # axis pointer values https://echarts.apache.org/en/option.html#axisPointer
    options = {
        "xAxis": {
            "type": "category",
            "data": f,
        },
        "yAxis": {
            "type": "value",
            "name":"abs(S)",
        },
        "series": [{"data": abs_S, "type": "line", "name":"abs(S)"}],
        "dataZoom": [{"type": "slider", "start": 0, "end": 100}],
        "tooltip": {
            "trigger":"axis",
            "axisPointer": {
                "type": 'cross',
                # "label": {
                    # "show":"true",
                # "formatter": JsCode(
            # "function(info){return info.value;};"
        # ).js_code
                # }
            }
        },
        "toolbox":{
            "feature": {
                "dataView": { "show": "true", "readOnly": "true" },
                "restore": { "show": "true" },
            }
        },
    }
    events = {
        "dataZoom": "function(params) { return [params.start, params.end] }",
    }

    interval_range = st_echarts(
        options=options, events=events, height="500px", key="render_basic_bar_events"
    )
    if interval_range is None:
        interval_range = (0, 100)

    n=len(f)
    interval_start,interval_end=(int(n*interval_range[id]*0.01) for id in (0,1))

def plot_ref_from_f(f, r, i):
    fig = plt.figure(figsize=(10, 10))
    abs_S = list((r[n] ** 2 + i[n] ** 2)**0.5 for n in range(len(r)))
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
    global interval_range,interval_start,   interval_end

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
                    # print('f')
                    try: 
                        data[x]=data[x].decode('utf-8-sig', 'ignore')
                    except:
                        return f, r, i, 'Not an utf-8-sig line №: ' + str(x)

                if select_separator == " ":
                    tru = data[x].split()
                else:
                    data[x] = data[x].replace(select_separator, ' ')
                    tru = data[x].split()

                if len(tru) != 3:
                    return f, r, i, 'Can\'t parse line №: ' + str(x)
                a, b, c = (y for y in tru)
                if not ((is_float(a)) or (is_float(b)) or (is_float(c))):
                    return f, r, i, 'Your data isn\'t numerical type. Error on line: ' + str(x)
                f.append(float(a))  # frequency
                r.append(float(b))  # Re of S11
                i.append(float(c))  # Im of S11
        else:
            return f, r, i, 'Wrong data format'
        return f, r, i, 'data parsed'

    validator_status = '...'
    # calculate
    circle_params = []
    if len(data) > 0:
        f, r, i, validator_status = unpack_data(data)
        plot_interact_abs_from_f(f, r, i)

        f_cut=f[interval_start:interval_end]
        r_cut=r[interval_start:interval_end]
        i_cut=i[interval_start:interval_end]

        if validator_status == 'data parsed':
            Q0, sigmaQ0, QL, sigmaQl, circle_params = calc_function(f_cut, r_cut, i_cut, select_coupling_losses)
            # Q0 = round_up(Q0)
            # sigmaQ0 = round_up(sigmaQ0)
            # QL = round_up(QL)
            # sigmaQl = round_up(sigmaQl)
            if select_coupling_losses:
                st.write("Lossy coupling")
            else:
                st.write("Cable attenuation")

            out_precision='0.7f'
            st.latex(r'Q_0 =' + f'{format(Q0, out_precision)} \pm {format(sigmaQ0, out_precision)},  ' + 
                r'\;\;\varepsilon_{Q_0} =' + f'{format(sigmaQ0 / Q0, out_precision)}')
            st.latex(r'Q_L =' + f'{format(QL, out_precision)} \pm {format(sigmaQl, out_precision)},  ' + 
                r'\;\;\varepsilon_{Q_L} =' + f'{format(sigmaQl / QL, out_precision)}')

    st.write("Status: " + validator_status)

    if len(data) > 0:
        f, r, i, validator_status = unpack_data(data)
        if validator_status == 'data parsed':
            plot_ref_from_f(f_cut, r_cut, i_cut)
            plot_data(r_cut, i_cut, circle_params)