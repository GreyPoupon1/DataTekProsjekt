# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 13:47:54 2021

@author: krist
"""

from yr.libyr import Yr
import pandas as pd
import requests
import json

def get_weather():
    weather_df = Yr(location_name='Norge/Trøndelag/Trondheim/Trondheim')
    now_df = weather_df.now() # henter værdata fra Yr
    temp_val = int(pd.DataFrame(now_df)['temperature']['@value']) # finner luft temeperaturen
    wind_val = float(pd.DataFrame(now_df)['windSpeed']['@mps']) # finner vindfart
#    wind_dir = float(pd.DataFrame(now_df)['windDirection']['@deg'])
    precipitation_val = float(pd.DataFrame(now_df)['precipitation']['@value']) # finner regn
#Sends temp, windspeed and precipitation to CoT

    token = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NzUxIn0.DeRcDo1IRe0fFV_IEw8WyUbEd02hwzWikjARXvc2oEE'
    
    temp_key = '12583'
    temp_data = {'Key': temp_key, 'Value': temp_val, 'Token': token} # sender lufttemp til CoT
    t_put = requests.put('https://circusofthings.com/WriteValue', 
             data = json.dumps(temp_data), 
             headers={'Content-Type': 'application/json'})
    
    wind_key = '8760'
    wind_data = {'Key': wind_key, 'Value': wind_val, 'Token': token} # sender vindfart til CoT
    w_put = requests.put('https://circusofthings.com/WriteValue', 
             data = json.dumps(wind_data), 
             headers={'Content-Type': 'application/json'})
    
    precipitation_key = '6464'
    precipitation_data = {'Key': precipitation_key, 'Value': precipitation_val, 'Token': token} # sender regn til CoT
    p_put = requests.put('https://circusofthings.com/WriteValue', 
             data = json.dumps(precipitation_data), 
             headers={'Content-Type': 'application/json'})
#sende data til cot