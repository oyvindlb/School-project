# -*- coding: utf-8 -*-
"""
Created on Sat May  9 13:14:48 2020

@author: Eier
"""
import pymysql
import hoggorm as ho
import hoggormplot as hop
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

#Oppretter tilkobling til databasen på Raspberry Pi
connection = pymysql.connect("IP-adress", "username", "password")
cursor = connection.cursor()
cursor.execute("use mandatory2") #select database
cursor.execute("select * from Observations_View;")
data = cursor.fetchall()
print(len(data))

#Gjør SQL-resultatet om til en DataFrame:
names = [ i[0] for i in cursor.description]
df = pd.DataFrame(data, columns=names)
data_df = df.sample(n=10000,random_state=10000) #med random_state blir det tilfeldige utvalget det samme hver gang

#Bruker fit_transform til å lage en ny numerisk kategorivariabel basert på tekstkategori-variabel (string):
Le = LabelEncoder()
data_df["Station_ID_NUMERIC"] = Le.fit_transform(data_df["Station_ID"])

#Fjerner kolonnene (variablene) "index", "Date_Time" og "Station_ID"
#og tar kun med variablene som skal brukes i "model_data":
data_df.drop(["index", "Date_Time", "Station_ID"], axis=1, inplace=True)
model_data = data_df[['air_temp_set_1', 'altimeter_set_1','dew_point_temperature_set_1d',\
                      'pressure_set_1d','relative_humidity_set_1', 'sea_level_pressure_set_1d',\
                      'wind_speed_set_1']].values

    
    
#HOGGORM PCA OG HOGGORMPLOT:
data_varNames = ['air_temp_set_1', 'altimeter_set_1','dew_point_temperature_set_1d',\
                 'pressure_set_1d','relative_humidity_set_1', 'sea_level_pressure_set_1d',\
                 'wind_speed_set_1']    
data_objNames = list(data_df['Station_ID_NUMERIC'])

#For PCA Kan det brukes: loo = cross validation med leave one out
#eller cvType=["Kfold", 4] = k-fold cross validation
#Datainput standardiseres og centreres ved å sette Xstand=True
#Det kalkuleres 7 prinsipale komponenter og data
model = ho.nipalsPCA(arrX=model_data, numComp=7, cvType=["loo"], Xstand=True)

#Tre figurer lages: 1: Scores-plott, 2: Loadings-plott, 6: Explained varinace-plott
#her brukes hoggormplot:
hop.plot(model, plots=[1, 2, 6], XvarNames=data_varNames, objNames=data_objNames)

#SKLEARN PCA:
#Data'en standardiseres ved å bruke StandardScaler()
#Det brukes PCA med 7 prinsipale komponenter
pipeline = Pipeline([('Scaling', StandardScaler()), ('pca', PCA(n_components=7))])
X_reduced = pipeline.fit_transform(model_data)

#PLotting av de prinsipale komponentene PC1 og PC2
#Forskellige Station_ID har forskjellige farge
plt.figure()
plt.scatter(X_reduced[:,0], X_reduced[:,1], c=data_objNames)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

#Direkte plotting av model_data uten PCA (kun numerisk datagrunnlag):
#Kolonne 1 og 2 plottes
plt.figure()
plt.scatter(model_data[:,0], model_data[:,1], c=data_objNames)
plt.show()
