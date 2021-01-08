# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:34:44 2020

@author: Eier
"""
import pymysql

connection = pymysql.connect("IP-Adress", "Username", "Password")
cursor = connection.cursor()
cursor.execute("use mandatory2") #selecting dabase
cursor.execute("select * from Observations;")

names = [ i[0] for i in cursor.description]
data = cursor.fetchall()
print(len(data))
for i in range(len(names)):
    missing_number = 0
    NULL_number = 0
    for row in data:
        if (row[i] == 0):
            missing_number += 1
        if (row[i] == None):
            NULL_number += 1
    
    Zero_Missing_Percent = (missing_number / len(data))*100
    Null_Missing_Percent = (NULL_number / len(data))*100
    
    
    print("KolonneIndeks: {}   VariableName: {}   Prosent zero-missing verdier: {}   \
          Prosent NULL-missing verdier: {}".format(i, names[i],\
              Zero_Missing_Percent, Null_Missing_Percent))


    