# -*- coding: utf-8 -*-
"""
Created on Thu May  6 16:13:49 2021

@author: krist
"""

from csv import writer
import pandas as pd
import requests
import json # importerer biblioteker
import datetime as dt

def prod_week():
    week = dt.datetime.now().isocalendar()[1] # henter ukenummer
    prod_week_df = pd.read_csv('csvfiler/Panel_production_day.csv')
    prod_week_df.to_csv('temp_csv/Panel_prod_week.csv', index=False) # putter data fra Panel_production_day inn i  panel_prod_week

    with open('temp_csv/Panel_prod_week.csv', 'a') as bt:
         prod_temp_df = writer(bt)
         prod_temp_df.writerow([week, '-', 0]) # skriver tom csv fil
        
    prod_this_week_df = pd.read_csv('temp_csv/Panel_prod_week.csv', index_col='Week')
    prod_week = sum(prod_this_week_df.at[week, 'kWh']) # regner ut summen av kWh kollonen
    
    key ='2605'
    token= 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NzUxIn0.DeRcDo1IRe0fFV_IEw8WyUbEd02hwzWikjARXvc2oEE' # info til CoT

    data = {'Key': key, 'Value': prod_week, 'Token': token}

    p = requests.put('https://circusofthings.com/WriteValue',   #sender ukes produksjon til CoT
         data = json.dumps(data), 
         headers={'Content-Type': 'application/json'} )

    with open('csvfiler/Panel_production_week.csv', 'a') as pw:
        prod_df = writer(pw)
        prod_df.writerow([week, prod_week]) # skriver uke nummer + ukesproduksjon til csvfil
        
    return prod_week
