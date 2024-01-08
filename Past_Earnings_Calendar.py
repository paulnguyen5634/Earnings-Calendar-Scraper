from datetime import date, timedelta
import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
from selenium import webdriver
import time
from pprint import pprint
import os

def getSource(current_date):
    '''
    scrapes the NASDAQ earnings calender for earnings releases when given a date

    Args:
        current_date (datetime.date): The age of your son
 
    Returns:
        data (dict): dictionary format of the json data scraped 
    '''
    print("Earnings date is: ", current_date)

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
    '''
    When given a dictionary from the json file generated will sift though the data to append information pertaining to all tickers present 
    during that earnings day

    Args:
        source (dict): dictionary generated from getSource function
        dictionary (dict): dictionary of the dataframe format
        earningdate (datetime.date): date of when earnings is released
 
    Returns:
        dictionary (dict): dictionary with associated appended data from json 
    '''
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

def getDirList():
    '''
    Goes into the working directory and returns a list of strings containing the names of all files in the directory

    Args:
 
    Returns:
        dir_list (list): list of all files present in current working directory 
    '''
    # Get the list of all files and directories
    path = os.getcwd()
    dir_list = os.listdir(path)

    return dir_list

def saveData(csvFile, dir_list, dictionary):
    '''
    Checks to see if the csv for prior earnings tickers exists, if it does add new rows, if it doesnt make new csv from Dataframe

    Args:
        csvFile (str): string name of the csv located in directory or desired save name
        dir_list (list): list of all files present in current working directory 
        dictionary (dict): dictionary containing the appended data from siftSource function

    Returns: 
    '''
    if csvFile in dir_list: 
        # If it is there, read the data in
        df = pd.read_csv(csvFile)

        # Make another DF from scraped data
        df_new = pd.DataFrame.from_dict(dictionary)

        # Concatenate two dataframes and drop duplicates
        concatenated_df = pd.concat([df, df_new], axis=0)
        result_df = concatenated_df.drop_duplicates(subset=['Symbol', 'Date'], keep='first')

        print('Dataframes Concatenated!')
        print(result_df)
        print('Data has been saved!')
        result_df.to_csv("Earnings Calender above 500 Mil Mrkt Cap.csv")
        
    else:
        # If it aint there
        '''
        Save the dictionary as a new dataframe and create new csv file from that
        '''
        df = pd.DataFrame.from_dict(dictionary)
        df.to_csv("Earnings Calender above 500 Mil Mrkt Cap.csv")
        print('Data has been saved!')

    return

def main():

    # Returns the current local date
    today = date.today()
    lookBackPeriod = 30
    start_date = today - timedelta(days=lookBackPeriod)
    dictionary = {
        'Date': [],
        'Symbol': [],
        'Release': [],
        'MarketCap': [],
    }
    csvFile = 'Earnings Calender above 500 Mil Mrkt Cap'

    for n in range((today - start_date).days + 1):
        earningsdate = start_date + timedelta(days=n)
        print(type(earningsdate))
        source = getSource(earningsdate)
        dict_ = siftSource(source, dictionary, earningsdate)

    dir_list = getDirList()
    saveData(csvFile, dir_list, dict_)
    return

if __name__ == '__main__':
    main()