from datetime import date, timedelta
import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
from selenium import webdriver
import time
from pprint import pprint

def getSource():

    return

def main():

    # Get the current date
    today = date.today()

    # Calculate the date 30 days ago
    start_date = today - timedelta(days=30)

    dict_ = {
        'Symbol': [],
        'Release': [],
        'Date': [],
        'MarketCap': [],
    }

    return

if __name__ == '__main__':
    main()