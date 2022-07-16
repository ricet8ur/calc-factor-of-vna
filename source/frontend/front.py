from streamlit_ace import st_ace
from streamlit_echarts import st_echarts
import math
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

XLIM = [-1.1, 1.1] # why global...
YLIM = [-1.1, 1.1]

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
    # ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    # ax.set_yticks(major_ticks)
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
    # sometimes throws exception
    try:
        st.pyplot(fig)
    except:
        st.write("Plot size is too big. There are some problems with fitting. Check your input")


interval_range = (0, 100) # in percents
interval_start, interval_end = 0, 0


def plot_interact_abs_from_f(f, r, i):
    abs_S = list((r[n] ** 2 + i[n] ** 2)**0.5 for n in range(len(r)))
    global interval_range, interval_start, interval_end
    # echarts for datazoom https://discuss.streamlit.io/t/streamlit-echarts/3655
    # datazoom https://echarts.apache.org/examples/en/editor.html?c=line-draggable&lang=ts
    # axis pointer values https://echarts.apache.org/en/option.html#axisPointer
    options = {
        "xAxis": {
            "type": "category",
            "data": f,
            "name": "Hz",
            "nameTextStyle": {"fontSize": 16},
            "axisLabel": {"fontSize": 16}
        },
        "yAxis": {
            "type": "value",
            "name": "abs(S)",
            "nameTextStyle": {"fontSize": 16},
            "axisLabel": {"fontSize": 16}
        },
        "series": [{"data": abs_S, "type": "line", "name": "abs(S)"}],
        "height": 300,
        "dataZoom": [{"type": "slider", "start": 0, "end": 100, "height": 100, "bottom": 10}],
        "tooltip": {
            "trigger": "axis",
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
        "toolbox": {
            "feature": {
                # "dataView": { "show": "true", "readOnly": "true" },
                "restore": {"show": "true"},
            }
        },
    }
    events = {
        "dataZoom": "function(params) { return [params.start, params.end] }",
    }

    # show echart with dataZoom and update intervals based on output
    interval_range = st_echarts(
        options=options, events=events, height="500px", key="render_basic_bar_events"
    )

    if interval_range is None:
        interval_range = (0, 100)

    n = len(f)
    interval_start, interval_end = (
        int(n*interval_range[id]*0.01) for id in (0, 1))

# plot (abs(S))(f) chart with pyplot
def plot_ref_from_f(f, r, i):
    fig = plt.figure(figsize=(10, 10))
    abs_S = list((r[n] ** 2 + i[n] ** 2)**0.5 for n in range(len(r)))
    xlim = [min(f) - abs(max(f) - min(f)) * 0.1,
            max(f) + abs(max(f) - min(f)) * 0.1]
    ylim = [min(abs_S) - abs(max(abs_S) - min(abs_S)) * 0.5,
            max(abs_S) + abs(max(abs_S) - min(abs_S)) * 0.5]
    ax = fig.add_subplot()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(which='major', color='k', linewidth=1)
    ax.grid(which='minor', color='grey', linestyle=':', linewidth=0.5)
    plt.xlabel(r'$f,\; 1/c$', color='gray', fontsize=16, fontname="Cambria")
    plt.ylabel('$|S|$', color='gray', fontsize=16, fontname="Cambria")
    plt.title('Absolute value of reflection coefficient from frequency',
              fontsize=24, fontname="Cambria")

    ax.plot(f, abs_S, '+', ms=10, mew=2, color='#1946BA')
    st.pyplot(fig)


def run(calc_function):

    def is_float(element) -> bool:
        try:
            float(element)
            val = float(element)
            if math.isnan(val) or math.isinf(val):
                raise ValueError
            return True
        except ValueError:
            return False

    # to utf-8
    def read_data(data):
        for x in range(len(data)):
            if type(data[x]) == bytes:
                try:
                    data[x] = data[x].decode('utf-8-sig', 'ignore')
                except:
                    return 'Not an utf-8-sig line №: ' + str(x)
        return 'data read: success'

    # for Touchstone .snp format
    def parse_heading(data):
        nonlocal data_format_snp
        if data_format_snp:
            for x in range(len(data)):
                if data[x][0]=='#':
                    line = data[x].split()
                    if len(line)== 6:
                        repr_map = {"RI":0,"MA":1, "DB":2}
                        para_map = {"S":0,"Z":1}
                        hz_map = {"GHz":10**9,"MHz":10**6,"KHz":10**3,"Hz":1}
                        hz,measurement_parameter,data_representation,_r,ref_resistance=line[1:]
                        try:
                            return hz_map[hz], para_map[measurement_parameter], repr_map[data_representation], ref_resistance
                        except:
                            break
                    break
        return 1, 0, 0, 50
    

    def unpack_data(data, input_start_line, input_end_line):
        nonlocal select_measurement_parameter
        nonlocal select_data_representation
        f, r, i = [], [], []
        return_status='data parsed'
        for x in range(input_start_line-1, input_end_line):
            if len(data[x])<2 or data[x][0]== '!' or data[x][0]=='#' or data[x][0]=='%' or data[x][0]=='/':
                # first is a comment line according to .snp documentation,
                # others detects comments in various languages
                continue
            data[x] = data[x].replace(';', ' ').replace(',', ' ') # generally we expect these chars as seperators
            line = data[x].split()

            # always at least 3 values for single data point
            if len(line) < 3:
                return_status = 'Can\'t parse line №: ' + str(x) + ',\n not enough arguments (less than 3)'
                break

            # 1: process according to data_placement
            a,b,c=[],[],[]
            try:
                a, b, c = (line[y] for y in range(min(len(line),3)))
                    # for x in input_data_columns.keys():
                    #     if x=='f':

                    #     elif x=='r':

                    #     elif x=='i':
            except:
                return_status = 'Can\'t parse line №: ' + str(x) + ',\n not enough arguments'
                break    
            if not ((is_float(a)) or (is_float(b)) or (is_float(c))):
                return_status = 'Wrong data type, expected number. Error on line: ' + str(x)
                break
            a,b,c=(float(x) for x in (a,b,c))
            f.append(a)  # frequency

            # 2: process according to data_representation
            if select_data_representation == 'Frequency, real, imaginary':
                r.append(b)  # Re
                i.append(c)  # Im
            elif select_data_representation == 'Frequency, magnitude, angle':
                r.append(b*np.cos(np.deg2rad(c)))  # Re
                i.append(b*np.sin(np.deg2rad(c)))  # Im
            elif select_data_representation == 'Frequency, db, angle':
                b=10**(b/20)
                r.append(b*np.sin(np.deg2rad(c)))  # Re
                i.append(b*np.cos(np.deg2rad(c)))  # Im
            else:
                return_status = 'Wrong data format'
                break

            # 3: process according to measurement_parameter

        return f, r, i, return_status

    # make accessible specific range of numerical data choosen with interactive plot 
    global interval_range, interval_start, interval_end

    # file upload button
    data = []
    uploaded_file = st.file_uploader('Upload a csv')
    if uploaded_file is not None:
        data_format_snp = False
        data = uploaded_file.readlines()
        if uploaded_file.name[-4:-2]=='.s' and uploaded_file.name[-1]== 'p':
            data_format_snp = True
    
    validator_status = '...'
    ace_preview_markers = []

    # data loaded
    circle_params = []
    if len(data) > 0:

        validator_status = read_data(data)
        if validator_status == 'data read: success':
            hz, select_measurement_parameter, select_data_representation, input_ref_resistance=parse_heading(data)

            col1, col2 = st.columns(2)
            select_measurement_parameter = col1.selectbox('Measurement parameter',
                                                      ['S', 'Z'],
                                                      select_measurement_parameter)
            select_data_representation = col1.selectbox('Data representation',
                                                    ['Frequency, real, imaginary',
                                                     'Frequency, magnitude, angle',
                                                     'Frequency, db, angle'],
                                                     select_data_representation)
            if select_measurement_parameter=='Z':
                input_ref_resistance = col1.number_input(
                    "Reference resistance:", min_value=0, value=input_ref_resistance)                                    
            input_start_line = col1.number_input(
                "First line of data:", min_value=1, max_value=len(data))
            input_end_line = col1.number_input(
                "Last line of data:", min_value=1, max_value=len(data), value=len(data))

            f, r, i, validator_status = unpack_data(data, input_start_line, input_end_line)
            f = f * hz  # to hz

            # Ace editor to show choosen data columns and rows
            with col2.expander("File preview"):
                # So little 'official' functionality in libs and lack of documentation
                # therefore beware: css hacks 

                # yellow ~ ace_step
                # light yellow ~ ace_highlight-marker
                # green ~ ace_stack
                # red ~ ace_error-marker

                # no more good colors included in streamlit_ace for marking

                # st.markdown('''<style>
                # .choosen_option_1
                # {
                # color: rgb(49, 51, 63);
                # }</style>''', unsafe_allow_html=True)

                # markdown injection does not seems to work, since ace is in a different .html accessible via iframe

                # markers format:
                #[{"startRow": 2,"startCol": 0,"endRow": 2,"endCol": 3,"className": "ace_error-marker","type": "text"}]
                
                # add general marking for choosen data lines? better just mark the problematic lines?
                ace_preview_markers.append(
                    {"startRow": input_start_line,"startCol": 0,
                    "endRow": input_end_line+1,"endCol": 0,"className": "ace_highlight-marker","type": "text"})

                text_value = "Frequency,Hz  | Re(S11) | Im(S11)\n" + \
                    ''.join(data).strip()
                st_ace(value=text_value,
                       readonly=True,
                       auto_update=True,
                       placeholder="Your data is empty",
                       markers=ace_preview_markers,
                       height="300px")

            st.write("Use range slider to choose best suitable data interval")
            plot_interact_abs_from_f(f, r, i)

            select_coupling_losses = st.checkbox(
                'Apply corrections for coupling losses (lossy coupling)')
            f_cut, r_cut, i_cut = (x[interval_start:interval_end]
                                   for x in (f, r, i))
            # for x in range(len(f_cut)):
                # print(f_cut[x], r_cut[x], i_cut[x])
            if validator_status == 'data parsed':
                Q0, sigmaQ0, QL, sigmaQl, circle_params = calc_function(
                    f_cut, r_cut, i_cut, select_coupling_losses)
                if select_coupling_losses:
                    st.write("Lossy coupling")
                else:
                    st.write("Cable attenuation")

                out_precision = '0.7f'
                st.latex(r'Q_0 =' + f'{format(Q0, out_precision)} \pm {format(sigmaQ0, out_precision)},  ' +
                         r'\;\;\varepsilon_{Q_0} =' + f'{format(sigmaQ0 / Q0, out_precision)}')
                st.latex(r'Q_L =' + f'{format(QL, out_precision)} \pm {format(sigmaQl, out_precision)},  ' +
                         r'\;\;\varepsilon_{Q_L} =' + f'{format(sigmaQl / QL, out_precision)}')

    st.write("Status: " + validator_status)

    if len(data) > 0 and validator_status == 'data parsed':
        with st.expander("Show static abs(S) plot"):
            plot_ref_from_f(f_cut, r_cut, i_cut)
        plot_data(r_cut, i_cut, circle_params)
