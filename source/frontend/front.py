import streamlit as st
import matplotlib.pyplot as plt

import numpy as np
import sigfig
from streamlit_ace import st_ace

from .draw_smith_utils import draw_smith_circle, plot_abs_s_gridlines, plot_im_z_gridlines, plot_re_z_gridlines
from .show_amplitude_echart import plot_interact_abs_from_f
from .data_parsing_utils import parse_snp_header, read_data, count_columns, prepare_snp, unpack_data


def plot_smith(r, i, g, r_cut, i_cut):
    # maintaining state again (remember options for this session)
    if 'smith_options' not in st.session_state:
        st.session_state.smith_options = (True, True, False, False, False)
    with st.expander("Smith chart options"):

        smith_options_input = (st.checkbox(
            "Show excluded points",
            value=st.session_state.smith_options[0]),
                               st.checkbox("Show grid",
                                           st.session_state.smith_options[1]),
                               st.checkbox(
                                   "Show |S| gridlines",
                                   value=st.session_state.smith_options[2],
                               ),
                               st.checkbox(
                                   "Show Re(Z) gridlines",
                                   value=st.session_state.smith_options[3],
                               ),
                               st.checkbox(
                                   "Show Im(Z) gridlines",
                                   value=st.session_state.smith_options[4],
                               ))
        if st.session_state.smith_options != smith_options_input:
            st.session_state.smith_options = smith_options_input
            st.experimental_rerun()

    (show_excluded_points, show_grid, show_Abs_S_gridlines,
     show_Re_Z_gridlines, show_Im_Z_gridlines) = st.session_state.smith_options
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot()
    ax.axis('equal')
    minor_ticks = np.arange(-1.1, 1.1, 0.05)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(minor_ticks, minor=True)
    ax.grid(which='major', color='grey', linewidth=1.5)
    ax.grid(which='minor', color='grey', linewidth=0.5, linestyle=':')
    plt.xlabel('$Re(S)$', color='gray', fontsize=16, fontname="Cambria")
    plt.ylabel('$Im(S)$', color='gray', fontsize=16, fontname="Cambria")
    plt.title('Smith chart', fontsize=24, fontname="Cambria")

    # unit circle
    draw_smith_circle(ax, 0, 0, 1, '#1946BA')

    if not show_grid:
        ax.axis('off')

    if show_Abs_S_gridlines:
        # imshow is extremely slow, so draw it in place
        plot_abs_s_gridlines(ax)

    if show_Re_Z_gridlines:
        plot_re_z_gridlines(ax)

    if show_Im_Z_gridlines:
        plot_im_z_gridlines(ax)

    # input data points
    if show_excluded_points:
        ax.plot(r, i, '+', ms=8, mew=2, color='#b6c7f4')

    # choosen data points
    ax.plot(r_cut, i_cut, '+', ms=8, mew=2, color='#1946BA')

    # S-circle approximation by calc
    radius = abs(g[1] - g[0] / g[2]) / 2
    x = ((g[1] + g[0] / g[2]) / 2).real
    y = ((g[1] + g[0] / g[2]) / 2).imag
    draw_smith_circle(ax, x, y, radius, color='#FF8400')

    XLIM = [-1.3, 1.3]
    YLIM = [-1.3, 1.3]
    ax.set_xlim(XLIM)
    ax.set_ylim(YLIM)
    try:
        st.pyplot(fig)
    except:
        st.write('Unexpected plot error')


# plot abs(S) vs f chart with pyplot
def plot_abs_vs_f(f, r, i, fitted_mag_s):
    fig = plt.figure(figsize=(10, 10))
    s = np.abs(np.array(r) + 1j * np.array(i))
    if st.session_state.legendselection == '|S| (dB)':
        m = np.min(np.where(s == 0, np.inf, s))
        s = list(20 * np.where(s == 0, np.log10(m), np.log10(s)))
        m = np.min(np.where(s == 0, np.inf, fitted_mag_s))
        fitted_mag_s = list(
            20 * np.where(s == 0, np.log10(m), np.log10(fitted_mag_s)))
    s = list(s)
    min_f = min(f)
    max_f = max(f)
    xlim = [min_f - abs(max_f - min_f) * 0.1, max_f + abs(max_f - min_f) * 0.1]
    min_s = min(s)
    max_s = max(s)
    ylim = [min_s - abs(max_s - min_s) * 0.5, max_s + abs(max_s - min_s) * 0.5]
    ax = fig.add_subplot()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(which='major', color='k', linewidth=1)
    ax.grid(which='minor', color='grey', linestyle=':', linewidth=0.5)
    plt.xlabel(r'$f,\; 1/c$', color='gray', fontsize=16, fontname="Cambria")
    if st.session_state.legendselection == '|S| (dB)':
        plt.ylabel('$|S|$ (dB)', color='gray', fontsize=16, fontname="Cambria")
        plt.title('|S| (dB) vs frequency', fontsize=24, fontname="Cambria")
    else:
        plt.ylabel('$|S|$', color='gray', fontsize=16, fontname="Cambria")
        plt.title('|S| vs frequency', fontsize=24, fontname="Cambria")

    ax.plot(f, s, '+', ms=8, mew=2, color='#1946BA')

    ax.plot(f, fitted_mag_s, '-', linewidth=3, color='#FF8400')

    try:
        st.pyplot(fig)
    except:
        st.write('Unexpected plot error')

