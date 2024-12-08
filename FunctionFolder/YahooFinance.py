import yfinance as yf
import pandas as pd
import os
import csv
import requests
import json
from pandas_datareader import data as pdr

from FunctionFolder.UserConfig import *



def YahooFinanceHistData(symbol, startDate, endDate):

    API_ENDPOINT = main_url+"/account/json-yahoo-hist-api1/"
    
    yf.pdr_override() # <== that's all it takes :-)

    OpenItem = []
    Item1 = []
    Item2 = []
    Item3 = []
    Item4 = []
    Item5 = []
    Item6 = []
    Item7 = []
    OpenSectionDic = {}

    # download dataframe
    alv_daat = pdr.get_data_yahoo(symbol, start=startDate, end=endDate)
    print("dataP", alv_daat)

    for i, j in alv_daat['Open'].items():
        OpenSectionDic['Date']=i.strftime('%Y-%m-%d')
        OpenSectionDic['Open']=j
        if OpenSectionDic != "":
            OpenItem.append(OpenSectionDic)
            OpenSectionDic={}

    for i, j in alv_daat['High'].items():
        for m in OpenItem:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=j
                if OpenSectionDic != "":
                    Item1.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Low'].items():
        for m in Item1:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=j
                if OpenSectionDic != "":
                    Item2.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Close'].items():
        for m in Item2:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=j
                if OpenSectionDic != "":
                    Item3.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Adj Close'].items():
        for m in Item3:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=m['Close']
                OpenSectionDic['Adj Close']=j
                if OpenSectionDic != "":
                    Item4.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Volume'].items():
        for m in Item4:
            if m['Date'] == i.strftime('%Y-%m-%d'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=m['Low']
                OpenSectionDic['Close']=m['Close']
                OpenSectionDic['Adj Close']=m['Adj Close']
                OpenSectionDic['Volume']=j
                if OpenSectionDic != "":
                    Item5.append(OpenSectionDic)
                    OpenSectionDic={}

    
    data={
        'symbol': symbol,
        'datalist': Item5,
    }
    r = requests.post(url=API_ENDPOINT, json=data)
    print("75",  r.text)




def YFHistData(symbol):
    if type(symbol) is str:
        symbol1=symbol
        now_utc = datetime.utcnow()
        currenttimedate = datetime.strftime(now_utc, '%Y-%m-%d')
        try:
            yfinance_file_check = requests.get(url=main_url+f'/media/upload_file/yahoo_finance_hist/{symbol1}.json')
            array_data = yfinance_file_check.json()['data']
                    
            startDate=array_data[len(array_data)-1]['Date']
            YahooFinanceHistData(symbol, startDate, currenttimedate)
        except:
            yfinance_configure = requests.get(url=main_url+'/media/upload_file/investing/json/yahoo_finance_configure.json')
            startDate = yfinance_configure.json()['data'][0]['BeginDate']  
            YahooFinanceHistData(symbol, startDate, currenttimedate)

    if type(symbol) is list:
        for m in symbol:
            symbol1=m
            now_utc = datetime.utcnow()
            currenttimedate = datetime.strftime(now_utc, '%Y-%m-%d')
            try:
                yfinance_file_check = requests.get(url=main_url+f'/media/upload_file/yahoo_finance_hist/{symbol1}.json')
                array_data = yfinance_file_check.json()['data']
                        
                startDate=array_data[len(array_data)-1]['Date']
                YahooFinanceHistData(symbol, startDate, currenttimedate)
            except:
                yfinance_configure = requests.get(url=main_url+'/media/upload_file/investing/json/yahoo_finance_configure.json')
                startDate = yfinance_configure.json()['data'][0]['BeginDate']  
                YahooFinanceHistData(symbol, startDate, currenttimedate)
            
        
def YFHistData1(symbol):
    if type(symbol) is str:
        API_ENDPOINT = main_url+"/account/json-yahoo-hist-api/"
        OpenItem = []
        Item1 = []
        Item2 = []
        Item3 = []
        Item4 = []
        Item5 = []
        Item6 = []
        Item7 = []
        OpenSectionDic = {}
        

        alv = yf.Ticker(symbol)

        alv_daat = alv.history(period="5y")

    
        for i, j in alv_daat['Open'].items():
            OpenSectionDic['Date']=i.strftime('%Y-%m-%d')
            OpenSectionDic['Open']=j
            if OpenSectionDic != "":
                OpenItem.append(OpenSectionDic)
                OpenSectionDic={}

        for i, j in alv_daat['High'].items():
            for m in OpenItem:
                if m['Date'] == i.strftime('%Y-%m-%d'):
                    OpenSectionDic['Date']=m['Date']
                    OpenSectionDic['Open']=m['Open']
                    OpenSectionDic['High']=j
                    if OpenSectionDic != "":
                        Item1.append(OpenSectionDic)
                        OpenSectionDic={}

        for i, j in alv_daat['Low'].items():
            for m in Item1:
                if m['Date'] == i.strftime('%Y-%m-%d'):
                    OpenSectionDic['Date']=m['Date']
                    OpenSectionDic['Open']=m['Open']
                    OpenSectionDic['High']=m['High']
                    OpenSectionDic['Low']=j
                    if OpenSectionDic != "":
                        Item2.append(OpenSectionDic)
                        OpenSectionDic={}

        for i, j in alv_daat['Close'].items():
            for m in Item2:
                if m['Date'] == i.strftime('%Y-%m-%d'):
                    OpenSectionDic['Date']=m['Date']
                    OpenSectionDic['Open']=m['Open']
                    OpenSectionDic['High']=m['High']
                    OpenSectionDic['Low']=m['Low']
                    OpenSectionDic['Close']=j
                    if OpenSectionDic != "":
                        Item3.append(OpenSectionDic)
                        OpenSectionDic={}

        for i, j in alv_daat['Volume'].items():
            for m in Item3:
                if m['Date'] == i.strftime('%Y-%m-%d'):
                    OpenSectionDic['Date']=m['Date']
                    OpenSectionDic['Open']=m['Open']
                    OpenSectionDic['High']=m['High']
                    OpenSectionDic['Low']=m['Low']
                    OpenSectionDic['Close']=m['Close']
                    OpenSectionDic['Volume']=j
                    if OpenSectionDic != "":
                        Item4.append(OpenSectionDic)
                        OpenSectionDic={}

        for i, j in alv_daat['Dividends'].items():
            for m in Item4:
                if m['Date'] == i.strftime('%Y-%m-%d'):
                    OpenSectionDic['Date']=m['Date']
                    OpenSectionDic['Open']=m['Open']
                    OpenSectionDic['High']=m['High']
                    OpenSectionDic['Low']=m['Low']
                    OpenSectionDic['Close']=m['Close']
                    OpenSectionDic['Volume']=m['Volume']
                    OpenSectionDic['Dividends']=j
                    if OpenSectionDic != "":
                        Item5.append(OpenSectionDic)
                        OpenSectionDic={}

        for i, j in alv_daat['Stock Splits'].items():
            for m in Item5:
                if m['Date'] == i.strftime('%Y-%m-%d'):
                    OpenSectionDic['Date']=m['Date']
                    OpenSectionDic['Open']=m['Open']
                    OpenSectionDic['High']=m['High']
                    OpenSectionDic['Low']=m['Low']
                    OpenSectionDic['Close']=m['Close']
                    OpenSectionDic['Volume']=m['Volume']
                    OpenSectionDic['Dividends']=m['Dividends']
                    OpenSectionDic['Stock Splits']=j
                    if OpenSectionDic != "":
                        Item6.append(OpenSectionDic)
                        OpenSectionDic={}


        data={
            'symbol': symbol,
            'datalist': Item6,
        }
        r = requests.post(url=API_ENDPOINT, json=data)
        print("75", r.text)
        return "Yahoo Finance Hist Data Successfully created"

    if type(symbol) is list:
        for m in symbol:
            API_ENDPOINT = main_url+"/account/json-yahoo-hist-api/"
            OpenItem = []
            Item1 = []
            Item2 = []
            Item3 = []
            Item4 = []
            Item5 = []
            Item6 = []
            Item7 = []
            OpenSectionDic = {}
            

            alv = yf.Ticker(symbol)

            alv_daat = alv.history(period="5y")

        
            for i, j in alv_daat['Open'].items():
                OpenSectionDic['Date']=i.strftime('%Y-%m-%d')
                OpenSectionDic['Open']=j
                if OpenSectionDic != "":
                    OpenItem.append(OpenSectionDic)
                    OpenSectionDic={}

            for i, j in alv_daat['High'].items():
                for m in OpenItem:
                    if m['Date'] == i.strftime('%Y-%m-%d'):
                        OpenSectionDic['Date']=m['Date']
                        OpenSectionDic['Open']=m['Open']
                        OpenSectionDic['High']=j
                        if OpenSectionDic != "":
                            Item1.append(OpenSectionDic)
                            OpenSectionDic={}

            for i, j in alv_daat['Low'].items():
                for m in Item1:
                    if m['Date'] == i.strftime('%Y-%m-%d'):
                        OpenSectionDic['Date']=m['Date']
                        OpenSectionDic['Open']=m['Open']
                        OpenSectionDic['High']=m['High']
                        OpenSectionDic['Low']=j
                        if OpenSectionDic != "":
                            Item2.append(OpenSectionDic)
                            OpenSectionDic={}

            for i, j in alv_daat['Close'].items():
                for m in Item2:
                    if m['Date'] == i.strftime('%Y-%m-%d'):
                        OpenSectionDic['Date']=m['Date']
                        OpenSectionDic['Open']=m['Open']
                        OpenSectionDic['High']=m['High']
                        OpenSectionDic['Low']=m['Low']
                        OpenSectionDic['Close']=j
                        if OpenSectionDic != "":
                            Item3.append(OpenSectionDic)
                            OpenSectionDic={}

            for i, j in alv_daat['Volume'].items():
                for m in Item3:
                    if m['Date'] == i.strftime('%Y-%m-%d'):
                        OpenSectionDic['Date']=m['Date']
                        OpenSectionDic['Open']=m['Open']
                        OpenSectionDic['High']=m['High']
                        OpenSectionDic['Low']=m['Low']
                        OpenSectionDic['Close']=m['Close']
                        OpenSectionDic['Volume']=j
                        if OpenSectionDic != "":
                            Item4.append(OpenSectionDic)
                            OpenSectionDic={}

            for i, j in alv_daat['Dividends'].items():
                for m in Item4:
                    if m['Date'] == i.strftime('%Y-%m-%d'):
                        OpenSectionDic['Date']=m['Date']
                        OpenSectionDic['Open']=m['Open']
                        OpenSectionDic['High']=m['High']
                        OpenSectionDic['Low']=m['Low']
                        OpenSectionDic['Close']=m['Close']
                        OpenSectionDic['Volume']=m['Volume']
                        OpenSectionDic['Dividends']=j
                        if OpenSectionDic != "":
                            Item5.append(OpenSectionDic)
                            OpenSectionDic={}

            for i, j in alv_daat['Stock Splits'].items():
                for m in Item5:
                    if m['Date'] == i.strftime('%Y-%m-%d'):
                        OpenSectionDic['Date']=m['Date']
                        OpenSectionDic['Open']=m['Open']
                        OpenSectionDic['High']=m['High']
                        OpenSectionDic['Low']=m['Low']
                        OpenSectionDic['Close']=m['Close']
                        OpenSectionDic['Volume']=m['Volume']
                        OpenSectionDic['Dividends']=m['Dividends']
                        OpenSectionDic['Stock Splits']=j
                        if OpenSectionDic != "":
                            Item6.append(OpenSectionDic)
                            OpenSectionDic={}


            data={
                'symbol': symbol,
                'datalist': Item6,
            }
            r = requests.post(url=API_ENDPOINT, json=data)
            print("75", r.text)
        return "Yahoo Finance Hist Data Successfully created"
        
        

def YFInfoData(symbol):
    
    if type(symbol) is str:
        API_ENDPOINT = main_url+"/account/json-yahoo-api/"
        lazr = yf.Ticker(symbol)
        data = {
            'symbol': symbol,
            'datalist': lazr.info,
        }

        r = requests.post(url=API_ENDPOINT, json=data)
        print("75", r.text)
        return "Yahoo Finance Info Data Successfully created"

    if type(symbol) is list:
        API_ENDPOINT = main_url+"/account/json-yahoo-api/"
        for m in symbol:
            lazr = yf.Ticker(m)
            data = {
                'symbol': m,
                'datalist': lazr.info,
            }

            r = requests.post(url=API_ENDPOINT, json=data)
            print("75", r.text)    

        return "Yahoo Finance Info Data Successfully created"
    



        


        