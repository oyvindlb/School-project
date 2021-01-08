# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:53:58 2020

@author: Eier
"""

import pandas as pd
import pymysql

#Importerer datasettet som en Pandas DataFrame
data = pd.read_csv(r"C:\Users\Eier\Documents\Skole\INF230\Oblig 2\all_weather_data.csv", sep=";")

#Finner at wind_cardinal_direction_set_1d har 7880 missing value (ingen verdi, dvs. NULL):
print(data.isnull().sum()) 
print(data)

#Setter 7880 tomme verdier til tomme String's. Disse gjøres senere om til NULL verdier i MySQL:
data.fillna('', inplace=True)

#Oppretter tilkobling til Raspberry pi MariaDB server:
connection = pymysql.connect("IP-adress", "Username", "Password")
cursor = connection.cursor()


#Bruker den nylig lagde databasen mandatory2 og kjører følgende sql-kode for å lage tabellen Observations. 
#Verdiene i dataframe'en importeres til den nye tabellen:
cursor.execute("use mandatory2") #select database
cursor.execute("CREATE TABLE Observations (`index` INT, Date_Time DATETIME,\
               Station_ID VARCHAR(20), air_temp_set_1 FLOAT, altimeter_set_1 FLOAT,\
               dew_point_temperature_set_1d FLOAT, heat_index_set_1d FLOAT,\
               pressure_set_1d FLOAT, relative_humidity_set_1 FLOAT,\
               sea_level_pressure_set_1d FLOAT, weather_cond_code_set_1 FLOAT,\
               wind_cardinal_direction_set_1d VARCHAR(20), wind_chill_set_1d FLOAT,\
               wind_direction_set_1 FLOAT, wind_gust_set_1 FLOAT, wind_speed_set_1 FLOAT)")
cursor.executemany("INSERT INTO Observations VALUES (%s, %s, %s, %s, %s, %s,\
                   %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data.values.tolist())
connection.commit() 
