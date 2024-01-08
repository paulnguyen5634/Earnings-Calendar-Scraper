import pandas as pd # library for data analysis
import numpy as np
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
from selenium import webdriver
import time
from pprint import pprint
# Import date class from datetime module
from datetime import date

def getSource():

    # Returns the current local date
    today = date.today()
    print("Today date is: ", today)

    year = today.year

    month = today.month
    if month < 10:
        month = str(month)
        month = ''.join(('0',month))
        
    day = today.day
    if day < 10:
        day = str(day)
        day = ''.join(('0',day))

    headers = {
        "Accept":"application/json, text/plain, */*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"en-US,en;q=0.9",
        "Origin":"https://www.nasdaq.com",
        "Referer":"https://www.nasdaq.com",
        "User-Agent":"your user agent..."
    }
 
    url = 'https://api.nasdaq.com/api/calendar/earnings?' 
    #Change this according to day
    payload = {"date":f"{year}-{month}-{day}"} 
    source = requests.get( url=url, headers=headers, params=payload, verify=True ) 
    data = source.json()

    return data

def main():
    '''
    Scrapes the NASDAQ earnings calender for earnings releases coming TODAY. 
    Will return blank when run on holidays/weekends
    '''
    
    data = getSource()
    print(data)

    try:
        for i in range(0,len(data['data']['rows'])):
        
            mrkt_cap = data['data']['rows'][i]['marketCap']
            mrkt_cap = mrkt_cap.replace('$', '')
            mrkt_cap = mrkt_cap.replace(',', '')
            
            forecastEPS = data['data']['rows'][i]['epsForecast']
            
            numAnalysts = data['data']['rows'][i]['noOfEsts']
            
            releaseTime = data['data']['rows'][i]['time'] 
            
            #Only showing companies with abova 1billion$ mrktCap
            if int(mrkt_cap)/100000000 > 1 and releaseTime == 'time-pre-market':
                print(data['data']['rows'][i]['symbol'])
                print(releaseTime)
                print(data['data']['rows'][i]['marketCap'])
                print('Forcasted EPS: '+forecastEPS)
                print('Num analysts: ' + numAnalysts + "\n")
    except TypeError:
        print('No Earnings Released Today')

    return

if __name__ == '__main__':
    main()