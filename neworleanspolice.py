# -*- coding: utf-8 -*-

"""

Created on Fri Oct 11 2019



@author: nathalie descusse-brown



This file documents the analysis performed as part of the BP data science bootcamp pre-assessment

analysis with Python 3.7.3 64-bit

"""

# First we want to explore the data and see what the data look like

import os

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import statistics

from datetime import datetime

print("Current Working Directory " , os.getcwd())

df_servicedata = pd.read_csv('Calls_for_Service_2012.csv')

df_servicedata.head()

#Question a. 
#Which zipcode has the most incidents in this dataset? 
#What percentage of all incidents occur in this zipcode? 
#The zipcode of each incident is recorded under column "Zip".

#totalincidents=df_servicedata.NOPD_Item.count()

#incidentsperzip=df_servicedata.groupby('Zip') 

#total_incidentsperzip=incidentsperzip.count() 

totalzip=df_servicedata['Zip'].value_counts().index.tolist() #.unstack(level=0)
totalcountzip=df_servicedata['Zip'].value_counts().values.tolist() #.unstack(level=0)

print('ANSWER TO QUESTION A')
print('the zip code with the most incidents in this dataset is:',int(totalzip[0]))
#print((totalzip,totalcount))
firstzipincidentrate=100*totalcountzip[0]/sum(totalcountzip)
print('the percentage of all incidents that occur in this zipcode is: ','{0:.10f}'.format(round(firstzipincidentrate,10)))

del totalcountzip,firstzipincidentrate

#Question b.
#Compute the number of incidents handled by each police district in the data set. 
#What is the mean number of incidents a police district in New Orleans handled in 2012? 
#What is the standard deviation of the number of incidents a police district handled? 
#The police district is recorded under column "PoliceDistrict".


totaldistrict=df_servicedata['PoliceDistrict'].value_counts().index.tolist() 
totalcountdistrict=df_servicedata['PoliceDistrict'].value_counts().values.tolist() 
#print((totaldistrict,totalcountdistrict))
meantotalcountdistrict=statistics.mean(totalcountdistrict)
stdtotalcountdistrict=statistics.stdev(totalcountdistrict)

incidentsperdistrict=pd.DataFrame(
    {'Police district': totaldistrict,
     'Incidents': totalcountdistrict,
    })

print('ANSWER TO QUESTION B')
print('the number of incidents handled by each police district in the data set is as follows',incidentsperdistrict)
print('the mean number of incidents a police district in New Orleans handled in 2012 is:','{0:.10f}'.format(round(meantotalcountdistrict,10)))
print('the standard deviation of the number of incidents a police district handled is:','{0:.10f}'.format(round(stdtotalcountdistrict,10)))

#Question c.
#Which zipcode in this data set had zero incidents of bicycle theft in 2012? 
#Incident type is described in column "TypeText" where bicycle theft is recorded as BICYCLE THEFT. 
#The zipcode of each incident is recorded under column "Zip".

bicycletheft=df_servicedata.loc[df_servicedata['TypeText'] == 'BICYCLE THEFT']
bicycletheftbyzip=bicycletheft['Zip'].value_counts().index.tolist() 
bicycletheftbyzipcount=bicycletheft['Zip'].value_counts().values.tolist() 
#print(bicycletheftbydistrict,bicycletheftbydistrictcount)


totalzipint=list(map(int, totalzip))
bicycletheftbyzipint=list(map(int,bicycletheftbyzip))
bicycletheftfreezip=np.setdiff1d(totalzipint,bicycletheftbyzipint)

print('ANSWER TO QUESTION C')
print('the zipcode in this data set that had zero incidents of bicycle theft in 2012 is:',int(bicycletheftfreezip))

del bicycletheft,bicycletheftbyzip,bicycletheftbyzipcount,bicycletheftbyzipint,bicycletheftfreezip

#Question d.
#What percentage of all incidents handled by the police district that handles most incidents are unfounded calls? 
#The police district handling a case is recorded under column "PoliceDistrict". 
#An unfounded call is recorded under column "DispositionText" as UNFOUNDED.

unfoundedincidents=df_servicedata.loc[df_servicedata['DispositionText'] == 'UNFOUNDED']
unfoundedincidentsbydistrict=unfoundedincidents['PoliceDistrict'].value_counts().index.tolist() 
unfoundedincidentsbydistrictcount=unfoundedincidents['PoliceDistrict'].value_counts().values.tolist() 

indexdistrict=unfoundedincidentsbydistrict.index(1)

unfoundedincidentintopdistrict=unfoundedincidentsbydistrictcount[indexdistrict]
unfoundedincidentintopdistrictrate=100*unfoundedincidentintopdistrict/totalcountdistrict[0]

print('ANSWER TO QUESTION D')
print('the percentage of all incidents handled by the police district that handles most incidents which are unfounded calls is:','{0:.10f}'.format(round(unfoundedincidentintopdistrictrate,10)))

del totaldistrict,totalcountdistrict,unfoundedincidents,unfoundedincidentsbydistrict,unfoundedincidentsbydistrictcount
del indexdistrict,unfoundedincidentintopdistrictrate

#Question e.
#On average, how many minutes does it take for a unit to arrive on the
#scene of an incident from the moment the incident is reported?
#The time it takes for a unit to arrive is the time between the time logged 
#in column "TimeCreate" and the time logged in column "TimeArrive".

d=df_servicedata[['TimeArrive','TimeCreate']]
d['TimeArrive_converted'] = d['TimeArrive'].astype('datetime64[ns]')
d['TimeCreate_converted']= d['TimeCreate'].astype('datetime64[ns]')
d['TimeDiff']=d['TimeArrive_converted']-d['TimeCreate_converted']

d['TimeDiff_minutes']=d['TimeDiff']/np.timedelta64(1, 'm')

l = []
for i in range(0,len(d['TimeDiff_minutes'])):
    if ~np.isnan(d['TimeDiff_minutes'][i]):
        l.append(d['TimeDiff_minutes'][i])
        
timetoacc=sum(l)/len(l)

print('ANSWER TO QUESTION E')    
print('on average, it takes','{0:.10f}'.format(round(timetoacc,10)),'minutes for a unit to arrive at the scene of an accident')
    