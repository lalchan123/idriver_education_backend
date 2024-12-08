

# import required libraries
import numpy as np
import yfinance as yf
import requests
from numpy.linalg import norm
import os, json
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt
from scipy.spatial.distance import hamming, cdist, pdist
from fuzzywuzzy import fuzz
import jaro

from FunctionFolder.UserConfig import *


def JsonYahooHistDataListWrite(symbol, DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/{symbol}.json'

    if os.path.isfile(fileName):
        f = open(fileName, 'wb')
        jsonformat = {
            "data": DataList
        }
        json_object = json.dumps(jsonformat, indent=4)
        with open(fileName, "w") as outfile:
            outfile.write(json_object)


def ABC():
    OpenItem = []
    Item1 = []
    Item2 = []
    Item3 = []
    Item4 = []
    Item5 = []
    Item6 = []
    Item7 = []
    OpenSectionDic = {}

    TickerSymbol = 'SPY'
    alv_daat = yf.download(tickers=TickerSymbol, period='1d', interval='5m')

    for i, j in alv_daat['Open'].items():
        OpenSectionDic['Date']=i.strftime('%Y-%m-%d %H:%M:%S')
        OpenSectionDic['Open']=j
        if OpenSectionDic != "":
            OpenItem.append(OpenSectionDic)
            OpenSectionDic={}

    for i, j in alv_daat['High'].items():
        for m in OpenItem:
            if m['Date'] == i.strftime('%Y-%m-%d %H:%M:%S'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=j
                if OpenSectionDic != "":
                    Item1.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Low'].items():
        for m in Item1:
            if m['Date'] == i.strftime('%Y-%m-%d %H:%M:%S'):
                OpenSectionDic['Date']=m['Date']
                OpenSectionDic['Open']=m['Open']
                OpenSectionDic['High']=m['High']
                OpenSectionDic['Low']=j
                if OpenSectionDic != "":
                    Item2.append(OpenSectionDic)
                    OpenSectionDic={}

    for i, j in alv_daat['Close'].items():
        for m in Item2:
            if m['Date'] == i.strftime('%Y-%m-%d %H:%M:%S'):
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
            if m['Date'] == i.strftime('%Y-%m-%d %H:%M:%S'):
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
            if m['Date'] == i.strftime('%Y-%m-%d %H:%M:%S'):
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


 
    JsonYahooHistDataListWrite('input', Item5)



# Cosine Similarity
def CosineSimilarity():
    try:
        ABC()  
        path_url = main_media_url+f'/media/upload_file/investing/json/SPY.json'
        input_path_url = main_media_url+f'/media/upload_file/investing/json/input.json'
        if os.path.isfile(path_url) and os.path.isfile(input_path_url):
            f = open(path_url)
            data1 = json.load(f)
            data = data1['data']

            f1 = open(input_path_url)
            data2 = json.load(f1)
            data_input = data2['data']

            input_data_count = len(data_input)
            print("input_data_count", input_data_count)
            df = pd.DataFrame(data)
            input_df= pd.DataFrame(data_input)
            input_df['Close']= round(input_df['Close'], 3)

            df['diff'] = df['Open']-df['Close']
            input_df['diff'] = round(input_df['Open']-input_df['Close'], 2)
            df['Date2'] = df['Date'].str[:10]

            DataList = []
            DataItem1 = []
        
            df.sort_values('Date')
            df2 = df.Date2.unique()

            for date in df2:
                df3Date = round(df[df['Date2'] == date], 2)
                DataList.append(list(df3Date['diff']))
            

            # print("DataList", DataList)
        
            AData = [sublist[:input_data_count] for sublist in DataList]
            BData = list(input_df['diff'])

            A = np.array(AData)
            B = np.array(input_df['diff'])

            # compute cosine similarity
            cosine = np.dot(A, B)/(norm(A, axis=1)*norm(B))
            CosineZipData = list(zip(df2, np.round(cosine, 3)))


            Dic = {}
            Date=''
            max=0
            for k, l in CosineZipData:
                if max < l:
                    max = l
                    Date = k

            Dic[Date] = max
            
            FuzzList = []
            for km in AData:
                FuzzList.append(fuzz.ratio(km, BData))
            FuzzZipData = list(zip(df2, FuzzList))

            DicF = {}
            DateF=''
            maxF=0
            for k1, l1 in FuzzZipData:
                if maxF < l1:
                    maxF = l1
                    DateF = k1

            DicF[DateF] = maxF

            df3 = df[df['Date2']==Date]
            df3['Close'] = df3['Close']+round(input_df.iloc[0]['Close']-df3.iloc[0]['Close'], 3)
            df3['Close'] = round(df3['Close'], 3)

           
            df4 = df[df['Date2']==DateF]
            df4['Close'] = df4['Close']+round(input_df.iloc[0]['Close']-df4.iloc[0]['Close'], 3)
            df4['Close'] = round(df4['Close'], 3)


            csv_df = pd.DataFrame({})

            csv_df1 = pd.DataFrame({})
            csv_df1["Date"] = '2024-06-10 '+df3['Date'].str[11:]
            csv_df1["Close"] = df3['Close']
            csv_df1["Type"] = 'Cosine Data'
            csv_df = pd.concat([csv_df, csv_df1], ignore_index=True)

            csv_df2 = pd.DataFrame({})
            csv_df2["Date"] = '2024-06-10 '+df4['Date'].str[11:]
            csv_df2["Close"] = df4['Close']
            csv_df2["Type"] = 'Fuzzy Data'
            csv_df = pd.concat([csv_df, csv_df2], ignore_index=True)


            csv_df3 = pd.DataFrame({})
            csv_df3["Date"] = '2024-06-10 '+input_df['Date'].str[11:]
            csv_df3["Close"] = input_df['Close']
            csv_df3["Type"] = 'Input Data'
            csv_df = pd.concat([csv_df, csv_df3], ignore_index=False)

            # csv_df['sorted_date'] = pd.to_datetime(df['Date'], dayfirst=True)

            csv_df.sort_values(by='Date', inplace=True)

            csv_df.to_csv(main_media_url+f'/media/upload_file/investing/csv/Cosine.csv', index=False)


        
            # print("df4", df4.to_dict(orient='records'))
            # print("input_df.iloc[0]['Close']-df3.iloc[0]['Close']", round(input_df.iloc[0]['Close']-df3.iloc[0]['Close']))
            # plt.figure(figsize=(15, 5))
            # plt.plot(df3['Date'].str[11:], df3['Close']+round(input_df.iloc[0]['Close']-df3.iloc[0]['Close']),  label=f"Cosine Similarity {[max]} {df3.Date.str[:10].unique()}")
            # plt.plot(df4['Date'].str[11:], df4['Close']+round(input_df.iloc[0]['Close']-df4.iloc[0]['Close']),  label=f"Fuzzy Similarity {[maxF]} % {df4.Date.str[:10].unique()}")
            # plt.plot(input_df['Date'].str[11:], input_df['Close'],  label=f"Today {input_df.Date.str[:10].unique()}")
            # plt.xticks(fontsize = 5)
            # plt.yticks(fontsize = 5)
            # plt.title("Cosine Fuzzy similarity")
            # plt.xlabel("Date")
            # plt.ylabel("Close")
            # plt.legend()
            # plt.grid(True)
            # plt.show()
            return True, f"success", df3.to_dict(orient='records'), df4.to_dict(orient='records'), input_df.to_dict(orient='records'), Dic, DicF

    except Exception as error:
        return False, f"Something error or Cosine Similarity Problem or {error}", [], [], [], {}, {}

   