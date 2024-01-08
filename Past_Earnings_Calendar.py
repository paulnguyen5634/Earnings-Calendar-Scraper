from datetime import date, timedelta
import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
from selenium import webdriver
import time
from pprint import pprint

def getSource(current_date):
    print("Today date is: ", current_date)

    year = current_date.year

    month = current_date.month
    if month < 10:
        month = str(month)
        month = ''.join(('0',month))
        
    day = current_date.day
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

    # As to prevent overbearing the website and getting throttled
    time.sleep(.25)

    return data

def siftSource(source, dictionary, earningsdate):
    try:
        for i in range(0,len(source['data']['rows'])):
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

            try:
                if int(mrkt_cap) > 500000000:
                    dictionary['Date'].append(earningsdate)
                    dictionary['Release'].append(releaseTime)
                    dictionary['Symbol'].append(symbol)
                    dictionary['MarketCap'].append(mrktCap)
            except ValueError:
                print("No Supplied Market Cap") 
                continue 

    except TypeError:
        print('No Earnings today')

    return dictionary

def main():

    # Returns the current local date
    today = date.today()
    lookBackPeriod = 30
    start_date = today - timedelta(days=lookBackPeriod)
    dict_ = {
        'Symbol': [],
        'Release': [],
        'Date': [],
        'MarketCap': [],
    }

    for n in range((today - start_date).days + 1):
        earningsdate = start_date + timedelta(days=n)
        source = getSource(earningsdate)
        dict_ = siftSource(source, dict_, earningsdate)

    return

if __name__ == '__main__':
    main()