import pandas as pd
import time
import json
import datetime as dt
import requests as rq
from sqlalchemy.ext.declarative import declarative_base


# Create Dataframe to insert sensor-data
df = pd.DataFrame(columns=['data_year', 'data_month', 'data_day', 'data_time', 'full_time', 'name_id', 'temperature', 'humidity', 'pressure'])

ips = ["http://192.168.178.77/json", "http://192.168.178.80/json"]
# Function to retrieve data from sensor/microcontroller and to store it in a library
def get_data(ip):
    sensor_data = rq.get(ip).json()
    time = dt.datetime.now()
    c_year = time.strftime('%Y')
    c_month = time.strftime('%m')
    c_day = time.strftime('%d')
    c_time = time.strftime('%X')
    c_time_full = time
    all_data = {'data_year': c_year, 'data_month': c_month, 'data_day': c_day, 'data_time': c_time, 'full_time': c_time_full, 'name_id': sensor_data['name'], 'temperature': sensor_data['temperature'],
                'humidity': sensor_data['humidity'], 'pressure': sensor_data['pressure'] }
    #return c_year, c_month, c_day, c_time, sensor_data['name'], sensor_data['temperature'], sensor_data['humidity'], sensor_data['pressure']
    return all_data

# Function to upload data to SQL-Database:
def upload_tosql():
    df.to_sql('sensordata', con=con, if_exists='append', index=False)

# Defining credentials for SQL-Server - SHOULD BE EXTRACTED IN A DIFFERENT MODULE!!!!!!
schema="final_project"
host="192.168.178.24"
user="upload_pi"
password="fure3132"
port=3306
con = f'mariadb+pymysql://{user}:{password}@{host}:{port}/{schema}'


while True:
    for ip in ips:
        # Creating data in 3 steps:
        # 1. Adding data to pandas-table -then closing the reqests-connection
        df = df.append(get_data(ip), ignore_index=[0])
    rq.session().close()
    # 2. uploading the Data to Database
    upload_tosql()
    # 3. Deleting data, which was uploaded before
    df.drop(df.index, inplace=True)
    time.sleep(60)