# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 17:53:32 2021

@author: krist
"""
from yr.libyr import Yr
import pandas as pd
import requests
import json # importerer biblioteker
from csv import writer
import datetime as dt

# Usage kitchen: oven, micro, fridge, heat, other (light etc.)
# Usage livingroom: heat, tv (if in use??), other (light etc.)
# Usage bathroom: heat, shower, Washing machine, other (light etc.)
# Usage bedroom(X6): heat (home, away, night), other (light etc.)

#https://www.siliconvalleypower.com/residents/save-energy/appliance-energy-use-chart
#https://www.fjordkraft.no/strom/stromforbruk/elektriske-apparater/
# energy consumption in based on energy labeling on products with klass A or A+ for the products that haveenergy labeling
#kitchen
oven = 1 #kWh pr time used
fridge = 0.82 #kWh pr day
micro_oven = 0.4 #kWh pr day. 800W fore 30min every day
dishwasher = 0.64 #kWh pr day (241kWh pr year)
#bath room
Water_heater = 8 #kWh pr day
washing_machine = 0.5 #kWh  pr time used
#livingroom
tv = 1.5 #Wh per minute of use
#the house
room_heating = 0.35 #kWh/(C*day). based on annual consumtion of 2190kWh. Average temp in trondheim 8 C and average room temp 22 C (panel oven) 
other = 6 #kWh pr day (lighting, charging, pc etc.)

tv_key = '22181'
token = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MTc3In0.G9gRducsNPjd8I01Pn6tmKB6hDr8MOXLr_t9cWYNwYY' # info til CoT

def heating_house(): #assume 2 panel ovens (Living room and hallway)
    weather_df = Yr(location_name='Norge/Trøndelag/Trondheim/Trondheim')
    now_df = weather_df.now()
    date = dt.datetime.now().strftime('%d-%m-%y') # henter vær og dato
    temp_df = pd.read_csv('temp_csv/Heating_Room.csv', index_col='Date').at[date, 'Temp'] # henter temperatur
    temp_val = sum(temp_df)/len(temp_df)
    temp_val = int(pd.DataFrame(now_df)['temperature']['@value']) # finner lufttemperatur som heltall
    
    if temp_val < 22: # finner ut hvor mye energi som brukes til oppvarming
        energy_house = (room_heating * (22 - temp_val))*2
    else:
        energy_house = 0
    if temp_val < 28:
       energy_bath = (room_heating * (28 - temp_val))
    else:
        energy_bath = 0
    return [energy_house, energy_bath]

def tv_use(): # resett value når dagen er fredig
   r = requests.get('https://circusofthings.com/ReadValue', params=  # henter tv-verdien fra CoT
                 {'Key': tv_key, 'Token':token})

   tv_time = json.loads(r.content)['Value']
   tv_consumption = tv * tv_time / 1000 # regner ut tv-en sitt strømforbruk i kWh
   
   data = {'Key': tv_key, 'Value': 0, 'Token': token}

   p = requests.put('https://circusofthings.com/WriteValue', # resetter verdien som sier om tv-en er i bruk eller ikke
             data = json.dumps(data), 
             headers={'Content-Type': 'application/json'} )
    
   return tv_consumption

# kjøres en gang pr dag
def energy_use():
    day = dt.datetime.now().isoweekday()
    date = dt.datetime.now().strftime('%d-%m-%y') # henter dato og uke og dag
    week_num = dt.datetime.now().isocalendar()[1]
    
    bedroom = pd.read_csv('temp_csv/Heating_Room.csv')['kWh']
    heating_bedroom=0
    for i in range(len(bedroom)):
        heating_bedroom += bedroom[i]
    
    total = 0
    total += heating_bedroom*6 # legger på strømforbruk fra ulike apparater til totalen
    # kitchen consumption
    total += fridge
    #bathroom consumption
    total += washing_machine * 3 # assume the washing mashine is used 3 times a day
    total += Water_heater #assume one shower pr person every day
    total += heating_house()[1] #hating bathroom
    #tv
    total += tv_use()
    #the house
    total += heating_house()[0] #heating livingroom and hallway
    total += other
    #monday to friday
    if day in range(1,6):
        # kitchen consumption
        total += oven*6 #assume the oven is used once a day per person to make dinner
        total += micro_oven
        total += dishwasher
    #saturday
    elif day == 6:
        # kitchen consumption
        total += oven*9 #oven is used per person to make dinner + half the house to make breakfast
        total += micro_oven*4 # microoven is used more on saturday
        total += dishwasher*1.5
    #sunday
    else:
        # kitchen consumption
        total += oven*12 #assume the oven is used to make dinner and breakfaste by all
        total += micro_oven
        total += dishwasher*1.5
       
    total = round(total, 2)
    with open('csvfiler/Electricety_consumption.csv', 'a') as el:
        consum_df = writer(el)
        consum_df.writerow([week_num, date, total]) #skriver ukenummer, totalt strømforbruk og dato til csv fil

    ec = pd.read_csv('csvfiler/Electricety_consumption.csv')
    print('forbruk')
    print(ec)
    return ec
#les ute temp legg på strøm når kaldere
#les hjemme status, hjemme mer strøm, + nat oppdater en verdi som rom kan lese av (reg tas av pi). 