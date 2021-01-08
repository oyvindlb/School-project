# -*- coding: utf-8 -*-
"""
Created on Thu May  7 17:31:02 2020

@author: Eier
"""
#2019-04-01 00:00:00

import pymysql
import matplotlib.pyplot as plt
from datetime import datetime

def fetching(Station_ID):
    connection = pymysql.connect("IP-adress", "Username", "Password")
    cursor = connection.cursor()
    cursor.execute("use mandatory2") #select database
    sql="select Date_Time, heat_index_set_1d, air_temp_set_1, wind_speed_set_1,\
        wind_gust_set_1 from Observations where Station_ID = '{}';".format(Station_ID)
    cursor.execute(sql)
    return cursor.fetchall()


    
def figure_print(data_fetched, Station_ID):
    DateTime = []
    heat_index_set_1d = []
    air_temp_set_1 = []
    wind_speed_set_1 = []
    wind_gust_set_1 = []

    for row in data_fetched:
        #print(row)

        DateTime.append(datetime.strptime(str(row[0]), "%Y-%m-%d %H:%M:%S"))
        heat_index_set_1d.append(float(row[1]))
        air_temp_set_1.append(float(row[2]))
        wind_speed_set_1.append(float(row[3]))
        wind_gust_set_1.append(float(row[4]))

    #Gjør om 0-verdier til NaN (not a number) ved bruk av list comprehension, 
    #slik at disse ikke vises ikke tas med i figurene.
    #Eventuelle NULL-verdier (None i python) gjøres også om til NaN. 
    FIXED_DateTime = [float('nan') if (i==0) or (i==None) else i for i in DateTime] 
    FIXED_heat_index_set_1d = [float('nan') if (i==0) or (i==None) else i for i in heat_index_set_1d] 
    FIXED_air_temp_set_1 = [float('nan') if (i==0) or (i==None) else i for i in air_temp_set_1] 
    FIXED_wind_speed_set_1 = [float('nan') if (i==0) or (i==None) else i for i in wind_speed_set_1]
    FIXED_wind_gust_set_1 = [float('nan') if (i==0) or (i==None) else i for i in wind_gust_set_1]
    
    
    plt.figure("Multiple plot", figsize=(12,8))
    plt.plot(FIXED_DateTime, FIXED_heat_index_set_1d)
    plt.plot(FIXED_DateTime, FIXED_air_temp_set_1)
    plt.title("Plot av Station_ID = {}".format(Station_ID))
    plt.xlabel("DateTime")
    plt.legend(["heat_index_set_1d","air_temp_set_1"], loc="upper left")
    plt.xticks(rotation=30)
    plt.show()
    plt.clf()

    plt.figure("Multiple plot", figsize=(12,8))
    plt.plot(FIXED_DateTime, FIXED_wind_speed_set_1)
    plt.plot(FIXED_DateTime, FIXED_wind_gust_set_1)
    plt.title("Plot av Station_ID = {}".format(Station_ID))
    plt.xlabel("DateTime")
    plt.legend(["wind_speed_set_1","wind_gust_set_1"], loc="upper left")
    plt.xticks(rotation=30)
    plt.show()
    

if __name__== "__main__":
    #Stations: FGBT, FMMI
    figure_print(fetching('FGBT'), "FGBT")
    figure_print(fetching("FMMI"), "FMMI")
    
    #EKSEMPELPLOT:
    #figure_print(fetching("DTTD"), "DTTD")




