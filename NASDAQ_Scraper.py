import pandas as pd # library for data analysis
import numpy as np
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
from selenium import webdriver
import time
from pprint import pprint
# Import date class from datetime module
from datetime import date

def main():
    '''
    Scrapes the NASDAQ earnings calender for earnings releases coming TODAY. 
    Will not work on holidays/weekends
    '''
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

    return

if __name__ == '__main__':
    main()