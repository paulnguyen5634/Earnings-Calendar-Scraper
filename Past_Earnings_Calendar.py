from datetime import date, timedelta
import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
from selenium import webdriver
import time
from pprint import pprint

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

def siftData(source):

    try:
        for i in range(0,len(source['data']['rows'])):
            earningsdate = current_date
            symbol = source['data']['rows'][i]['symbol']
            mrktCap = source['data']['rows'][i]['marketCap']

            # continue if stock has '.' in the string
            if '.' in symbol:
                continue

            mrkt_cap = source['data']['rows'][i]['marketCap']
            mrkt_cap = mrkt_cap.replace('$', '')
            mrkt_cap = mrkt_cap.replace(',', '')
            
            forecastEPS = source['data']['rows'][i]['epsForecast']
            
            numAnalysts = source['data']['rows'][i]['noOfEsts']
            
            releaseTime = source['data']['rows'][i]['time'] 
    except:
        print('No Earnings today')

    return

def main():

    

    return

if __name__ == '__main__':
    main()