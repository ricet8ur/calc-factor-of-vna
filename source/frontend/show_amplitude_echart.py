import streamlit as st
import numpy as np
from streamlit_echarts import st_echarts, JsCode


# So that you can choose an interval of points on which we apply q-calc algorithm
def plot_interact_abs_from_f(f, r, i):
    # for making it work smoothly with streamlit
    if 'start' not in st.session_state or 'end' not in st.session_state:
        st.session_state.start = 0
        st.session_state.end = 100
    if 'legendselection' not in st.session_state:
        st.session_state.legendselection = '|S|'

    # data
    s = np.abs(np.array(r) + 1j * np.array(i))
    abs_S = list(s)
    # case (s[x] = 0) => (log10(s[x]) = log10(min(s)))
    m = np.max(np.where(s == 0, 10**-50, s)) # where 10**-50 ~ 0
    db_abs_S = list(20 * np.where(s == 0, np.log10(m), np.log10(s)))
    # echarts for datazoom https://discuss.streamlit.io/t/streamlit-echarts/3655
    # datazoom https://echarts.apache.org/examples/en/editor.html?c=line-draggable&lang=ts
    # axis pointer values https://echarts.apache.org/en/option.html#axisPointer
    options = {
        "legend": {
            "data": ['|S|', '|S| (dB)'],
            "selectedMode": "single",
            "selected": {
                '|S|': st.session_state.legendselection == '|S|',
                '|S| (dB)': st.session_state.legendselection == '|S| (dB)'
            }
        },
        "xAxis": {
            "type": "category",
            "data": f,
            "name": "Hz",
            "nameTextStyle": {
                "fontSize": 16
            },
            "axisLabel": {
                "fontSize":
                16,
                "formatter":
                JsCode(
                    "function(x){return Intl.NumberFormat('en-US').format(x).replaceAll(',',\"_\")}"
                ).js_code
            },
            "axisPointer": {
                "label": {
                    "formatter":
                    JsCode(
                        "function(x){return Intl.NumberFormat('en-US').format(x.value).replaceAll(',',\"_\")}"
                    ).js_code
                }
            }
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {
                "fontSize": 16,
            },
        },
        "series": [{
            "name": "|S|",
            "data": abs_S,
            "type": "line",
        }, {
            "name": "|S| (dB)",
            "data": db_abs_S,
            "type": "line",
        }],
        "height":
        300,
        "dataZoom": [{
            "type": "slider",
            "start": st.session_state.start,
            "end": st.session_state.end,
            "height": 100,
            "bottom": 10
        }],
        "tooltip": {
            "trigger":
            "axis",
            "axisPointer": {
                "type": 'cross',
                "label": {
                    "show": "true",
                }
            },
            "formatter":
            JsCode("function(x){\
                return \"frequency: \" + Intl.NumberFormat('en-US').format(x[0].name).replaceAll(',',\"_\")\
                    + \" Hz<br>\" + x[0].seriesName + \": \" + x[0].data.toFixed(3) \
            }").js_code
        },
        "toolbox": {
            "feature": {
                "restore": {
                    "show": "true"
                },
            }
        },
    }

    events = {
        "dataZoom":
        "function(params) { return ['dataZoom', params.start, params.end] }",
        "restore":
        "function() { return ['restore'] }",
        "legendselectchanged":
        "function(params){ return ['legendselectchanged', params.name] }"
    }

    # show echart with dataZoom and update intervals based on output
    e = st_echarts(options=options,
                   events=events,
                   height="500px",
                   key="echart_S")
    # e - event from echarts
    if e:
        # DataZoom event is not fired on new file upload (and in some other cases)
        # There is no 'default event' to fix it, so use st.experimental_rerun() with session_state
        if e[0] == "restore":
            if 0 != st.session_state.start or 100 != st.session_state.end:
                st.session_state.start = 0
                st.session_state.end = 100
                st.experimental_rerun()

        elif e[0] == "dataZoom":
            if e[1] != st.session_state.start or e[2] != st.session_state.end:
                st.session_state.start = e[1]
                st.session_state.end = e[2]
                st.experimental_rerun()

        elif e[0] == "legendselectchanged":
            if e[1] != st.session_state.legendselection:
                # Save selected type of series to state
                st.session_state.legendselection = e[1]
                # make chart state the same as actual state
                st.experimental_rerun()

    n = len(f)
    interval_start, interval_end = int(n * st.session_state.start * 0.01), int(
        n * st.session_state.end * 0.01)
    return interval_start, interval_end