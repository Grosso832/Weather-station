# Thanks a lot to Joan, my DataScience Instructor for helping me with this streamlit-app!

import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from functions import *
from sql_credentials import *

# set a nice theme for plotly
px.defaults.template = "plotly_dark"

weather = pd.read_sql("sensordata", con=con).assign(
    full_time=lambda x: pd.to_datetime(x["full_time"])
)

# add input bar at the left
st.sidebar.title("Weather Station")
select_station = st.sidebar.selectbox("Which station should be displayed", ("", 1, 2, "Both"))
# add informative message to select a station
if select_station == "":
    st.sidebar.warning("Please select a Client-Station - 1: Bureau / 2: Living-room")
else:
    # add input bar at the left
    select_data = st.sidebar.selectbox("Please select the data-type you want to display", ("", "temperature", "humidity", "pressure"))
    # add informative message to select a data type
    if select_data == "":
        st.sidebar.warning("Please select a data-type - temperature / humidity / pressure")
    else:
        add_time = st.sidebar.checkbox("Define time range")
        if add_time:
            datetime_min, datetime_max = create_calendar_inputs()

            # filter by datetime
            if st.sidebar.button("Submit"):
                df = weather[(weather["full_time"] >= datetime_min) & (weather["full_time"] <= datetime_max)]
                show_info(df, select_station, select_data)
        else: 
            show_info(weather, select_station, select_data)