def run(calc_function):
    # info
    with st.expander("Info"):
        # streamlit.markdown does not support footnotes
        try:
            with open('./source/frontend/info.md') as f:
                st.markdown(f.read())
        except:
            st.write('Wrong start directory, see readme')

    # file upload button
    uploaded_file = st.file_uploader(
        'Upload a file from your vector analizer. \
        Make sure the file format is .snp or it has a similar inner structure.'
    )

    # check .snp
    is_data_format_snp = False
    data_format_snp_number = 0
    if uploaded_file is None:
        st.write("DEMO: ")
        # display DEMO
        is_data_format_snp = True
        try:
            with open('./resource/data/8_default_demo.s1p') as f:
                data = f.readlines()
        except:
            # 'streamlit run' call in the wrong directory. Display smaller demo:
            data = [
                '# Hz S MA R 50\n\
                11415403125 0.37010744 92.47802\n\
                11416090625 0.33831283 92.906929\n\
                11416778125 0.3069371 94.03318'
            ]
    else:
        data = uploaded_file.readlines()
        if uploaded_file.name[-4:-2] == '.s' and uploaded_file.name[-1] == 'p':
            is_data_format_snp = True
            data_format_snp_number = int(uploaded_file.name[-2])

    validator_status = '...'
    column_count = 0

    # data loaded
    circle_params = []
    if len(data) > 0:

        validator_status = read_data(data)
        if validator_status == 'data read, but not parsed':
            hz, select_measurement_parameter, select_data_representation, input_ref_resistance = parse_snp_header(
                data, is_data_format_snp)

            col1, col2 = st.columns([1, 2])

            ace_text_value = ''.join(data).strip()
            with col1.expander("Processing options"):
                select_measurement_parameter = st.selectbox(
                    'Measurement parameter', ['S', 'Z'],
                    select_measurement_parameter)
                select_data_representation = st.selectbox(
                    'Data representation', [
                        'Frequency, real, imaginary',
                        'Frequency, magnitude, angle', 'Frequency, db, angle'
                    ], select_data_representation)
                if select_measurement_parameter == 'Z':
                    input_ref_resistance = st.number_input(
                        "Reference resistance:",
                        min_value=0,
                        value=input_ref_resistance)
                if not is_data_format_snp:
                    input_hz = st.selectbox('Unit of frequency',
                                            ['Hz', 'KHz', 'MHz', 'GHz'], 0)
                    hz_map = {
                        "ghz": 10**9,
                        "mhz": 10**6,
                        "khz": 10**3,
                        "hz": 1
                    }
                    hz = hz_map[input_hz.lower()]
                input_start_line = int(
                    st.number_input("First line for processing:",
                                    min_value=1,
                                    max_value=len(data)))
                input_end_line = int(
                    st.number_input("Last line for processing:",
                                    min_value=1,
                                    max_value=len(data),
                                    value=len(data)))
                if input_end_line < input_start_line:
                    input_end_line=input_start_line
                data = data[input_start_line - 1:input_end_line]

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

                # markdown injection does not seems to work,
                # since ace is in a different .html accessible via iframe

                # markers format:
                #[{"startRow": 2,"startCol": 0,"endRow": 2,"endCol": 3,"className": "ace_error-marker","type": "text"}]

                # add marking for choosen data lines?
                # todo or not todo?
                ace_preview_markers =[{
                    "startRow": input_start_line - 1,
                    "startCol": 0,
                    "endRow": input_end_line,
                    "endCol": 0,
                    "className": "ace_highlight-marker",
                    "type": "text"
                }]

                st_ace(value=ace_text_value,
                       readonly=True,
                       auto_update=True,
                       placeholder="Your file is empty",
                       markers=ace_preview_markers,
                       height="300px")

            if is_data_format_snp and data_format_snp_number >= 3:
                data, validator_status = prepare_snp(data,
                                                     data_format_snp_number)

    if validator_status == "data read, but not parsed":
        column_count, validator_status = count_columns(data)

    f, r, i = [], [], []
    if validator_status == "data parsed":
        input_ports_pair = 1
        if column_count > 3:
            pair_count = (column_count - 1) // 2
            input_ports_pair = st.number_input(
                "Choose pair of ports with network parameters:",
                min_value=1,
                max_value=pair_count,
                value=1)
            input_ports_pair_id = input_ports_pair - 1
            ports_count = round(pair_count**0.5)
            st.write('Choosen ports: ' + select_measurement_parameter +
                     str(input_ports_pair_id // ports_count + 1) +
                     str(input_ports_pair_id % ports_count + 1))
        f, r, i, validator_status = unpack_data(data,
                                                (input_ports_pair - 1) * 2 + 1,
                                                column_count,
                                                input_ref_resistance,
                                                select_measurement_parameter,
                                                select_data_representation)
        f = [x * hz for x in f]  # to hz

    st.write("Use range slider to choose best suitable data interval")

    if len(f)==0:
        validator_status = 'data unpacking error: empty data'
    else:
        # make accessible a specific range of numerical data choosen with interactive plot
        # line id, line id
        interval_start, interval_end = plot_interact_abs_from_f(f,r,i)
    
        f_cut, r_cut, i_cut = [], [], []
        if validator_status == "data parsed":
            f_cut, r_cut, i_cut = (x[interval_start:interval_end]
                                   for x in (f, r, i))
            with st.expander("Selected data interval as .s1p"):
                st_ace(value="# Hz S RI R 50\n" +
                       ''.join(f'{f_cut[x]} {r_cut[x]} {i_cut[x]}\n'
                               for x in range(len(f_cut))),
                       readonly=True,
                       auto_update=True,
                       placeholder="Selection is empty",
                       height="150px")
    
            if len(f_cut) < 3:
                validator_status = "Choosen interval is too small, add more points"

    st.write("Status: " + validator_status)

    if validator_status == "data parsed":
        col1, col2 = st.columns(2)

        check_coupling_loss = col1.checkbox(
            'Apply correction for coupling losses', value = False)

        if check_coupling_loss:
            col1.write("Option: Lossy coupling")
        else:
            col1.write("Option: Cable attenuation")

        select_autoformat = col2.checkbox("Autoformat output", value=True)
        precision = '0.0f'
        if not select_autoformat:
            precision = col2.slider("Precision",
                                    min_value=0,
                                    max_value=7,
                                    value=4)
            precision = '0.' + str(precision) + 'f'

        Q0, sigmaQ0, QL, sigmaQL, k, ks, circle_params, fl, fitted_mag_s = calc_function(
            f_cut, r_cut, i_cut, check_coupling_loss)

        if Q0 <= 0 or QL <= 0:
            st.write("Negative Q detected, fitting may be inaccurate!")

        def show_result_in_latex(name, value, uncertainty=None):
            nonlocal select_autoformat
            if uncertainty is not None:
                if select_autoformat:
                    st.latex(
                        name + ' =' +
                        f'{sigfig.round(value, uncertainty=uncertainty, style="PDG")},  '
                        + r'\;\;\varepsilon_{' + name + '} =' +
                        f'{sigfig.round(uncertainty / value, sigfigs=1, style="PDG")}'
                    )
                else:
                    st.latex(name + ' =' + f'{format(value, precision)} \pm ' +
                             f'{format(uncertainty, precision)},  ' +
                             r'\;\;\varepsilon_{' + name + '} =' +
                             f'{format(uncertainty / value, precision)}')
            else:
                if select_autoformat:
                    st.latex(name + ' =' +
                             f'{sigfig.round(value, sigfigs=5, style="PDG")}')
                else:
                    st.latex(name + ' =' + f'{format(value, precision)}')

        show_result_in_latex('Q_0', Q0, sigmaQ0)
        show_result_in_latex('Q_L', QL, sigmaQL)
        show_result_in_latex(r'\kappa', k)
        if check_coupling_loss:
            show_result_in_latex(r'\kappa_s', ks)

        st.latex('f_L =' + f'{format(fl, precision)}' + r'\text{ }Hz')

        with st.expander("Show static abs(S) plot"):
            plot_abs_vs_f(f_cut, r_cut, i_cut, fitted_mag_s)

        plot_smith(r, i, circle_params, r_cut, i_cut)
