# -*- coding: utf-8 -*-
"""
Created on Mon May  3 18:24:01 2021

@author: krist
"""
import pandas as pd
# runs every day av 23.59

def resett():
    room_df = pd.DataFrame(data={'Date': [], 'kWh': [], 'Temp': []})
    price_df = pd.DataFrame(data={'Date': [], 'kr/kWh': []}) # lager dataframes med kolonnenavn
    prod_h_df = pd.DataFrame(data={'Date': [], 'Time': [], 'kWh': []})
    bill_temp_df = pd.DataFrame(data={'Week': [], 'Date': [], 'Kr': []})
    consum_temp_df = pd.DataFrame(data={'Date': [], 'kWh': []})

    prod_h_df.to_csv('temp_csv/Panel_production_hour.csv', index=False)
    room_df.to_csv('temp_csv/Heating_Room.csv', index=False) # skriver dataframe til tomme csv filer uten index
    price_df.to_csv('temp_csv/avg_price_day.csv', index=False)
    bill_temp_df.to_csv('temp_csv/bill_temp.csv', index=False)
    consum_temp_df.to_csv('temp_csv/El_consumption_temp.csv', index=False)
#resett()