# web scrapping api
import json
import os
import pandas as pd
import csv
import numpy as np
import time
import datetime
from datetime import datetime
import schedule
import requests

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response

from accountapp.DynamicFunction.SentimentAnalyzer import *



def InvestingCalderJsonWrite(DataList):
    fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/csv/investingCalender.csv'
    if os.path.isfile(fileName):
        
        with open(fileName, 'r', encoding='utf-8') as file:
       
            csvreader = csv.DictReader(file)
            df = pd.DataFrame(list(csvreader))
           
            if len(df)==0:
                DataList.to_csv(r'/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/csv/investingCalender.csv', index=False)
            if len(df)!=0:

                filterData = DataList[(DataList['date'].isin(df['date'])) & (DataList['event'].isin(df['event']))]
                filterDataNotEqual = DataList[(~DataList['date'].isin(df['date'])) & (~DataList['event'].isin(df['event']))]

                if len(filterData)!=0:
                    df.update(filterData)
                    df.to_csv(r'/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/csv/investingCalender.csv', index=False)
                
                if len(filterDataNotEqual)!=0:
                    df3 = df._append(filterDataNotEqual)
                    df3.to_csv(r'/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/csv/investingCalender.csv', index=False)
                    


    else:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'File not found'}, status=status.HTTP_400_BAD_REQUEST)    
    



        
def InvestingReutersJsonWrite(DataList):
    fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/investing/json/investing_reuters_data.json'
    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']
        for index, row in DataList.iterrows():
            if [x for x in news_array_data if x['NewsTitle'] == row['NewsTitle']] and [
                x for x in news_array_data if x['time'] == row['time']] and [
                x for x in news_array_data if x['url'] == row['url']]:
                return
            else:
                category, sentiment, most_frequent_word, summary = SentimentAnalyzerFunction(row['NewsTitle'])
                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "time": row['time'],
                    "NewsTitle": row['NewsTitle'],
                    "url": row['url'],
                    "categories": category,
                    "sentiment": sentiment,
                    "most_frequent_word": most_frequent_word,
                    "summary": summary,
                }

                write_json(y)


    else:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'File not found'}, status=status.HTTP_400_BAD_REQUEST)



