# -*- coding: utf-8 -*-
"""
Created on Mon May  3 12:18:01 2021

@author: krist
"""

from csv import writer
import pandas as pd
import requests
import json # importerer biblioteker
import datetime as dt

token = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NzUxIn0.DeRcDo1IRe0fFV_IEw8WyUbEd02hwzWikjARXvc2oEE'
bill_key = '18287' # info til CoT
panel_key = '8718'
consumption_key = '29260'
nettleie = 0.6 #Kr/kWh

def panelprod_day():
    current_date = dt.datetime.now().strftime('%d-%m-%y')
    week_num = dt.datetime.now().isocalendar()[1] # henter dato og ukenummer
    
    panel_csv = pd.read_csv('temp_csv/Panel_production_hour.csv',index_col='Date').at[current_date, 'kWh'] # leser kWh outputtet for current_date
    total_production = 0
    for i in range(len(panel_csv)):
        total_production += panel_csv[i]
    total_production = round(total_production, 2) # legger sammen alle kWh outputtene for hver time
    
    with open('csvfiler/Panel_production_day.csv', 'a') as prd:
        prod_df = writer(prd)
        prod_df.writerow([week_num, current_date, total_production]) # skriver ukenummer, dato og total kWh produksjon til csv fil
    
    return total_production

def bill():
    current_date = dt.datetime.now().strftime('%d-%m-%y')
    week_num = dt.datetime.now().isocalendar()[1]
    
    consumption = pd.read_csv('csvfiler/Electricety_consumption.csv', index_col='Date').at[current_date, 'kWh']
    el_price = pd.read_csv('temp_csv/avg_price_day.csv',index_col='Date').at[current_date, 'Kr/kWh'] + nettleie # regner ut strømpris pris/kWh + nettleie
    
    total = consumption - panelprod_day() # regner ut totalt forbruk, forbruk - produksjon
    with open('csvfiler/total_consumption.csv', 'a') as t:
        prod_df = writer(t)
        prod_df.writerow([current_date, total]) # skriver dato og totalt forbruk til csv fil 

    if total <= 0: # overskuddet går til huseier
        total = 0
    
    bill = round(el_price * total, 2) # regner ut kostnad for strøm
    with open('csvfiler/bill_total.csv', 'a') as b:
        bill_df = writer(b)
        bill_df.writerow([week_num, current_date, bill]) # skriver ukenummer, dato og kostnad til csv ifl
        
    el_bill_df = pd.read_csv('csvfiler/bill_total.csv', index_col='Week')
    return el_bill_df

def pay_consm():
    week_num = dt.datetime.now().isocalendar()[1]
    
    consumption_week = pd.read_csv('csvfiler/Electricety_consumption.csv', index_col='Week') # leser ukesforbruk fra csv-fil
    bill().to_csv('temp_csv/bill_temp.csv')
    
    with open('temp_csv/bill_temp.csv', 'a') as bt:
        bill_temp_df = writer(bt)
        bill_temp_df.writerow([week_num, '-', 0]) # skriver tomme kolonner inn i csv-fil
    
    pay_csv = pd.read_csv('temp_csv/bill_temp.csv', index_col='Week')
    pay = round(sum(pay_csv.at[week_num, 'Kr'])/6) # regner ut kostand per pers
    
    data1 = {'Key': bill_key, 'Value': pay, 'Token': token}

    p = requests.put('https://circusofthings.com/WriteValue', # sender kostnad per pers til CoT
             data = json.dumps(data1), 
             headers={'Content-Type': 'application/json'} )
    
    #consumption
    consumption_week.to_csv('temp_csv/El_consumption_temp.csv')
    
    with open('temp_csv/El_consumption_temp.csv', 'a') as  c: 
        consumption_df = writer(c)
        consumption_df.writerow([week_num, '-', 0]) # skriver tom csv fil
        
    cons_csv = pd.read_csv('temp_csv/El_consumption_temp.csv', index_col='Week')
    consumption_this_week = round(sum(cons_csv.at[week_num, 'kWh']), 2) # finner total forbruk for uka
    
    data2 = {'Key': consumption_key, 'Value': consumption_this_week, 'Token': token}

    c = requests.put('https://circusofthings.com/WriteValue', # sender totalt ukes forbruk til CoT
             data = json.dumps(data2), 
             headers={'Content-Type': 'application/json'} )
    ret = [pay, consumption_this_week]
    print('kost kjørt')
    print(ret)
    return ret