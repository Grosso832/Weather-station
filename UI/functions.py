import plotly.express as px
import pandas
import streamlit as st
import datetime

def plot_single_station(df, station, sensor):

    df = df[df["name_id"] == station]
    st.title(f'{sensor.capitalize()} from Client-Station {str(station)}')
    # plotly line plot
    fig = px.line(
        df, x="full_time", y=sensor, 
        labels={
            "name_id": "Station", 
            "full_time": "Time",}
    )
    st.plotly_chart(fig)

def plot_all_stations(df, stations, sensor):
    
    st.title(
        f'''
        {sensor.capitalize()} from Client-Station {
            str(stations)
            .replace("[", "")
            .replace("]", "")
            .replace(", ", " and ")}
        ''')
    # plotly line separated by station
    fig = px.line(
        df, x="full_time", y=sensor, color="name_id",
        # add label to x-axis for station name
        labels={
            "name_id": "Station", 
            "full_time": "Time",}
        )
    st.plotly_chart(fig)

def print_max_info(df): 
    st.dataframe(
        df
        # filter by max date
        .loc[df["full_time"] == df["full_time"].max()]
        # select temperature, humidity, and pressure
        .loc[:, ["name_id", "temperature", "humidity", "pressure"]]
        # rename columns
        .rename(columns={
            "name_id": "Station", 
            "temperature": "Temperature", 
            "humidity": "Humidity", 
            "pressure": "Pressure"})
        # reset index
        .reset_index(drop=True)
    )

def show_info(df, select_station, select_data):        
    if select_station == "Both":   
        # print last as a message
        
        select_station = [1, 2]
        print_max_info(df[df["name_id"].isin(select_station)])
        plot_all_stations(
            df[df["name_id"].isin(select_station)], 
            select_station, select_data)
    else:
        print_max_info(df[df["name_id"] == select_station])
        plot_single_station(df, select_station, select_data)

def create_calendar_inputs(): 
    # create a date and time input
    date_min = st.sidebar.date_input("Start date")
    time_min = st.sidebar.time_input("Start time")


    date_max = st.sidebar.date_input("End date", datetime.date.today() + datetime.timedelta(days=1))
    if date_max < date_min:
        st.sidebar.warning("Please select a date after the start date")
    time_max = st.sidebar.time_input("End time")
    if (time_max < time_min) & (date_max == date_min):
        st.sidebar.warning("Please select a time after the start time")

    # convert date and time to datetime
    datetime_min = datetime.datetime.combine(date_min, time_min)
    datetime_max = datetime.datetime.combine(date_max, time_max)

    return datetime_min, datetime_max