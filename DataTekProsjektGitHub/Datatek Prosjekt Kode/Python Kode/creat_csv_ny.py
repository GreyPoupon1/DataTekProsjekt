# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 18:51:40 2021

@author: krist
"""
# Denne kjøres kun en gang for å opprette csv_filer som de andre kodene skriver til
import pandas as pd

# Definerer dataframes ved hjelp av pandas
prod_d_df = pd.DataFrame(data={'Week': [], 'Date': [], 'kWh': []})
prod_W_df = pd.DataFrame(data={'Week': [], 'kWh': []})
consum_df = pd.DataFrame(data={'Week': [], 'Date': [], 'kWh': []})
bill_df = pd.DataFrame(data={'Week': [], 'Date': [], 'Kr': []})
tot_df = pd.DataFrame(data={'Date': [], 'kWh': []})
til_plot_df = pd.DataFrame(data={'Date': [], "Time": [], "Temp": [], "kWh": []})

# lagrer csv-fila
prod_d_df.to_csv('csvfiler/Panel_production_day.csv', index=False)
prod_W_df.to_csv('csvfiler/Panel_production_week.csv', index=False)
consum_df.to_csv('csvfiler/Electricety_consumption.csv', index=False)
bill_df.to_csv('csvfiler/bill_total.csv', index=False)
tot_df.to_csv('csvfiler/total_consumption.csv', index=False)
til_plot_df.to_csv("csvfiler/to_plot.csv",sep=";",index=False)