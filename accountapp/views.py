from django.shortcuts import redirect, render

# web scrapping api
import json
import os, sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
from datetime import datetime
import schedule
import requests

import yfinance as yf

import shutil

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import *



from rest_framework.pagination import PageNumberPagination



# activation import library

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

#import model
from django.contrib.auth.models import User
from accountapp.models import *

from courseapp.models import *

#import serializer
from accountapp.serializer import *

#import helper 
from accountapp.helpers import *
from accountapp.PointerCalculationOne import *
from accountapp.twoPointer import *
from accountapp.twoPointerMinp import *
from accountapp.threePointer import *
from accountapp.threePointerLeftRight import *
from accountapp.fourPointerLeftRight import *
from accountapp.threePointerLeftRightDayBasis import *
from accountapp.threePointerMinp import *
from accountapp.threePointerd3 import *
from accountapp.threePointerd3Minp import *
from accountapp.MainPointerCalculation import *
from accountapp.cosine_similarity import *

# authentication functions
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout,get_user_model
from accountapp.Decorators import *

Usermodel = get_user_model()


gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
currenttimestamp = datetime.strptime(
                gm, "%a, %d %b %Y %X").timestamp()
currenttimedate = datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y')


# dynamic function import
from accountapp.DynamicFunction.Process_Log import *

from accountapp.DynamicFunction.WebScrappingJson import *
from accountapp.DynamicFunction.LinkedList import *
from accountapp.DynamicFunction.JsonSelect import *
from accountapp.DynamicFunction.SentimentAnalyzer import *

from accountapp.classbase import GlobalJson
from accountapp.apicoderun import ApiCodeRun


from accountapp.DynamicFunction.ValidatorF import *
from FunctionFolder.UserConfig import *


from media.upload_file.dynamic_rest.UIGETAPI1 import *
from media.upload_file.dynamic_rest.UIGETAPI2 import *
from media.upload_file.dynamic_rest.UIPOSTAPI import *
from media.upload_file.dynamic_rest.Custom import *
from media.upload_file.dynamic_rest.Custom2 import *
# from static.upload_folder.dynamic_rest.Custom import *

# global function
from FunctionFolder.WrapperFunc import *


def generate_unique_random_number():
    # Get the current time in seconds since the Epoch
    current_time = int(time.time() * 1000)  # Multiply by 1000 to include milliseconds
    
    # Generate a random number
    random_number = random.randint(0, 99999)
    
    # Combine the current time with the random number to ensure uniqueness
    unique_random_number = int(f"{current_time}{random_number}")
    
    return unique_random_number



# Create your views here.


def JsonWrite(subject, sender, date, body, currenttimedate):
    fileName = main_media_url+f'/media/upload_file/json/gmail_data_{currenttimedate}.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/json/gmail_data_{currenttimedate}.json', api_url=main_url+f'/media/upload_file/json/gmail_data_{currenttimedate}.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        email_array_data = data['gmail_data']

        if [x for x in email_array_data if x['subject'] == subject] and [
                x for x in email_array_data if x['date'] == date]:
            return

        else:
            print("68")

            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["gmail_data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            y = {
                "subject": subject,
                "sender": sender,
                "date": date,
                "body": body
            }

            write_json(y)
    else:
        f = open(fileName, 'wb')
        jsonformat = {
            "gmail_data": []
        }
        json_object = json.dumps(jsonformat, indent=4)
        with open(fileName, "w") as outfile:
            outfile.write(json_object)
        print("38 file is created")

def JsonConvertData(df):
    try:
        DataItem = []
        KeyItem = []
        sections={}
        for key, value in df.iteritems():
            KeyItem.append(key)

        for index, row in df.iterrows():

            for i in range(len(KeyItem)):
                sections[KeyItem[i]]= row[KeyItem[i]]
            if sections != "":
                DataItem.append(sections)
                sections={}

        return DataItem
    
    except Exception as err:
        print("err", err)        

def ExcelFileWrite(file_name, df):
    df_data = pd.read_excel(file_name)
    df_data = pd.concat([df_data, df], ignore_index=True)
    df_data.to_excel(file_name, index=False)        
        
def JsonNewsDataWrite(time, headline):
    fileName = main_media_url+f'/media/upload_file/json/news_data.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/json/news_data.json', api_url=main_url+f'/media/upload_file/json/news_data.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']

        if [x for x in news_array_data if x['time'] == time] and [
                x for x in news_array_data if x['headline'] == headline]:
            return

        else:
            print("68")

            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            y = {
                "time": time,
                "headline": headline,
            }

            write_json(y)        


# def JsonNewsDataListWrite(DataList):
#     fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/news_data.json'
#     if os.path.isfile(fileName):
#         f = open(fileName)
#         data = json.load(f)
#         news_array_data = data['news_data']

    
#         for i in DataList:
            
  
#             fileNewsTimestands = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/news_data_timestamp.json'
#             ftimestand = open(fileNewsTimestands)
#             datatimestand = json.load(ftimestand)
#             news_array_data_timestand = datatimestand['news_data_timestamp']
            
#             timestand1 = datetime.datetime.strptime(i['time'], "%d/%m/%Y %I:%M %p").timestamp()

#             if news_array_data_timestand:
               
#                 news_array_data_timestand1 = datetime.datetime.strptime(news_array_data_timestand[0]['time'], "%d/%m/%Y %I:%M %p").timestamp()
#                 presenttimestand1 = datetime.datetime.strptime(i['presenttimestand'], "%d/%m/%Y %I:%M %p").timestamp()
                


#                 if news_array_data_timestand1 == presenttimestand1:
#                     return 
#                 else:
#                     if news_array_data_timestand1<timestand1:
#                         datatimestand['news_data_timestamp'][0]['time'] = i['presenttimestand']
#                         with open('/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/news_data_timestamp.json', 'w') as f: 
#                             json.dump(datatimestand, f)
                        


#                         if [x for x in news_array_data if x['headline'] == i['headline']] and [
#                             x for x in news_array_data if x['time'] == i['time']] and [
#                             x for x in news_array_data if x['url'] == i['url']]:
#                             return

#                         else:
#                             def write_json1(new_data, filename=fileName):
#                                 with open(filename, 'r+') as file:
#                                     file_data = json.load(file)
#                                     file_data["news_data"].append(new_data)
#                                     file.seek(0)
#                                     json.dump(file_data, file, indent=4)
#                             y = {
#                                 "time": i['time'],
#                                 "headline": i['headline'],
#                                 "url": i['url'],
#                             }

#                             write_json1(y)

#             else:
#                 def write_json(new_data, filename=fileNewsTimestands):
#                         with open(filename, 'r+') as file:
#                             file_data = json.load(file)
#                             file_data["news_data_timestamp"].append(new_data)
#                             file.seek(0)
#                             json.dump(file_data, file, indent=4)
#                 y = {
#                     "time": i['presenttimestand'],
#                 }

#                 write_json(y)
                
                
                
def JsonNewsDataListWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/json/news_data.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/json/news_data.json', api_url=main_url+f'/media/upload_file/json/news_data.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']

    
        for i in DataList:
            if [x for x in news_array_data if x['headline'] == i['headline']] and [
                x for x in news_array_data if x['time'] == i['time']] and [
                x for x in news_array_data if x['url'] == i['url']]:
                return

            else:

                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "time": i['time'],
                    "headline": i['headline'],
                    "url": i['url'],
                }

                write_json(y)  
                
                
                
def JsonCNBCNewsDataListWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/cnbc_news_data.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/cnbc_news_data.json', api_url=main_url+f'/media/upload_file/investing/json/cnbc_news_data.json')
    gm = time.strftime("%a, %d %b %Y %X", time.gmtime())
    currenttimestamp = datetime.strptime(gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            news_array_data = data['data']

            # print("DataList", DataList)
        
            for i in DataList:
                if [x for x in news_array_data if x['headline'] == i['headline']] and [
                    x for x in news_array_data if x['url'] == i['url']]:
                    return

                else:
                    category, sentiment, most_frequent_word, summary = SentimentAnalyzerFunction(i['headline'])
                    
                    # def write_json(new_data, filename=fileName):
                    #     with open(filename, 'r+') as file:
                    #         file_data = json.load(file)
                    #         file_data["data"].append(new_data)
                    #         file.seek(0)
                    #         json.dump(file_data, file, indent=4)
                    new_data = {
                        # "time": i['time'],
                        "time": currenttimedate,
                        "headline": i['headline'],
                        "url": i['url'],
                        "categories": category,
                        "sentiment": sentiment,
                        "most_frequent_word": most_frequent_word,
                        "summary": summary,
                    }


                    with open(fileName, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)

                    try:
                        f = open(fileName)
                        data1 = json.load(f)
                    except Exception as error:
                        with open(fileName, 'w') as file:
                            file.write(json.dumps(data, indent=4))     



    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))

                
                
def JsonAppleNewsDataListWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/apple_news_data.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/apple_news_data.json', api_url=main_url+f'/media/upload_file/investing/json/apple_news_data.json')
    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            news_array_data = data['data']

        
            for i in DataList:

                if [x for x in news_array_data if x['headline'] == i['headline']] and [
                    x for x in news_array_data if x['time'] == i['time']] and [
                    x for x in news_array_data if x['url'] == i['url']]:
                    return

                else:
                    
                    category, sentiment, most_frequent_word, summary = SentimentAnalyzerFunction(i['headline'])

                    new_data = {
                        "time": i['time'],
                        "headline": i['headline'],
                        "url": i['url'],
                        "categories": category,
                        "sentiment": sentiment,
                        "most_frequent_word": most_frequent_word,
                        "summary": summary,
                    }

                    with open(fileName, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)

                    try:
                        f = open(fileName)
                        data1 = json.load(f)
                    except Exception as error:
                        with open(fileName, 'w') as file:
                            file.write(json.dumps(data, indent=4))
    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))            
                
def JsonRokuNewsDataListWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/roku_news_data.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/roku_news_data.json', api_url=main_url+f'/media/upload_file/investing/json/roku_news_data.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']

    
        for i in DataList:

            if [x for x in news_array_data if x['headline'] == i['headline']] and [
                x for x in news_array_data if x['time'] == i['time']] and [
                x for x in news_array_data if x['url'] == i['url']]:
                return

            else:

                category, sentiment, most_frequent_word, summary = SentimentAnalyzerFunction(i['headline'])
                
                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "time": i['time'],
                    "headline": i['headline'],
                    "url": i['url'],
                    "categories": category,
                    "sentiment": sentiment,
                    "most_frequent_word": most_frequent_word,
                    "summary": summary,
                }

                write_json(y)  
                
                


def JsonTeslaNewsDataListWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/tesla_news_data.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/tesla_news_data.json', api_url=main_url+f'/media/upload_file/investing/json/tesla_news_data.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']

    
        for i in DataList:

            if [x for x in news_array_data if x['headline'] == i['headline']] and [
                x for x in news_array_data if x['time'] == i['time']] and [
                x for x in news_array_data if x['url'] == i['url']]:
                return

            else:

                category, sentiment, most_frequent_word, summary = SentimentAnalyzerFunction(i['headline'])
                
                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "time": i['time'],
                    "headline": i['headline'],
                    "url": i['url'],
                    "categories": category,
                    "sentiment": sentiment,
                    "most_frequent_word": most_frequent_word,
                    "summary": summary,
                }

                write_json(y)
                
                
def JsonC3AiNewsDataListWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/c3ai_news_data.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/c3ai_news_data.json', api_url=main_url+f'/media/upload_file/investing/json/c3ai_news_data.json')
    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            news_array_data = data['data']
        
            for i in DataList:

                if [x for x in news_array_data if x['headline'] == i['headline']] and [
                    x for x in news_array_data if x['time'] == i['time']] and [
                    x for x in news_array_data if x['url'] == i['url']]:
                    return

                else:

                    category, sentiment, most_frequent_word, summary = SentimentAnalyzerFunction(i['headline'])
                    
                    new_data = {
                        "time": i['time'],
                        "headline": i['headline'],
                        "url": i['url'],
                        "categories": category,
                        "sentiment": sentiment,
                        "most_frequent_word": most_frequent_word,
                        "summary": summary,
                    }

                    with open(fileName, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)

                    try:
                        f = open(fileName)
                        data1 = json.load(f)
                    except Exception as error:
                        with open(fileName, 'w') as file:
                            file.write(json.dumps(data, indent=4))  
                
    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))            
                
def JsonRivianNewsDataListWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/rivian_news_data.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/rivian_news_data.json', api_url=main_url+f'/media/upload_file/investing/json/rivian_news_data.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']
    
        for i in DataList:

            if [x for x in news_array_data if x['headline'] == i['headline']] and [
                x for x in news_array_data if x['time'] == i['time']] and [
                x for x in news_array_data if x['url'] == i['url']]:
                return

            else:
                
                category, sentiment, most_frequent_word, summary = SentimentAnalyzerFunction(i['headline'])

                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "time": i['time'],
                    "headline": i['headline'],
                    "url": i['url'],
                    "categories": category,
                    "sentiment": sentiment,
                    "most_frequent_word": most_frequent_word,
                    "summary": summary,
                }

                write_json(y) 
                
                
def JsonYahooHistDataListWrite(symbol, DataList):
    fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/yahoo_finance_hist/{symbol}.json', api_url=main_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']
    
        for i in DataList:

            if [x for x in news_array_data if x['Date'] == i['Date']]:
                return

            else:

                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "Date": i['Date'],
                    "Open": i['Open'],
                    "High": i['High'],
                    "Low": i['Low'],
                    "Close": i['Close'],
                    "Volume": i['Volume'],
                    "Dividends": i['Dividends'],
                    "Stock Splits": i['Stock Splits'],
                }

                write_json(y)
    else:
        f = open(fileName, 'wb')
        jsonformat = {
            "data": DataList
        }
        json_object = json.dumps(jsonformat, indent=4)
        with open(fileName, "w") as outfile:
            outfile.write(json_object)
            
            
def JsonYahooHistDataListWrite1(symbol, DataList):
    fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/yahoo_finance_hist/{symbol}.json', api_url=main_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']
    
        for i in DataList:

            if [x for x in news_array_data if x['Date'] == i['Date']]:
                return

            else:

                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "Date": i['Date'],
                    "Open": i['Open'],
                    "High": i['High'],
                    "Low": i['Low'],
                    "Close": i['Close'],
                    "Adj Close": i['Adj Close'],
                    "Volume": i['Volume'],
                }

                write_json(y)
    else:
        f = open(fileName, 'wb')
        jsonformat = {
            "data": DataList
        }
        json_object = json.dumps(jsonformat, indent=4)
        with open(fileName, "w") as outfile:
            outfile.write(json_object)


def JsonYahooDataWrite(symbol, DataList):
    fileName = main_media_url+f'/media/upload_file/yahoo_finance/{symbol}.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/yahoo_finance/{symbol}.json', api_url=main_url+f'/media/upload_file/yahoo_finance/{symbol}.json')

    
    f = open(fileName, 'wb')
    jsonformat = {
        "data": [DataList]
    }
    json_object = json.dumps(jsonformat, indent=4)
    with open(fileName, "w") as outfile:
        outfile.write(json_object)
        
        

def JsonYahooFinanceInfoDataWrite(currenttimedate, symbol, DataList):
    fileName = main_media_url+f'/media/upload_file/yahoo_finance/{symbol}.json'
    fileNameYLog = main_media_url+f'/media/upload_file/investing/json/y_log.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/yahoo_finance/{symbol}.json', api_url=main_url+f'/media/upload_file/yahoo_finance/{symbol}.json')

    f = open(fileName, 'wb')
    jsonformat = {
        "data": [DataList]
    }
    json_object = json.dumps(jsonformat, indent=4)
    with open(fileName, "w") as outfile:
        outfile.write(json_object)

    f_y_log = open(fileNameYLog)
    y_log_data = json.load(f_y_log)
    y_data = y_log_data['y_log']

    compareValue = [x for x in y_data if x['process_name'] == 'Yahoo Finance Info' and x['symbol'] == symbol]
    if len(compareValue)!=0:
        for j in range(len(y_data)):
            if y_data[j]['symbol'] ==  symbol and y_data[j]['process_name'] == 'Yahoo Finance Info':
                y_data[j]['process_name'] = 'Yahoo Finance Info'
                y_data[j]['symbol'] = symbol
                y_data[j]['date'] = currenttimedate
                file_data={}
                with open(fileNameYLog, 'w', encoding='utf-8') as file:
                    file_data["y_log"]=y_data
                    json.dump(file_data, file, indent=4)
    else:
        def write_json_log(new_data, filename=fileNameYLog):
            with open(filename, 'r+') as file:
                file_data = json.load(file)
                file_data["y_log"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        y = {
            "process_name": "Yahoo Finance Info",
            "symbol": symbol,
            "date": currenttimedate
        }

        write_json_log(y)

        
def JsonYahooDynamicDataWrite(currenttimedate, symbol, DataList):
    fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json'
    fileNameYLog = main_media_url+f'/media/upload_file/investing/json/y_log.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/yahoo_finance_hist/{symbol}.json', api_url=main_url+f'/media/upload_file/yahoo_finance_hist/{symbol}.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        news_array_data = data['data']

        f_y_log = open(fileNameYLog)
        y_log_data = json.load(f_y_log)
        y_data = y_log_data['y_log']

        compareValue = [x for x in y_data if x['process_name'] == 'Yahoo Finance' and x['symbol'] == symbol]
        if len(compareValue)!=0:
            for j in range(len(y_data)):
                if y_data[j]['symbol'] ==  symbol and y_data[j]['process_name'] == 'Yahoo Finance':
                    y_data[j]['process_name'] = 'Yahoo Finance'
                    y_data[j]['symbol'] = symbol
                    y_data[j]['date'] = currenttimedate
                    file_data={}
                    with open(fileNameYLog, 'w', encoding='utf-8') as file:
                        file_data["y_log"]=y_data
                        json.dump(file_data, file, indent=4)
        else:
            def write_json_log(new_data, filename=fileNameYLog):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["y_log"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            y = {
                "process_name": "Yahoo Finance",
                "symbol": symbol,
                "date": currenttimedate
            }

            write_json_log(y)

    
        for i in DataList:
           
            
            if [x for x in news_array_data if x['Date'] == i['Date']]:
                return

            else:

                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "Date": i['Date'],
                    "Open": i['Open'],
                    "High": i['High'],
                    "Low": i['Low'],
                    "Close": i['Close'],
                    "Volume": i['Volume'],
                    "Dividends": i['Dividends'],
                    "Stock Splits": i['Stock Splits'],
                }

                write_json(y)

    else:
        f = open(fileName, 'wb')
        jsonformat = {
            "data": DataList
        }
        json_object = json.dumps(jsonformat, indent=4)
        with open(fileName, "w") as outfile:
            outfile.write(json_object)

        f_y_log = open(fileNameYLog)
        y_log_data = json.load(f_y_log)
        y_data = y_log_data['y_log']

        compareValue = [x for x in y_data if x['process_name'] == 'Yahoo Finance' and x['symbol'] == symbol]
        if len(compareValue)!=0:
            for j in range(len(y_data)):
                if y_data[j]['symbol'] ==  symbol and y_data[j]['process_name'] == 'Yahoo Finance':
                    y_data[j]['process_name'] = 'Yahoo Finance'
                    y_data[j]['symbol'] = symbol
                    y_data[j]['date'] = currenttimedate
                    file_data={}
                    with open(fileNameYLog, 'w', encoding='utf-8') as file:
                        file_data["y_log"]=y_data
                        json.dump(file_data, file, indent=4)
        else:
            def write_json_log(new_data, filename=fileNameYLog):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["y_log"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            y = {
                "process_name": "Yahoo Finance",
                "symbol": symbol,
                "date": currenttimedate
            }

            write_json_log(y)
        
    


def ProcessLogJsonWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/process_log.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/process_log.json', api_url=main_url+f'/media/upload_file/investing/json/process_log.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']


        for i in DataList:
            compareValue = [x for x in array_data if x['Process_Id'] == i['Process_Id'] and x['Process_Name'] == i['Process_Name'] and x['Time'] == i['Time']]
            if len(compareValue)!=0:
                for j in range(len(array_data)):
                    if array_data[j]['Process_Id'] ==  i['Process_Id'] and array_data[j]['Process_Name'] ==  i['Process_Name'] and array_data[j]['Time'] ==  i['Time']:
                        array_data[j]['Process_Id'] = i['Process_Id']
                        array_data[j]['Process_Name'] = i['Process_Name']
                        array_data[j]['Schedule'] = i['Schedule']
                        array_data[j]['Start_Date'] = i['Start_Date']
                        array_data[j]['End_Date'] = i['End_Date']
                        array_data[j]['Time'] = i['Time']
                        array_data[j]['Process_Status'] = i['Process_Status']
                        array_data[j]['Process_Type'] = i['Process_Type']
                        array_data[j]['Server_Name'] = i['Server_Name']
                        array_data[j]['Process_Code'] = i['Process_Code']
                        array_data[j]['Finished_Process'] = i['Finished_Process']
                        array_data[j]['error'] = i['error']
                        file_data={}
                        with open(fileName, 'w', encoding='utf-8') as file:
                            file_data["data"]=array_data
                            json.dump(file_data, file, indent=4)

            else:          
                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
            
                y = {
                    "Process_Id": i['Process_Id'],
                    "Process_Name": i['Process_Name'],
                    "Schedule": i['Schedule'],
                    "Start_Date": i['Start_Date'],
                    "End_Date": i['End_Date'],
                    "Time": i['Time'],
                    "Process_Status": i['Process_Status'],
                    "Process_Type": i['Process_Type'],
                    "Server_Name": i['Server_Name'],
                    "Process_Code": i['Process_Code'],
                    "Finished_Process": i['Finished_Process'],
                    "error": i['error'],
                }

                write_json(y)
            
            
def InternalProcessLogJsonWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/internal_process_log.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/internal_process_log.json', api_url=main_url+f'/media/upload_file/investing/json/internal_process_log.json')

    if os.path.isfile(fileName):
        for i in DataList:
            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            y = {
                "process_id": i['process_id'],
                "log_date": i['log_date'],
                "status_code": i['status_code'],
                "message": i['message']
            }

            write_json(y)
            
            
def NormalLogJsonWrite(DataList):
    fileName = main_media_url+'/media/upload_file/investing/json/normal_log.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/normal_log.json', api_url=main_url+f'/media/upload_file/investing/json/normal_log.json')

    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
            for i in DataList:
                compareValue = [x for x in array_data if x['process_name'] == i['process_name'] and x['server_name'] == i['server_name']]
                if len(compareValue)!=0:
                    for j in range(len(array_data)):
                        if array_data[j]['process_name'] ==  i['process_name'] and array_data[j]['server_name'] ==  i['server_name']:
                            array_data[j]['response_time'] = i['response_time']
                            array_data[j]['till_time'] = i['till_time']
                            array_data[j]['process_name'] = i['process_name']
                            array_data[j]['server_name'] = i['server_name']
                            array_data[j]['status'] = i['status']
                            file_data={}
                            with open(fileName, 'w', encoding='utf-8') as file:
                                file_data["data"]=array_data
                                json.dump(file_data, file, indent=4)

                            try:
                                f = open(fileName)
                                data1 = json.load(f)
                            except Exception as error:
                                with open(fileName, 'w') as file:
                                    file.write(json.dumps(data, indent=4))     
                
                    
                else:            
                    def write_json(new_data, filename=fileName):
                        with open(filename, 'r+') as file:
                            file_data = json.load(file)
                            file_data["data"].append(new_data)
                            file.seek(0)
                            json.dump(file_data, file, indent=4)
                    y = {
                        "response_time": i['response_time'],
                        "till_time": i['till_time'],
                        "process_name": i['process_name'],
                        "server_name": i['server_name'],
                        "status": i['status'],
                    }

                    write_json(y)

                    try:
                        f = open(fileName)
                        data1 = json.load(f)
                    except Exception as error:
                        with open(fileName, 'w') as file:
                            file.write(json.dumps(data, indent=4))

    except Exception as err:
        print("NormalLogJsonWrite", str(err)) 
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))             
                
def HeartBeatJsonWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/Heartbeat.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/Heartbeat.json', api_url=main_url+'/media/upload_file/investing/json/Heartbeat.json')

    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
            for i in DataList:
                compareValue = [x for x in array_data if x['server_name'] == i['server_name']]
                if len(compareValue)!=0:
                    for j in range(len(array_data)):
                        if array_data[j]['server_name'] ==  i['server_name']:
                            array_data[j]['response_time'] = i['response_time']
                            array_data[j]['server_name'] = i['server_name']
                            array_data[j]['status'] = i['status']
                            file_data={}
                            with open(fileName, 'w', encoding='utf-8') as file:
                                file_data["data"]=array_data
                                json.dump(file_data, file, indent=4)

                            try:
                                f = open(fileName)
                                data1 = json.load(f)
                            except Exception as error:
                                with open(fileName, 'w') as file:
                                    file.write(json.dumps(data, indent=4))       
                
                    
                else:            
                    def write_json(new_data, filename=fileName):
                        with open(filename, 'r+') as file:
                            file_data = json.load(file)
                            file_data["data"].append(new_data)
                            file.seek(0)
                            json.dump(file_data, file, indent=4)
                    y = {
                        "response_time": i['response_time'],
                        "server_name": i['server_name'],
                        "status": i['status'],
                    }

                    write_json(y)

                    try:
                        f = open(fileName)
                        data1 = json.load(f)
                    except Exception as error:
                        with open(fileName, 'w') as file:
                            file.write(json.dumps(data, indent=4))   

    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))            
                
def MarketingMostActiveJsonWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/marketing_most_active.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/marketing_most_active.json', api_url=main_url+f'/media/upload_file/investing/json/marketing_most_active.json')

    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
            for index, row in DataList.iterrows():
                gm = time.strftime("%a, %d %b %Y %X", time.gmtime())
                currenttimestamp = datetime.strptime(gm, "%a, %d %b %Y %X").timestamp()
                currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                new_data = {
                    "time": currenttimedate,
                    "symbol": row['symbol'],
                    "value": row['value'],
                    "percent": row['percent'],
                }

                with open(fileName, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)

                try:
                    f = open(fileName)
                    data1 = json.load(f)
                except Exception as error:
                    with open(fileName, 'w') as file:
                        file.write(json.dumps(data, indent=4)) 

    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))                    
            
            
def MarketingGainerJsonWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/marketing_gainers.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/marketing_gainers.json', api_url=main_url+f'/media/upload_file/investing/json/marketing_gainers.json')

    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
            for index, row in DataList.iterrows():
                gm = time.strftime("%a, %d %b %Y %X", time.gmtime())
                currenttimestamp = datetime.strptime(gm, "%a, %d %b %Y %X").timestamp()
                currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                new_data = {
                    "time": currenttimedate,
                    "symbol": row['symbol'],
                    "value": row['value'],
                    "percent": row['percent'],
                }

                with open(fileName, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)

                try:
                    f = open(fileName)
                    data1 = json.load(f)
                except Exception as error:
                    with open(fileName, 'w') as file:
                        file.write(json.dumps(data, indent=4)) 

    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))

            
def MarketingLoserJsonWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/marketing_losers.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/marketing_losers.json', api_url=main_url+f'/media/upload_file/investing/json/marketing_losers.json')

    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
            for index, row in DataList.iterrows():
                gm = time.strftime("%a, %d %b %Y %X", time.gmtime())
                currenttimestamp = datetime.strptime(gm, "%a, %d %b %Y %X").timestamp()
                currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
                
                new_data = {
                    "time": currenttimedate,
                    "symbol": row['symbol'],
                    "value": row['value'],
                    "percent": row['percent'],
                }

                with open(fileName, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)

                try:
                    f = open(fileName)
                    data1 = json.load(f)
                except Exception as error:
                    with open(fileName, 'w') as file:
                        file.write(json.dumps(data, indent=4)) 

    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))        
            
def GoogleNewsJsonWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/google_news.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/google_news.json', api_url=main_url+f'/media/upload_file/investing/json/google_news.json')
    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
            for index, row in DataList.iterrows():
                if [x for x in array_data if x['title'] == row['title']] and [
                    x for x in array_data if x['url'] == row['url']]:
                    return
                else:
                    gm = time.strftime("%a, %d %b %Y %X", time.gmtime())
                    currenttimestamp = datetime.strptime(gm, "%a, %d %b %Y %X").timestamp()
                    currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
                    
                    category, sentiment, most_frequent_word, summary = SentimentAnalyzerFunction(row['title'])

                    new_data = {
                        "time": currenttimedate,
                        "title": row['title'],
                        "url": row['url'],
                        "categories": category,
                        "sentiment": sentiment,
                        "most_frequent_word": most_frequent_word,
                        "summary": summary,
                    }
                    
                    with open(fileName, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)

                    try:
                        f = open(fileName)
                        data1 = json.load(f)
                    except Exception as error:
                        with open(fileName, 'w') as file:
                            file.write(json.dumps(data, indent=4))
    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))                
                
def GoogleFinanceJsonWrite(DataList):
    fileName = main_media_url+f'/media/upload_file/investing/json/google_finance_news.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/google_finance_news.json', api_url=main_url+f'/media/upload_file/investing/json/google_finance_news.json')

    try:
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
            for index, row in DataList.iterrows():
                if [x for x in array_data if x['title'] == row['title']] and [
                    x for x in array_data if x['url'] == row['url']]:
                    return
                else:
                    gm = time.strftime("%a, %d %b %Y %X", time.gmtime())
                    currenttimestamp = datetime.strptime(gm, "%a, %d %b %Y %X").timestamp()
                    currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
                    
                    category, sentiment, most_frequent_word, summary = SentimentAnalyzerFunction(row['title'])

                    new_data = {
                        "time": currenttimedate,
                        "title": row['title'],
                        "url": row['url'],
                        "categories": category,
                        "sentiment": sentiment,
                        "most_frequent_word": most_frequent_word,
                        "summary": summary,
                    }
                    
                    with open(fileName, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)

                    try:
                        f = open(fileName)
                        data1 = json.load(f)
                    except Exception as error:
                        with open(fileName, 'w') as file:
                            file.write(json.dumps(data, indent=4))

    except Exception as error:
        with open(fileName, 'w') as file:
            new_data1={
            "data": []
            }
            file.write(json.dumps(new_data1, indent=4))            
                
def YahooFinanceHistDataJsonWrite1(Symbol, DataList):
    fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{Symbol}.json'
    ChangeLogFunction(folder_path=f'/media/upload_file/yahoo_finance_hist/{Symbol}.json', api_url=main_url+f'/media/upload_file/yahoo_finance_hist/{Symbol}.json')

    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']
        
        for index, row in DataList.iterrows():
            
            gm = time.strftime("%a, %d %b %Y %X", time.gmtime())
            currenttimestamp = datetime.strptime(gm, "%a, %d %b %Y %X").timestamp()
            currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
                
            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            y = {
                "Date": row['Date'],
                "Open": row['Open'],
                "High": row['High'],
                "Low": row['Low'],
                "Close": row['Close'],
                "Volume": row['Volume'],
                "Dividends": row['Dividends'],
                "Stock Splits": row['Stock Splits'],
            }
    
            write_json(y)   
            
            
@api_view(['POST'])
def YahooFinanceHistDataAPI1(request):
    try:
        Symbol = request.data['symbol']
        DataList = request.data['datalist']
        YahooFinanceHistDataJsonWrite1(Symbol, DataList)
        return Response({'message':'Json Yahoo Hist Data1 List Added Successfully','status': status.HTTP_201_CREATED},)
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)  
            


@api_view(['POST'])
def RegisterDriver(request):
    try:
        APICALLFUNCTION('Register', 'null')
        first_name=request.data['first_name']
        last_name=request.data['last_name']
        email=request.data['email']
        password=request.data['password']
        zip_code=request.data['zip_code']
        
        val_email = validateEmail(email)
        
        if User.objects.filter(email=email).exists():
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        if val_email==False:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Email is not valid!"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(email=email, password=password, role='Driver')
        print('29')
        user.set_password(user.password)
        user.save() 
        print('32', user.id)
        user_detail = UserDetail.objects.create(user=user, first_name=first_name, last_name=last_name, zip_code=zip_code)
        user_detail.save()
        print('35')
         
        current_site = get_current_site(request)
        domain= current_site.domain
        uid= urlsafe_base64_encode(force_bytes(user.pk))
        token= default_token_generator.make_token(user)
        print('35',user.email)
        
        send_activation_mail(user.email, user_detail.first_name, domain, uid, token)
        
        serializer_user_master = UserMasterSerializerWithToken(user, many=False)
        serializer_user_detail = UserDetailSerializer(user_detail, many=False)
        print('62')
        return Response({'message':'Driver Account Created Successfully','status': status.HTTP_201_CREATED, 'user':serializer_user_master.data, 'user_detail':serializer_user_detail.data},)

    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)
    
    
def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False    
    
    
@api_view(['GET'])   
def DriverActivation(request, uidb64, token):
    try: 
        
        APICALLFUNCTION('Activation', 'null')
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Usermodel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_varified = True
        user.save()
        return redirect('http://localhost:3000/')
        # return Response({'status':200,'message':'Your Acount is activated and email is verified, please now login your account.'})  
    else:
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Activation link is invalid.'}, status=status.HTTP_400_BAD_REQUEST)   
    
    
@api_view(['POST'])    
def DriverLogin(request):
    try:
        APICALLFUNCTION('login', 'null')
        email = request.data['email']
        password = request.data['password']
        
        val_email = validateEmail(email)
        if val_email==False:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Email is not valid!"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active == True and user.role == 'Driver' and user.is_email_varified == True:
                login(request, user)
                serializer = UserMasterSerializerWithToken(user, many=False)
                return Response({'status': status.HTTP_200_OK, 'message': 'Driver Login Successfully', 'data': serializer.data})
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Not Valid active user and email verified and not valid customer'}, status=status.HTTP_404_NOT_FOUND)    
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'do not match the email or password.please correct email and password.'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'message':"Something error!"}, status=status.HTTP_400_BAD_REQUEST)    
        
        
        
        
        
@api_view(['POST'])
def JsonGmailDataAPI(request):
    try:
        APICALLFUNCTION('JsonGmailDataAPI', 'null')
        subject=request.data['subject']
        sender=request.data['sender']
        date=request.data['date']
        body=request.data['body']
        currenttimedate=request.data['currenttimedate']
        JsonWrite(subject, sender, date, body, currenttimedate)
        return Response({'message':'Json file Created Successfully','status': status.HTTP_201_CREATED},)

    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
        
        
@api_view(['POST'])
def JsonNewsDataAPI(request):
    try:
        APICALLFUNCTION('JsonNewsDataAPI', 'null')
        time=request.data['time']
        headline=request.data['headline']
        JsonNewsDataWrite(time, headline)
        return Response({'message':'Json News Data Added Successfully','status': status.HTTP_201_CREATED},)

    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
        
@api_view(['POST'])
def JsonNewsDataListAPI(request):
    try:
        APICALLFUNCTION('JsonNewsDataListAPI', 'null')
        JsonNewsDataListWrite(request.data)
        return Response({'message':'Json News Data List Added Successfully','status': status.HTTP_201_CREATED},)

    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)        
        
        
@api_view(['POST'])
def JsonCNBCNewsDataListAPI(request):
    try:
        APICALLFUNCTION('JsonCNBCNewsDataListAPI', 'null')
        JsonCNBCNewsDataListWrite(request.data)
        return Response({'message':'Json CNBC News Data List Added Successfully','status': status.HTTP_201_CREATED},)

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors'}, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
def JsonAPPLENewsDataListAPI(request):
    try:
        APICALLFUNCTION('JsonAPPLENewsDataListAPI', 'null')
        JsonAppleNewsDataListWrite(request.data)
        return Response({'message':'Json Apple News Data List Added Successfully','status': status.HTTP_201_CREATED},)

    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)        
        
@api_view(['POST'])        
def JsonROKUNewsDataListAPI(request):
    try:
        APICALLFUNCTION('JsonROKUNewsDataListAPI', 'null')
        JsonRokuNewsDataListWrite(request.data)
        return Response({'message':'Json Roku News Data List Added Successfully','status': status.HTTP_201_CREATED},)

    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
def JsonTeslaNewsDataListAPI(request):
    try:
        APICALLFUNCTION('JsonTeslaNewsDataListAPI', 'null')
        JsonTeslaNewsDataListWrite(request.data)
        return Response({'message':'Json Tesla News Data File Added Successfully','status': status.HTTP_201_CREATED},)
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def ProcessLogAPI(request):
    try:
        APICALLLOGFUNCTION('ProcessLogAPI', 'null')
        ProcessLogJsonWrite(request.data)
        return Response({'message':'Process Log Successfully Created','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)        
        
@api_view(['GET'])
def ServerOnOffcheckApi(request):
    try:
        return Response({'message':'Main server ON','status': status.HTTP_200_OK},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)        
        
        
@api_view(['POST'])
def InternalProcessLogAPI(request):
    try:
        APICALLLOGFUNCTION('InternalProcessLogAPI', 'null')
        InternalProcessLogJsonWrite(request.data)
        return Response({'message':'Internal Process Log Successfully Created','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
        
        
      
        
        
@api_view(['POST'])
def HeartbeatAPI(request):
    try:
        APICALLSTATUSFUNCTION('HeartbeatAPI', 'null')
        HeartBeatJsonWrite(request.data)
        return Response({'message':'Heartbeat Log Successfully Created','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
@api_view(['POST'])
def ProcessRestartAPI(request):
    now_utc = datetime.utcnow()
    currenttimedate = datetime.strftime(now_utc, '%Y-%m-%d %H:%M:%S')
    sec = datetime.strftime(now_utc, '%S')
    currenttimestamp = datetime.strptime(currenttimedate, "%Y-%m-%d %H:%M:%S").timestamp()
    try:
        server_name = request.data['server_name']
        fileName = main_media_url+f'/media/upload_file/investing/json/Heartbeat.json'
        ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/Heartbeat.json', api_url=main_url+'/media/upload_file/investing/json/Heartbeat.json')
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            server_data = [x for x in array_data if x['server_name'] == server_name]
            timeDiff = currenttimestamp - datetime.strptime(server_data[0]['response_time'], "%Y-%m-%d %H:%M:%S").timestamp()
           
            print("timeDiff", timeDiff,  type(timeDiff), int(timeDiff), int(int(timeDiff)/60))
            if int(int(timeDiff)/60) > 2:
                fileName1 = main_media_url+f'/media/upload_file/investing/json/normal_log.json'
                ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/normal_log.json', api_url=local_main_url+'/media/upload_file/investing/json/normal_log.json')
                if os.path.isfile(fileName1):
                    f1 = open(fileName1)
                    data1 = json.load(f1)
                    array_data1 = data1['data']
                    item_data = []
                    sections = {}
                    for l in range(len(array_data1)):
                        if array_data1[l]['server_name'] == server_name:
                            array_data1[l]['status'] = "Done"
                            with open(fileName1, 'w', encoding='utf-8') as json_file:
                                file_data={}
                                file_data["data"]=array_data1
                                json.dump(file_data, json_file, indent=4)
                                
                                
    
                  
                    # with open(fileName1, 'w', encoding='utf-8') as json_file:
                    #     file_data={}
                    #     file_data["normal_log"]=item_data
                    #     json.dump(file_data, json_file, indent=4)
                        
                    
                    

        return Response({'message':'Process Restart Successfully','status': status.HTTP_200_OK},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)         
        

@api_view(['POST'])
def NormalLogAPI(request):
    try:
        APICALLLOGFUNCTION('NormalLogAPI', 'null')
        NormalLogJsonWrite(request.data)
        return Response({'message':'Normal Log Successfully Created','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)         


        
        
@api_view(['POST'])
def JsonC3AiNewsDataListAPI(request):
    try:
        APICALLFUNCTION('JsonC3AiNewsDataListAPI', 'null')
        JsonC3AiNewsDataListWrite(request.data)
        return Response({'message':'Json C3Ai News Data List Added Successfully','status': status.HTTP_201_CREATED},)
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
@api_view(['POST'])
def JsonRivianNewsDataListAPI(request):
    try:
        APICALLFUNCTION('JsonRivianNewsDataListAPI', 'null')
        JsonRivianNewsDataListWrite(request.data)
        return Response({'message':'Json Rivian News Data List Added Successfully','status': status.HTTP_201_CREATED},)
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
@api_view(['POST'])
def JsonYahooHistAPI(request):
    try:
        APICALLFUNCTION('JsonYahooHistAPI', 'null')
        symbol = request.data['symbol']
        datalist = request.data['datalist']
        JsonYahooHistDataListWrite(symbol, datalist)
        return Response({'message':'Json Yahoo Hist Data List Added Successfully','status': status.HTTP_201_CREATED},)
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)          
        
@api_view(['POST'])
def JsonYahooHistAPI1(request):
    try:
        APICALLFUNCTION('JsonYahooHistAPI1', 'null')
        symbol = request.data['symbol']
        datalist = request.data['datalist']
        JsonYahooHistDataListWrite1(symbol, datalist)
        return Response({'message':'Json Yahoo Hist Data List1 Added Successfully','status': status.HTTP_201_CREATED},)
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)          
        
        
@api_view(['POST'])
def JsonYahooAPI(request):
    try:
        APICALLFUNCTION('JsonYahooAPI', 'null')
        symbol = request.data['symbol']
        datalist = request.data['datalist']
        JsonYahooDataWrite(symbol, datalist)
        return Response({'message':'Json Yahoo Data Added Successfully','status': status.HTTP_201_CREATED},)
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST) 
        
   
   
def JsonConvertYahooFinance(df):
    DataReturn=[]
    KeyItem = []
    sections={}
    for key, value in df.iteritems():
        KeyItem.append(key)

   
    for index, row in df.iterrows():
        for i in range(len(KeyItem)):
            sections['Date']=datetime.strftime(index, '%Y-%m-%d')
            sections[KeyItem[i]]= row[KeyItem[i]]
        if sections != "":
            DataReturn.append(sections)
            sections={}

    return DataReturn   
        
@api_view(['POST'])
def JsonYahooDynamicAPI(request):
    try:
        APICALLFUNCTION('JsonYahooDynamicAPI', 'null')
        now_utc = datetime.utcnow()
        currenttimedate = datetime.strftime(now_utc, '%Y-%m-%d')
        currenttimestamp = datetime.strptime(currenttimedate, "%Y-%m-%d").timestamp()
        

        symbol = request.data['symbol']


        f = open(main_media_url+"/media/upload_file/investing/json/y_log.json")
        data = json.load(f)
        y_log_data = data['y_log']
        y_data = [x for x in y_log_data if x['process_name'] == 'Yahoo Finance' and x['symbol'] == symbol]
    

        if len(y_data) != 0:
          
            msft = yf.Ticker(symbol)

            dif_day = int((datetime.strptime(currenttimedate, "%Y-%m-%d") - datetime.strptime(y_data[0]['date'], "%Y-%m-%d")).days)

            data = msft.history(period=f"{dif_day}d")
            datalist = JsonConvertYahooFinance(data)
            JsonYahooDynamicDataWrite(currenttimedate, symbol, datalist)

           
            

        else:
            msft = yf.Ticker(symbol)
            data = msft.history(period="3y")
            datalist = JsonConvertYahooFinance(data)

            JsonYahooDynamicDataWrite(currenttimedate, symbol, datalist)

        return Response({'message':'Json Yahoo Dynamic Data Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
def JsonYahooFinanceInfoAPI(request):
    try:
        APICALLFUNCTION('JsonYahooFinanceInfoAPI', 'null')
        now_utc = datetime.utcnow()
        currenttimedate = datetime.strftime(now_utc, '%Y-%m-%d')
        currenttimestamp = datetime.strptime(currenttimedate, "%Y-%m-%d").timestamp()
        

        symbol = request.data['symbol']


       
        msft = yf.Ticker(symbol)
        datalist = msft.info

        JsonYahooFinanceInfoDataWrite(currenttimedate, symbol, datalist)

        return Response({'message':'Json Yahoo Finance Info Data Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
        
        
        
 


        
        

        
        
def TableDataFile(table_data_id, table_id, column_id, column_name, column_data):
    def write_json(new_data, filename=main_media_url+'/media/upload_file/json/TableData.json'):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data["table_data"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    
    y = {
        "table_data_id": table_data_id,
        "table_id": table_id,
        "column_id": column_id,
        "column_name": column_name,
        "column_data": column_data,
        }
        
    write_json(y)

    
@api_view(['POST'])
def CreateTableDataJsonAPI(request):
    try:
        APICALLFUNCTION('CreateTableDataJsonAPI', 'null')
        table_data_id=request.data['table_data_id']
        table_id=request.data['table_id']
        column_id=request.data['column_id']
        column_name=request.data['column_name']
        column_data=request.data['column_data']
        TableDataFile(table_data_id, table_id, column_id, column_name, column_data)
        return Response({'message':'Json file Created Successfully','status': status.HTTP_201_CREATED},)

    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)   
        
        
        
        
def NodeDataJsonWrite(name, node_data):
    fileName = main_media_url+f'/media/upload_file/node-design/node_design.json'
    if os.path.isfile(fileName):
        f = open(fileName)
        data = json.load(f)
        array_data = data['node_design']
        compareValue = [x for x in array_data if name in x]
        if compareValue:
            for i in range(len(array_data)):
                for j in range(len(compareValue)):
                    if compareValue[j] == array_data[i]:
                        array_data[i][name] = node_data
                        file_data={}
                        with open(fileName, 'w', encoding='utf-8') as file:
                            file_data["node_design"]=array_data
                            json.dump(file_data, file, indent=4)
            

        else:
            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["node_design"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            y = {
                name: node_data
            }

            write_json(y)   


@api_view(['POST'])
def JsonNodeDataAPI(request):
    try:
        APICALLFUNCTION('JsonNodeDataAPI', 'null')
        name = request.data['name']
        node_data = request.data['node_data']
        NodeDataJsonWrite(name, node_data)
        return Response({'message':'Node Data Added Successfully','status': status.HTTP_201_CREATED},)
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)   
        
        
        
@api_view(['POST'])
def InvestingCalenderJsonDataAPI(request):
    try:
        APICALLFUNCTION('InvestingCalenderJsonDataAPI', 'null')
        df = pd.DataFrame(request.data)
        InvestingCalderJsonWrite(df)
        return Response({'message':'InvestingCalender Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
@api_view(['POST'])
def InvestingReutersJsonDataAPI(request):
    try:
        APICALLFUNCTION('InvestingReutersJsonDataAPI', 'null')
        df = pd.DataFrame(request.data)
        InvestingReutersJsonWrite(df)
        return Response({'message':'Investing Reuters Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  



        
@api_view(['POST'])
def MarketingMostActiveJsonDataAPI(request):
    try:
        APICALLFUNCTION('MarketingMostActiveJsonDataAPI', 'null')
        df = pd.DataFrame(request.data)
        MarketingMostActiveJsonWrite(df)
        return Response({'message':'Marketing Most Active Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        
@api_view(['POST'])
def MarketingGainerJsonDataAPI(request):
    try:
        APICALLFUNCTION('MarketingGainerJsonDataAPI', 'null')
        df = pd.DataFrame(request.data)
        MarketingGainerJsonWrite(df)
        return Response({'message':'Marketing Gainer Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        
        
@api_view(['POST'])
def MarketingLoserJsonDataAPI(request):
    try:
        APICALLFUNCTION('MarketingLoserJsonDataAPI', 'null')
        df = pd.DataFrame(request.data)
        MarketingLoserJsonWrite(df)
        return Response({'message':'Marketing Loser Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
@api_view(['POST'])
def GoogleNewsJsonDataAPI(request):
    try:
        APICALLFUNCTION('GoogleNewsJsonDataAPI', 'null')
        df = pd.DataFrame(request.data)
        GoogleNewsJsonWrite(df)
        return Response({'message':'Google News Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
@api_view(['POST'])
def GoogleFinanceJsonDataAPI(request):
    try:
        APICALLFUNCTION('GoogleFinanceJsonDataAPI', 'null')
        df = pd.DataFrame(request.data)
        GoogleFinanceJsonWrite(df)
        return Response({'message':'Google finance Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)        
        
        
        
        
        
@api_view(['GET'])
def JsonArrayMergeDataAPI(request):
    try:
        startTime = CurrentTimeFunc()        

        with open(main_media_url+f'/media/upload_file/yahoo_finance_hist/AAOI.json', 'r') as file:
            fileData = json.load(file)
            
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(fileData)
        DataFetch_Static("JsonArrayMergeDataAPI", "JsonArrayMergeData function", value_count, round(loadTime, 6))   
        
        return Response({'message':"Successfully Fetch DataList",'status': status.HTTP_200_OK, "data": fileData})    
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
        
        
@api_view(['GET'])
def FileTransferAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('FileTransferAPI', 'null')
        fileName = main_media_url+'/media/upload_file/process'
        dir_list = os.listdir(fileName)
        listUrl=[]
        listName=[]
        for m in dir_list:
            if m == '__pycache__':
                pass 
            
            else:
                file = 'https://itb-usa.a2hosted.com'+fileName+"/"+m
                listUrl.append(file)
                listName.append(m)
                
                
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(listName)
        DataFetch_Static("FileTransferAPI", "FileTransfer function", value_count, round(loadTime, 6)) 
        
        return Response({'status': status.HTTP_200_OK, 'data_url':listUrl, 'data_name': listName})
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)  


        
@api_view(['GET'])
def FileTransferYahooFinanceHistAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('FileTransferYahooFinanceHistAPI', 'null')
        fileName = main_media_url+'/media/upload_file/yahoo_finance_hist'
        dir_list = os.listdir(fileName)
        listUrl=[]
        listName=[]
        for m in dir_list:
            if m == '__pycache__':
                pass 
            
            else:
                file = 'https://itb-usa.a2hosted.com'+fileName+"/"+m
                listUrl.append(file)
                listName.append(m)
                
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(listName)
        DataFetch_Static("FileTransferYahooFinanceHistAPI", "FileTransferYahooFinanceHist function", value_count, round(loadTime, 6)) 
                
                
        return Response({'status': status.HTTP_200_OK, 'data_url':listUrl, 'data_name': listName})
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST) 
        
@api_view(['GET'])
def FileTransferYahooFinanceAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('FileTransferYahooFinanceAPI', 'null')
        fileName = main_media_url+'/media/upload_file/yahoo_finance'
        dir_list = os.listdir(fileName)
        listUrl=[]
        listName=[]
        for m in dir_list:
            if m == '__pycache__':
                pass 
            
            else:
                file = 'https://itb-usa.a2hosted.com'+fileName+"/"+m
                listUrl.append(file)
                listName.append(m)
                
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(listName)
        DataFetch_Static("FileTransferYahooFinanceAPI", "FileTransferYahooFinance function", value_count, round(loadTime, 6)) 
                        
                
        return Response({'status': status.HTTP_200_OK, 'data_url':listUrl, 'data_name': listName})
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET'])
def FileTransferJsonAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('FileTransferJsonAPI', 'null')
       
        fileName = main_media_url+'/media/upload_file/json'
        dir_list = os.listdir(fileName)
        listUrl=[]
        listName=[]
        for m in dir_list:
            if m == '__pycache__':
                pass 
            
            else:
                file = 'https://itb-usa.a2hosted.com'+fileName+"/"+m
                listUrl.append(file)
                listName.append(m)
                
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(listName)
        DataFetch_Static("FileTransferJsonAPI", "FileTransferJson function", value_count, round(loadTime, 6))         
                
        return Response({'status': status.HTTP_200_OK, 'data_url':listUrl, 'data_name': listName})
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)  
        
@api_view(['GET'])
def FileTransferInvestingJsonAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('FileTransferInvestingJsonAPI', 'null')
       
        fileName = main_media_url+'/media/upload_file/investing/json'
        dir_list = os.listdir(fileName)
        listUrl=[]
        listName=[]
        for m in dir_list:
            if m == '__pycache__':
                pass 
            
            else:
                file = 'https://itb-usa.a2hosted.com'+fileName+"/"+m
                listUrl.append(file)
                listName.append(m)
                
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(listName)
        DataFetch_Static("FileTransferInvestingJsonAPI", "FileTransferInvestingJson function", value_count, round(loadTime, 6))        
                
        return Response({'status': status.HTTP_200_OK, 'data_url':listUrl, 'data_name': listName})
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def FileTransferInvestingCsvAPI(request):
    try:
        startTime = CurrentTimeFunc()
       
        APICALLFUNCTION('FileTransferInvestingCsvAPI', 'null')
        
        fileName = main_media_url+'/media/upload_file/investing/csv'
        dir_list = os.listdir(fileName)
        listUrl=[]
        listName=[]
        for m in dir_list:
            if m == '__pycache__':
                pass 
            
            else:
                file = 'https://itb-usa.a2hosted.com'+fileName+"/"+m
                listUrl.append(file)
                listName.append(m)
                
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(listName)
        DataFetch_Static("FileTransferInvestingCsvAPI", "FileTransferInvestingCsv function", value_count, round(loadTime, 6))         
                
        return Response({'status': status.HTTP_200_OK, 'data_url':listUrl, 'data_name': listName})
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
@api_view(['GET'])
def ProcessNameAPI(request):
    try:
        startTime = CurrentTimeFunc()
        
        APICALLFUNCTION('ProcessNameAPI', 'null')
       
        fileName = main_media_url+'/media/upload_file/process'
        dir_list = os.listdir(fileName)
        listName=[]
        for m in dir_list:
            if m == '__pycache__':
                pass 
            
            else:
                listName.append(m)
                
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(listName)
        DataFetch_Static("ProcessNameAPI", "ProcessName function", value_count, round(loadTime, 6))          
                
        return Response({'status': status.HTTP_200_OK, 'data_name': listName})
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
@api_view(['POST'])
def PipeLineApi(request):
    try:
        APICALLFUNCTION('PipeLineApi', 'null')
        code = request.data['code']
        api_name = request.data['api_name']
        user = request.data['user']
        paramList = request.data['paramList']


        code_v = "    if user == "+ "'"+ user +"'" +" and api_name == "+ "'"+ api_name +"'"+" and "+" paramList"+":"
        code_v1 = "        a=''"
        code_v2 = "        b=''"
        code_v3 = "        for key, values in paramList.items():"
        code_v4 = "            if key == 'a':"
        code_v5 = "                a = values"
        code_v6 = "            if key == 'b':"
        code_v7 = "                b = values"
       
        
     

        fileName = main_media_url+f'/media/upload_file/dynamic_rest/Custom.py'
        ChangeLogFunction(folder_path=f'/media/upload_file/dynamic_rest/Custom.py', api_url=main_url+f'/media/upload_file/dynamic_rest/Custom.py')

        # fileName = f'/home/itbusaah/idriver_education_djangoproject/static/upload_folder/dynamic_rest/Custom.py'
       
        f = open(fileName, "a")
       
        f.write(code_v)
        f.write("\n")
        f.write(code_v1)
        f.write("\n")
        f.write(code_v2)
        f.write("\n")
        f.write(code_v3)
        f.write("\n")
        f.write(code_v4)
        f.write("\n")
        f.write(code_v5)
        f.write("\n")
        f.write(code_v6)
        f.write("\n")
        f.write(code_v7)
        f.write("\n")
       
        lines = code.split('\n')
        for line in lines:
            print(line) 
            f.write("\n        ")
            f.write(line)
          
        f.write("\n\n")
        f.close()


        return Response({'status': status.HTTP_200_OK, 'message':"pipeline api write successfully"},)
        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  



@api_view(['POST'])
def PipeLineApiHashKey(request, user_hashkey):
    try:
        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            APICALLFUNCTION('PipeLineApiHashKey', 'null')
            code = request.data['code']
            api_name = request.data['api_name']
            user = request.data['user']
            paramList = request.data['paramList']
    
    
            code_v = "    if user == "+ "'"+ user +"'" +" and api_name == "+ "'"+ api_name +"'"+" and "+" paramList"+":"
            code_v1 = "        a=''"
            code_v2 = "        b=''"
            code_v3 = "        for key, values in paramList.items():"
            code_v4 = "            if key == 'a':"
            code_v5 = "                a = values"
            code_v6 = "            if key == 'b':"
            code_v7 = "                b = values"
           
            
         
    
            fileName = main_media_url+f'/media/upload_file/dynamic_rest/Custom.py'
            ChangeLogFunction(folder_path=f'/media/upload_file/dynamic_rest/Custom.py', api_url=main_url+f'/media/upload_file/dynamic_rest/Custom.py')

            # fileName = f'/home/itbusaah/idriver_education_djangoproject/static/upload_folder/dynamic_rest/Custom.py'
           
            f = open(fileName, "a")
           
            f.write(code_v)
            f.write("\n")
            f.write(code_v1)
            f.write("\n")
            f.write(code_v2)
            f.write("\n")
            f.write(code_v3)
            f.write("\n")
            f.write(code_v4)
            f.write("\n")
            f.write(code_v5)
            f.write("\n")
            f.write(code_v6)
            f.write("\n")
            f.write(code_v7)
            f.write("\n")
           
            lines = code.split('\n')
            for line in lines:
                print(line) 
                f.write("\n        ")
                f.write(line)
              
            f.write("\n\n")
            f.close()
    
    
            return Response({'status': status.HTTP_200_OK, 'message':"pipeline api write successfully"},)
            
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)    
        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  



@api_view(['POST'])
def PipeLineApi2(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('PipeLineApi2', 'null')
        code = request.data['code']
        api_name = request.data['api_name']
        user = request.data['user']
        paramList = request.data['paramList']

        DataR = Custom(user, api_name, eval(paramList)) 
        
        
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(DataR)
        DataFetch_Static("PipeLineApi2", "Custom python file function", value_count, round(loadTime, 6))

        
        return Response({'status': status.HTTP_200_OK, 'message':"api data found successfully", "data": DataR},)
        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  

  
        
@api_view(['POST'])
def PipeLineApiHashKey2(request, user_hashkey):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('PipeLineApiHashKey2', 'null')

        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            code = request.data['code']
            api_name = request.data['api_name']
            user = request.data['user']
            paramList = request.data['paramList']
    
            DataR = Custom(user, api_name, eval(paramList)) 
            
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(DataR)
            DataFetch_Static("PipeLineApi2", "Custom python file function", value_count, round(loadTime, 6))
    
            
            return Response({'status': status.HTTP_200_OK, 'message':"api data found successfully", "data": DataR},)
        
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  

        
        


@api_view(['POST'])
def Custom_API_Code(request):
    try:
        APICALLFUNCTION('Custom_API_Code', 'null')
        code = request.data['code']
        code_object = request.data['code_object']
        api_name = request.data['api_name']
        api_file = request.data['api_file']
        user = request.data['user']
        
        code_v = "    if user == "+ "'"+ user +"'" +" and api_name == "+ "'"+ api_name +"'"+" and "+" paramList"+":"
        code_v1 = "        a=''"
        code_v2 = "        b=''"
        code_v3 = "        for key, values in paramList.items():"
        code_v4 = "            if key == 'a':"
        code_v5 = "                a = values"
        code_v6 = "            if key == 'b':"
        code_v7 = "                b = values"
       

        fileName = main_media_url+f'/media/upload_file/dynamic_rest/{api_file}.py'
        ChangeLogFunction(folder_path=f'/media/upload_file/dynamic_rest/{api_file}.py', api_url=main_url+f'/media/upload_file/dynamic_rest/{api_file}.py')

       
        f = open(fileName, "a")
        

        f.write(code_v)
        f.write("\n")
        f.write(code_v1)
        f.write("\n")
        f.write(code_v2)
        f.write("\n")
        f.write(code_v3)
        f.write("\n")
        f.write(code_v4)
        f.write("\n")
        f.write(code_v5)
        f.write("\n")
        f.write(code_v6)
        f.write("\n")
        f.write(code_v7)
        f.write("\n")

        lines = code.split('\n')
        for line in lines:
            f.write("\n        ")
            f.write(line)

        f.write("\n\n")
       
 
                       
        return Response({'status': status.HTTP_200_OK, 'message':"api file write successfully" },)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        


@api_view(['POST'])
def Custom_API_CodeHashkey(request, user_hashkey):
    try:
        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            APICALLFUNCTION('Custom_API_Code', 'null')
            code = request.data['code']
            code_object = request.data['code_object']
            api_name = request.data['api_name']
            api_file = request.data['api_file']
            user = request.data['user']
            
            code_v = "    if user == "+ "'"+ user +"'" +" and api_name == "+ "'"+ api_name +"'"+" and "+" paramList"+":"
            code_v1 = "        a=''"
            code_v2 = "        b=''"
            code_v3 = "        for key, values in paramList.items():"
            code_v4 = "            if key == 'a':"
            code_v5 = "                a = values"
            code_v6 = "            if key == 'b':"
            code_v7 = "                b = values"
           
    
            fileName = main_media_url+f'/media/upload_file/dynamic_rest/{api_file}.py'
            ChangeLogFunction(folder_path=f'/media/upload_file/dynamic_rest/{api_file}.py', api_url=main_url+f'/media/upload_file/dynamic_rest/{api_file}.py')

           
            f = open(fileName, "a")
            
    
            f.write(code_v)
            f.write("\n")
            f.write(code_v1)
            f.write("\n")
            f.write(code_v2)
            f.write("\n")
            f.write(code_v3)
            f.write("\n")
            f.write(code_v4)
            f.write("\n")
            f.write(code_v5)
            f.write("\n")
            f.write(code_v6)
            f.write("\n")
            f.write(code_v7)
            f.write("\n")
    
            lines = code.split('\n')
            for line in lines:
                f.write("\n        ")
                f.write(line)
    
            f.write("\n\n")
           
     
                           
            return Response({'status': status.HTTP_200_OK, 'message':"api file write successfully" },)
        
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)    
            
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 


        

@api_view(['POST'])
def Custom_Code(request):
    try:
        APICALLFUNCTION('Custom_Code', 'null')
        custom_code = request.data['custom_code']
#         code_v = f'''
# def Custom():
#     {custom_code}
# '''

        fileName = main_media_url+'/media/upload_file/process/Custom.py'
        ChangeLogFunction(folder_path=f'/media/upload_file/process/Custom.py', api_url=main_url+f'/media/upload_file/process/Custom.py')

        # open(fileName, 'w').write(code_v)
        
        # code = request.data['code']
        
       

       
        f = open(fileName, "a")
       
        # f.write(code_v)
        # f.write("\n")
        # f.write(code_v1)
        # f.write("\n")
        # f.write(code_v2)
        # f.write("\n")
        # f.write(code_v3)
        # f.write("\n")
        # f.write(code_v4)
        # f.write("\n")
        # f.write(code_v5)
        # f.write("\n")
        # f.write(code_v6)
        # f.write("\n")
        # f.write(code_v7)
        # f.write("\n")
       
        lines = custom_code.split('\n')
        for line in lines:
            print(line) 
            f.write("\n    ")
            f.write(line)
          
        f.write("\n\n")
        f.close()


                       
        return Response({'status': status.HTTP_200_OK, 'message':"custom file write successfully" },)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
 
@api_view(['POST'])
def Custom_Code_Async_Test(request):
    try:
        APICALLFUNCTION('Custom_Code_Async_Test', 'null')
        custom_code = request.data['custom_code']

        fileName = main_media_url+'/media/upload_file/process/AsyncTest.py'
        ChangeLogFunction(folder_path=f'/media/upload_file/process/AsyncTest.py', api_url=main_url+f'/media/upload_file/process/AsyncTest.py')


       
        f = open(fileName, "a")

       
        lines = custom_code.split('\n')
        for line in lines:
            print(line) 
            f.write("\n    ")
            f.write(line)
          
        f.write("\n\n")
        f.close()


                       
        return Response({'status': status.HTTP_200_OK, 'message':"Custom_Code_Async_Test file write successfully" },)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
 
 
@api_view(['POST'])
def Custom_CodeHashkey(request, user_hashkey):
    try:
        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            APICALLFUNCTION('Custom_Code', 'null')
            custom_code = request.data['custom_code']
            code_v = f'''
    def Custom():
        {custom_code}
    '''
    
            fileName = main_media_url+'/media/upload_file/process/Custom.py'
            ChangeLogFunction(folder_path=f'/media/upload_file/process/Custom.py', api_url=main_url+f'/media/upload_file/process/Custom.py')

            open(fileName, 'w').write(code_v)
                           
            return Response({'status': status.HTTP_200_OK, 'message':"custom file write successfully" },)
            
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)    
            
            
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
 


@api_view(['POST'])
def Custom_Code_Validate(request):
    try:
        APICALLFUNCTION('Custom_Code_Validate', 'null')
        custom_code = request.data['custom_code']
        code_v = f'''
def Custom():
    {custom_code}
'''

        try:
            compile(code_v, filename='<string>', mode='exec')
            return Response({'status': status.HTTP_200_OK, 'message':"custom code validated"},)
        except SyntaxError as err:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'SyntaxError: {err}'}, status=status.HTTP_400_BAD_REQUEST)  

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def Custom_Code_ValidateHashkey(request, user_hashkey):
    try:
        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            APICALLFUNCTION('Custom_Code_Validate', 'null')
            custom_code = request.data['custom_code']
            code_v = f'''
    def Custom():
        {custom_code}
    '''
    
            try:
                compile(code_v, filename='<string>', mode='exec')
                return Response({'status': status.HTTP_200_OK, 'message':"custom code validated"},)
            except SyntaxError as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'SyntaxError: {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)    
                    

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  




def ColumnListFunction(query_list, select_list, from_list):
    try:
        APICALLFUNCTION('ColumnListFunction', 'null')
        # column information
        ColumnList = []
        for p in range(select_list, from_list, 1):
            ColumnList.append(query_list[p].replace(',', ''))
        return ColumnList   
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)      

def ConditionListFunction(query_list, where_list, orderby_list):
    try:
        APICALLFUNCTION('ConditionListFunction', 'null')
        # condition information
        ConditionList = []
        for t in range(where_list, orderby_list, 1):
            ConditionList.append(query_list[t].replace(',', ''))
        return ConditionList   
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)      


    

def JsonConvert(df):
    try:
        DataItem = []
        KeyItem = []
        sections={}
        for key, value in df.iteritems():
            KeyItem.append(key)


        for index, row in df.iterrows():

            for i in range(len(KeyItem)):
                sections[KeyItem[i]]= row[KeyItem[i]]
            if sections != "":
                DataItem.append(sections)
                sections={}

        return DataItem
        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)


    

def SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby):
    try:
        if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)!=0: 
            if [x for x in ConditionList if x == 'between'] and len(ConditionList) == 5:
                KeyName = ConditionList[0]
                start = ConditionList[2]
                end = ConditionList[4]
                if KeyName == "Date":
                    result = df.loc[(df[KeyName] < start) & (df[KeyName] > end)]
                else:
                    result = df.loc[(df[KeyName] > int(start)) & (df[KeyName] < int(end))]
                source = result.sort_values(by=orderby[0], ascending=False)
                df = source[ColumnList]
                return df.to_csv(index=False)
                # return df
                # data = JsonConvert(df)
                # return data
                
                    
        if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)==0: 
            if [x for x in ConditionList if x == 'between'] and len(ConditionList) == 5:
                KeyName = ConditionList[0]
                start = ConditionList[2]
                end = ConditionList[4]
                if KeyName == "Date":
                    result = df.loc[(df[KeyName] < start) & (df[KeyName] > end)]
                else:
                    result = df.loc[(df[KeyName] > int(start)) & (df[KeyName] < int(end))]
                df = result[ColumnList]
                return df.to_csv(index=False)
                # return df
                # data = JsonConvert(df)
                # return data
                
                    
        if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)!=0: 
            source = df.sort_values(by=orderby[0], ascending=False)
            df = source[ColumnList]
            return df.to_csv(index=False)
            # return df
            # data = JsonConvert(df)
            # return data
        
            
            
        if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)==0:
            df = df[ColumnList]
            return df.to_csv(index=False)
            # return df
            # data = JsonConvert(df)
            # return data

        
        

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def QueryJsonfileDataAPI(request):  
    try: 
        APICALLFUNCTION('QueryJsonfileDataAPI', 'null')
        # table information
        TableList = []
        # column information
        ColumnList = []
        # condition information
        ConditionList = []
        

        # select, from, where, order index store information
        select_list = []
        from_list = []
        where_list = []
        orderby_list = []
        orderby = []

        query = request.data['Query']
        json_file = request.data['json_file']
        query = query.replace('\t', '').replace('\n', '').replace('\r', '')
        query_list = list(query.split(" "))
        query_list = list(filter(None, query_list))

        for i in range(len(query_list)):
            if query_list[i] =="SELECT": 
                select_list.append(i)

            if query_list[i] =="FROM": 
                from_list.append(i)
                
            if query_list[i] =="WHERE": 
                where_list.append(i)
               
            if query_list[i] =="ORDER" and query_list[i+1] =="BY": 
                orderby.append(query_list[i+2])
                orderby_list.append(i)

        if len(query_list)!=0 and len(from_list)!=0 and len(where_list)!=0:
            for t in range(from_list[0]+1, where_list[0], 1):
                TableList.append(query_list[t].replace(',', ''))
        if len(query_list)!=0 and len(from_list)!=0 and len(where_list)==0:
            for t in range(from_list[0]+1, len(query_list), 1):
                TableList.append(query_list[t].replace(',', ''))
        
        if len(query_list)!=0 and len(select_list)!=0 and len(from_list)!=0:
            Column = ColumnListFunction(query_list, select_list[0]+1, from_list[0])
            for c in Column:
                ColumnList.append(c)

        if len(query_list)!=0 and len(where_list)!=0 and len(orderby_list)!=0:
            Condition = ConditionListFunction(query_list, where_list[0]+1, orderby_list[0])  
            for c in Condition:
                ConditionList.append(c)

        if len(query_list)!=0 and len(where_list)!=0 and len(orderby_list)==0:
            Condition = ConditionListFunction(query_list, where_list[0]+1, len(query_list))  
            for c in Condition:
                ConditionList.append(c)


                    

        if len(json_file)!=0:
            df = pd.DataFrame(json_file)
           
            if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)!=0:
                SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
               
            if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)==0:
                SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                
            if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)!=0:
                SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
               
            if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)==0:
                SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                
            return Response({'message':"success",'status': status.HTTP_200_OK, "data": SelectQueryData}) 
        else:
            fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{TableList[0]}'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                array_data = data['data']
                df = pd.DataFrame(array_data)

              
                if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)!=0:
                    SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                    
                if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)==0:
                    SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                  
                if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)!=0:
                    SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                   
                if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)==0:
                    SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                    
                return Response({'message':"success",'status': status.HTTP_200_OK, "data": SelectQueryData})

            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Json file is not found'}, status=status.HTTP_400_BAD_REQUEST)  
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)




          
@api_view(['POST'])
def QueryJsonfileDataAPIHashkey(request, user_hashkey):  
    try: 
        
        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            
            APICALLFUNCTION('QueryJsonfileDataAPI', 'null')
            # table information
            TableList = []
            # column information
            ColumnList = []
            # condition information
            ConditionList = []
            
    
            # select, from, where, order index store information
            select_list = []
            from_list = []
            where_list = []
            orderby_list = []
            orderby = []
    
            query = request.data['Query']
            json_file = request.data['json_file']
            query = query.replace('\t', '').replace('\n', '').replace('\r', '')
            query_list = list(query.split(" "))
            query_list = list(filter(None, query_list))
    
            for i in range(len(query_list)):
                if query_list[i] =="SELECT": 
                    select_list.append(i)
    
                if query_list[i] =="FROM": 
                    from_list.append(i)
                    
                if query_list[i] =="WHERE": 
                    where_list.append(i)
                   
                if query_list[i] =="ORDER" and query_list[i+1] =="BY": 
                    orderby.append(query_list[i+2])
                    orderby_list.append(i)
    
            if len(query_list)!=0 and len(from_list)!=0 and len(where_list)!=0:
                for t in range(from_list[0]+1, where_list[0], 1):
                    TableList.append(query_list[t].replace(',', ''))
            if len(query_list)!=0 and len(from_list)!=0 and len(where_list)==0:
                for t in range(from_list[0]+1, len(query_list), 1):
                    TableList.append(query_list[t].replace(',', ''))
            
            if len(query_list)!=0 and len(select_list)!=0 and len(from_list)!=0:
                Column = ColumnListFunction(query_list, select_list[0]+1, from_list[0])
                for c in Column:
                    ColumnList.append(c)
    
            if len(query_list)!=0 and len(where_list)!=0 and len(orderby_list)!=0:
                Condition = ConditionListFunction(query_list, where_list[0]+1, orderby_list[0])  
                for c in Condition:
                    ConditionList.append(c)
    
            if len(query_list)!=0 and len(where_list)!=0 and len(orderby_list)==0:
                Condition = ConditionListFunction(query_list, where_list[0]+1, len(query_list))  
                for c in Condition:
                    ConditionList.append(c)
    
    
                        
    
            if len(json_file)!=0:
                df = pd.DataFrame(json_file)
               
                if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)!=0:
                    SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                   
                if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)==0:
                    SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                    
                if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)!=0:
                    SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                   
                if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)==0:
                    SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                    
                return Response({'message':"success",'status': status.HTTP_200_OK, "data": SelectQueryData}) 
            else:
                fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{TableList[0]}'
                if os.path.isfile(fileName):
                    f = open(fileName)
                    data = json.load(f)
                    array_data = data['data']
                    df = pd.DataFrame(array_data)
    
                  
                    if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)!=0:
                        SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                        
                    if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)!=0 and len(orderby)==0:
                        SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                      
                    if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)!=0:
                        SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                       
                    if len(df)!=0 and len(TableList)!=0 and len(ColumnList)!=0 and len(ConditionList)==0 and len(orderby)==0:
                        SelectQueryData = SelectQueryFunction(df, TableList, ColumnList, ConditionList, orderby)
                        
                    return Response({'message':"success",'status': status.HTTP_200_OK, "data": SelectQueryData})
    
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Json file is not found'}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)    
                        
                    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)

          
        
        
        
sucessList = []
errorList = []

def DateFormatingConvert(timed):
    currenttimestamp = datetime.strptime(timed, "%b %d, %Y").timestamp()
    currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%d-%m-%Y')
    return currenttimedate


def WebScrappingfunction(Code, company_url):
    exec(Code)
    if len(errorList)!=0:
        ProcessLogFunction(gm, company_url, list(set(errorList)))
    else:
        ProcessLogFunction(gm, company_url) 




@api_view(['POST'])
def WebScrappingAPI(request):  
    try: 
        APICALLFUNCTION('WebScrappingAPI', 'null')
        code_table_data_id = request.data['code_table_data_id']
        company_table_data_id = request.data['company_table_data_id']
        data = Table_data_info.objects.get(table_data_id=code_table_data_id)  
        data_param = Table_data_info.objects.get(table_data_id=company_table_data_id)  
        Code= data.column_data  
        company_url=data_param.column_data
        WebScrappingfunction(Code, company_url)
        if len(sucessList)!=0:
            for m in sucessList[0]:
                return Response(eval(m)) 
        if len(errorList)!=0: 
            Response({'status': status.HTTP_400_BAD_REQUEST, 'message': list(set(errorList[0]))}, status=status.HTTP_400_BAD_REQUEST)   
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
 
 
@api_view(['POST'])
def WebScrappingAPIHashkey(request, user_hashkey):  
    try: 
        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            
            APICALLFUNCTION('WebScrappingAPI', 'null')
            code_table_data_id = request.data['code_table_data_id']
            company_table_data_id = request.data['company_table_data_id']
            data = Table_data_info.objects.get(table_data_id=code_table_data_id)  
            data_param = Table_data_info.objects.get(table_data_id=company_table_data_id)  
            Code= data.column_data  
            company_url=data_param.column_data
            WebScrappingfunction(Code, company_url)
            if len(sucessList)!=0:
                for m in sucessList[0]:
                    return Response(eval(m)) 
            if len(errorList)!=0: 
                Response({'status': status.HTTP_400_BAD_REQUEST, 'message': list(set(errorList[0]))}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)        
                
                
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
 


        
        

import logging

logger = logging.getLogger(__name__)
logger = logging.getLogger('django')
logger.debug('1157 Find result! logger')
print("1157 Find result! print")

 
 
  

logger = logging.getLogger(__name__)
logger = logging.getLogger('django')        
@api_view(['GET'])
def LoggerFileCall(request):
    try:
        logger.info('1362 Find result! logger')
        print("1363 Find result! print") 
        return Response({'message':"success"}) 
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        
        
        
# select query new start

def addSelectNew(data1):
    SList=[] 
    FList=[] 
    WList=[] 
    OList=[] 
    select_counter = 0
    from_counter = 0
    where_counter = 0
    order_counter = 0
    while data1.head is not None:
        
        data2 = data1.head.data
        data1.head = data1.head.next
       
        if data2 == "SELECT":
            select_counter+=1
         
        if data2 != "FROM" and from_counter == 0 and data2 != "SELECT" and select_counter !=0:
            SList.append(data2)
            select_counter+=1

        if data2 == "FROM":
            from_counter+=1
        if data2 != "WHERE" and where_counter == 0 and data2 != "FROM" and from_counter !=0 and data2 != "ORDER" and order_counter ==0:
            FList.append(data2)
            from_counter+=1

        if data2 == "WHERE":
            where_counter+=1
        if data2 != "WHERE" and where_counter !=0 and data2 != "ORDER" and order_counter ==0:
            WList.append(data2)
            where_counter+=1
        if data2 == "ORDER":
            order_counter+=1
        if data2 == "BY":
            order_counter+=1
        if data2 != "ORDER" and data2 != "BY" and order_counter !=0:
            OList.append(data2)
            where_counter+=1

    return SList, FList, WList, OList



@api_view(['POST'])
def ModelJsonQueryDataNewAPI(request):
    try:
        APICALLFUNCTION('ModelJsonQueryDataNewAPI', 'null')
        
        # table information
        TableList = []
        TableName=[]
        TableId = []
        # column information
        ColumnName = []
        TableColId = []
   

        query1 = Table_data_info.objects.get(table_data_id=51484)
        query=query1.column_data
        query = query.replace('\t', '').replace('\n', '').replace('\r', '')
        query_list = list(query.split(" "))
        query_list = list(filter(None, query_list))

        data1 = LinkedList()

        for i in reversed(range(len(query_list))):
            data1.push(query_list[i])

        SList, FList, WList, OList = addSelectNew(data1)    


        if len(FList)!=0:
            for p in range(len(FList)):
                try:
                    v_result = Validate(FList[p].replace(',', ''), p, '')
                    if v_result is True:
                        TableData = Table_info_dtl.objects.get(table_name=FList[p].replace(',', ''))
                        TableList.append(TableData.table_name)
                    else:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableName Error'}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as err:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableName Error or {err}'}, status=status.HTTP_400_BAD_REQUEST)


        

        if len(SList)!=0:
            for p in range(len(SList)):
                v_result = Validate(SList[p].replace(',', ''), p, '')
                if v_result is True:
                    TableColumn = SList[p].split('.')
                    if len(TableColumn) == 1:
                        for t in range(len(TableList)):
                            TableData = Table_info_dtl.objects.get(table_name=TableList[t])
                            
                            for tc in range(len(TableColumn)): 
                                try:
                                    TableColumnData = Table_col_info.objects.get(table_id=TableData.table_id, column_name=TableColumn[tc].replace(',', ''))
                                    TableName.append(TableData.table_name)
                                    TableId.append(TableColumnData.table_id)
                                    ColumnName.append(TableColumnData.column_name)
                                    TableColId.append(TableColumnData.table_col_id)
                                except Exception as err:
                                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableColumn Error or {err}'}, status=status.HTTP_400_BAD_REQUEST)            
                    if len(TableColumn) == 2:
                        for tc in range(len(TableColumn)): 
                            if tc == 0:
                                try:
                                    TableName.append(TableColumn[tc])
                                    TableData = Table_info_dtl.objects.get(table_name=TableColumn[tc])
                                    TableId.append(TableData.table_id)
                                except Exception as err:
                                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableName Error or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
                            if tc == 1: 
                                try:   
                                    ColumnName.append(TableColumn[tc].replace(',', ''))
                                    TableColumnData = Table_col_info.objects.get(table_id=TableData.table_id, column_name=TableColumn[tc].replace(',', '')) 
                                    TableColId.append(TableColumnData.table_col_id)    
                                except Exception as err:
                                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableColumn Error or {err}'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableColumn Error'}, status=status.HTTP_400_BAD_REQUEST)

        df1 = pd.DataFrame(columns=('T1', 'C1', 'O', 'T2', 'C2', 'V', 'LO')) 
        new_row={}
       
        WDic={'jlist':[],'clist':[]}

        def DWhere(wlist):
            if len(wlist) != 0:
                if len(wlist) == 3:
                    return WDic['clist'].append(wlist) 
                for count, value in enumerate(wlist):
                    if value == 'and':
                        JList=wlist[:count]
                        CList=wlist[count+1:]
                        if len(WDic['jlist'])==0:
                            WDic['jlist'].append(JList)
                        else:
                            WDic['clist'].append(JList)
                        return DWhere(CList)
        
        if len(WList) != 0:
            DWhere(WList)
            if len(WDic['jlist'])!=0:
                for jdata in WDic['jlist']:
                    for i in range(len(jdata)):
                        v_result = Validate(jdata[i], i, '')
                        if v_result is True:
                            wj_data = jdata[i].split(".")
                            if  i==0:
                                t_data = Table_info_dtl.objects.get(table_name=wj_data[0])
                                t_col = Table_col_info.objects.get(table_id=t_data.table_id, column_name=wj_data[1])
                                new_row['T1']=t_data.table_id 
                                new_row['C1']=t_col.table_col_id   
                            if i==1:
                                new_row['O']=wj_data[0]  
                            if i==2:
                                t_data = Table_info_dtl.objects.get(table_name=wj_data[0])
                                t_col = Table_col_info.objects.get(table_id=t_data.table_id, column_name=wj_data[1])
                                new_row['T2']=t_data.table_id 
                                new_row['C2']=t_col.table_col_id  
                        else:
                            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Joining Query Error'}, status=status.HTTP_400_BAD_REQUEST)
                    if len(new_row) != 0:
                        df1 = df1._append(new_row, ignore_index=True)
                        new_row={}

            if len(WDic['clist'])!=0:
                for cdata in WDic['clist']:
                    for i in range(len(cdata)):
                        v_result = Validate(cdata[i], i, 'clist')
                        if v_result is True:
                            if i==2:
                                new_row['V']=cdata[i]    
                            else:
                                wj_data = cdata[i].split(".")
                                if  i==0:
                                    t_data = Table_info_dtl.objects.get(table_name=wj_data[0])
                                    t_col = Table_col_info.objects.get(table_id=t_data.table_id, column_name=wj_data[1])
                                    new_row['T1']=t_data.table_id 
                                    new_row['C1']=t_col.table_col_id   
                                if i==1:
                                    new_row['O']=wj_data[0]
                        else:
                            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Condition Query Error'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    if len(new_row) != 0:
                        df1 = df1._append(new_row, ignore_index=True)
                        new_row={}

  

        data = {
            "TableName": TableName,
            "ColumnName": ColumnName,
            "TableId": TableId,
            "TableColId": TableColId,
        } 

        df = pd.DataFrame(data) 


        if len(ColumnName)!=0 and len(df)!=0 and len(df1)!=0 and len(OList)!=0:
            ModelSelectQueryData = ModelSelectQueryFunction(ColumnName, df, df1, OList)
        if len(ColumnName)!=0 and len(df)!=0 and len(df1)!=0 and len(OList)==0:
            ModelSelectQueryData = ModelSelectQueryFunction(ColumnName, df, df1, OList)
        if len(ColumnName)!=0 and len(df)!=0 and len(df1)==0 and len(OList)!=0:
            ModelSelectQueryData = ModelSelectQueryFunction(ColumnName, df, df1, OList)
        if len(ColumnName)!=0 and len(df)!=0 and len(df1)==0 and len(OList)==0:
            ModelSelectQueryData = ModelSelectQueryFunction(ColumnName, df, df1, OList)
        
        
        # return Response({'message':"success",'status': status.HTTP_200_OK, "data": [{'a':20, 'b':10},{'c':10, 'd':30}]})
        # return Response({'message':"success",'status': status.HTTP_200_OK, "data": ModelSelectQueryData})
        # return Response(ModelSelectQueryData)
        ListDic = {'data':[]}
        for m in ModelSelectQueryData:
            ListDic['data'].append(m)
                
        # return Response(ListDic)
        response = Response(
            data=ListDic,
            status=status.HTTP_200_OK
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response 
            
            
            

            

        # try:
        #     result = JsonDataSerializer({'data':[{'a':10, 'b':20},{'c':30, 'd': 40}]})
        #     return Response({'message':"success",'status': status.HTTP_200_OK, "data": result})
        #     # return Response({'message':"success",'status': status.HTTP_200_OK, "data": ModelSelectQueryData}) 
        # except Exception as err:
        #     return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)   
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 





@api_view(['POST'])
def ModelJsonQueryDataNewAPIHashkey(request, user_hashkey):
    try:
        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            APICALLFUNCTION('ModelJsonQueryDataNewAPI', 'null')
            
            # table information
            TableList = []
            TableName=[]
            TableId = []
            # column information
            ColumnName = []
            TableColId = []
       
    
            query1 = Table_data_info.objects.get(table_data_id=51484)
            query=query1.column_data
            query = query.replace('\t', '').replace('\n', '').replace('\r', '')
            query_list = list(query.split(" "))
            query_list = list(filter(None, query_list))
    
            data1 = LinkedList()
    
            for i in reversed(range(len(query_list))):
                data1.push(query_list[i])
    
            SList, FList, WList, OList = addSelectNew(data1)    
    
    
            if len(FList)!=0:
                for p in range(len(FList)):
                    try:
                        v_result = Validate(FList[p].replace(',', ''), p, '')
                        if v_result is True:
                            TableData = Table_info_dtl.objects.get(table_name=FList[p].replace(',', ''))
                            TableList.append(TableData.table_name)
                        else:
                            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableName Error'}, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as err:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableName Error or {err}'}, status=status.HTTP_400_BAD_REQUEST)
    
    
            
    
            if len(SList)!=0:
                for p in range(len(SList)):
                    v_result = Validate(SList[p].replace(',', ''), p, '')
                    if v_result is True:
                        TableColumn = SList[p].split('.')
                        if len(TableColumn) == 1:
                            for t in range(len(TableList)):
                                TableData = Table_info_dtl.objects.get(table_name=TableList[t])
                                
                                for tc in range(len(TableColumn)): 
                                    try:
                                        TableColumnData = Table_col_info.objects.get(table_id=TableData.table_id, column_name=TableColumn[tc].replace(',', ''))
                                        TableName.append(TableData.table_name)
                                        TableId.append(TableColumnData.table_id)
                                        ColumnName.append(TableColumnData.column_name)
                                        TableColId.append(TableColumnData.table_col_id)
                                    except Exception as err:
                                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableColumn Error or {err}'}, status=status.HTTP_400_BAD_REQUEST)            
                        if len(TableColumn) == 2:
                            for tc in range(len(TableColumn)): 
                                if tc == 0:
                                    try:
                                        TableName.append(TableColumn[tc])
                                        TableData = Table_info_dtl.objects.get(table_name=TableColumn[tc])
                                        TableId.append(TableData.table_id)
                                    except Exception as err:
                                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableName Error or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
                                if tc == 1: 
                                    try:   
                                        ColumnName.append(TableColumn[tc].replace(',', ''))
                                        TableColumnData = Table_col_info.objects.get(table_id=TableData.table_id, column_name=TableColumn[tc].replace(',', '')) 
                                        TableColId.append(TableColumnData.table_col_id)    
                                    except Exception as err:
                                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableColumn Error or {err}'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'TableColumn Error'}, status=status.HTTP_400_BAD_REQUEST)
    
            df1 = pd.DataFrame(columns=('T1', 'C1', 'O', 'T2', 'C2', 'V', 'LO')) 
            new_row={}
           
            WDic={'jlist':[],'clist':[]}
    
            def DWhere(wlist):
                if len(wlist) != 0:
                    if len(wlist) == 3:
                        return WDic['clist'].append(wlist) 
                    for count, value in enumerate(wlist):
                        if value == 'and':
                            JList=wlist[:count]
                            CList=wlist[count+1:]
                            if len(WDic['jlist'])==0:
                                WDic['jlist'].append(JList)
                            else:
                                WDic['clist'].append(JList)
                            return DWhere(CList)
            
            if len(WList) != 0:
                DWhere(WList)
                if len(WDic['jlist'])!=0:
                    for jdata in WDic['jlist']:
                        for i in range(len(jdata)):
                            v_result = Validate(jdata[i], i, '')
                            if v_result is True:
                                wj_data = jdata[i].split(".")
                                if  i==0:
                                    t_data = Table_info_dtl.objects.get(table_name=wj_data[0])
                                    t_col = Table_col_info.objects.get(table_id=t_data.table_id, column_name=wj_data[1])
                                    new_row['T1']=t_data.table_id 
                                    new_row['C1']=t_col.table_col_id   
                                if i==1:
                                    new_row['O']=wj_data[0]  
                                if i==2:
                                    t_data = Table_info_dtl.objects.get(table_name=wj_data[0])
                                    t_col = Table_col_info.objects.get(table_id=t_data.table_id, column_name=wj_data[1])
                                    new_row['T2']=t_data.table_id 
                                    new_row['C2']=t_col.table_col_id  
                            else:
                                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Joining Query Error'}, status=status.HTTP_400_BAD_REQUEST)
                        if len(new_row) != 0:
                            df1 = df1._append(new_row, ignore_index=True)
                            new_row={}
    
                if len(WDic['clist'])!=0:
                    for cdata in WDic['clist']:
                        for i in range(len(cdata)):
                            v_result = Validate(cdata[i], i, 'clist')
                            if v_result is True:
                                if i==2:
                                    new_row['V']=cdata[i]    
                                else:
                                    wj_data = cdata[i].split(".")
                                    if  i==0:
                                        t_data = Table_info_dtl.objects.get(table_name=wj_data[0])
                                        t_col = Table_col_info.objects.get(table_id=t_data.table_id, column_name=wj_data[1])
                                        new_row['T1']=t_data.table_id 
                                        new_row['C1']=t_col.table_col_id   
                                    if i==1:
                                        new_row['O']=wj_data[0]
                            else:
                                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Condition Query Error'}, status=status.HTTP_400_BAD_REQUEST)
                        
                        if len(new_row) != 0:
                            df1 = df1._append(new_row, ignore_index=True)
                            new_row={}
    
      
    
            data = {
                "TableName": TableName,
                "ColumnName": ColumnName,
                "TableId": TableId,
                "TableColId": TableColId,
            } 
    
            df = pd.DataFrame(data) 
    
    
            if len(ColumnName)!=0 and len(df)!=0 and len(df1)!=0 and len(OList)!=0:
                ModelSelectQueryData = ModelSelectQueryFunction(ColumnName, df, df1, OList)
            if len(ColumnName)!=0 and len(df)!=0 and len(df1)!=0 and len(OList)==0:
                ModelSelectQueryData = ModelSelectQueryFunction(ColumnName, df, df1, OList)
            if len(ColumnName)!=0 and len(df)!=0 and len(df1)==0 and len(OList)!=0:
                ModelSelectQueryData = ModelSelectQueryFunction(ColumnName, df, df1, OList)
            if len(ColumnName)!=0 and len(df)!=0 and len(df1)==0 and len(OList)==0:
                ModelSelectQueryData = ModelSelectQueryFunction(ColumnName, df, df1, OList)
            
            
            # return Response({'message':"success",'status': status.HTTP_200_OK, "data": [{'a':20, 'b':10},{'c':10, 'd':30}]})
            # return Response({'message':"success",'status': status.HTTP_200_OK, "data": ModelSelectQueryData})
            # return Response(ModelSelectQueryData)
            ListDic = {'data':[]}
            for m in ModelSelectQueryData:
                ListDic['data'].append(m)
                    
            # return Response(ListDic)
            response = Response(
                data=ListDic,
                status=status.HTTP_200_OK
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response 
            
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)       
  
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 






# select query new end        


@api_view(['GET'])
def GETTABLEDYNAMICFIELDAPI(request, table_id):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('GETTABLEDYNAMICFIELDAPI', 'null')
        sections = {}
        items = []
        refId = []
        table_data = Table_data_info.objects.filter(table_id=table_id).order_by('-table_ref_id')
        for k in table_data:
            refId.append(k.table_ref_id)
                   
        refId = list(set(refId))
        # print("303", refId)

        for m in refId:
            for i in table_data:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_id']=i.table_id
                    sections['table_ref_id']=i.table_ref_id
            if sections != "":
                items.append(sections)   
                sections = {}     
                
    
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(items)
        DataFetch_Static("GETTABLEDYNAMICFIELDAPI", "Model Data", value_count, round(loadTime, 6))
        
        return Response({'message':'success','status': status.HTTP_200_OK, 'data': items},)

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


        
@api_view(['GET'])
def GETTABLEDYNAMICFIELDAPIHashkey(request, table_id, user_hashkey):
    try:
        startTime = CurrentTimeFunc()
        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            APICALLFUNCTION('GETTABLEDYNAMICFIELDAPI', 'null')
            sections = {}
            items = []
            refId = []
            table_data = Table_data_info.objects.filter(table_id=table_id).order_by('-table_ref_id')
            for k in table_data:
                refId.append(k.table_ref_id)
                       
            refId = list(set(refId))
            print("303", refId)
    
            for m in refId:
                for i in table_data:
                    if i.table_ref_id==m:
                        sections[i.column_name]=i.column_data
                        sections['table_id']=i.table_id
                        sections['table_ref_id']=i.table_ref_id
                if sections != "":
                    items.append(sections)   
                    sections = {}     
                    
        
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("GETTABLEDYNAMICFIELDAPI", "Model Data", value_count, round(loadTime, 6))
            
            return Response({'message':'success','status': status.HTTP_200_OK, 'data': items},)
            
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)       

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
@api_view(['GET'])
def GETTABLEDYNAMICFIELDUSERAPI(request, table_id, user_id):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('GETTABLEDYNAMICFIELDUSERAPI', 'null')
        sections = {}
        items = []
        refId = []
        table_data = Table_data_info.objects.filter(table_id=table_id, user_id=user_id).order_by('-table_ref_id')
        for k in table_data:
            refId.append(k.table_ref_id)
                   
        refId = list(set(refId))
        print("303", refId)

        for m in refId:
            for i in table_data:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_id']=i.table_id
                    sections['table_ref_id']=i.table_ref_id
            if sections != "":
                items.append(sections)   
                sections = {}    
                
                
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(items)
        DataFetch_Static("GETTABLEDYNAMICFIELDUSERAPI", "Model Data", value_count, round(loadTime, 6))
                
        return Response({'message':'success','status': status.HTTP_200_OK, 'data': items},)

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
                
    
        
@api_view(['GET'])
def GETTABLEDYNAMICFIELDUSERAPIHashkey(request, table_id, user_id, user_hashkey):
    try:
        startTime = CurrentTimeFunc()
        validate = HashKeyValidateFunc(user_hashkey)
        if validate == True:
            APICALLFUNCTION('GETTABLEDYNAMICFIELDUSERAPIHashkey', 'null')
            sections = {}
            items = []
            refId = []
            table_data = Table_data_info.objects.filter(table_id=table_id, user_id=user_id).order_by('-table_ref_id')
            for k in table_data:
                refId.append(k.table_ref_id)
                       
            refId = list(set(refId))
            print("303", refId)
    
            for m in refId:
                for i in table_data:
                    if i.table_ref_id==m:
                        sections[i.column_name]=i.column_data
                        sections['table_id']=i.table_id
                        sections['table_ref_id']=i.table_ref_id
                if sections != "":
                    items.append(sections)   
                    sections = {}    
                    
                    
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(items)
            DataFetch_Static("GETTABLEDYNAMICFIELDUSERAPIHashkey", "Model Data", value_count, round(loadTime, 6))
                    
            return Response({'message':'success','status': status.HTTP_200_OK, 'data': items},)
            
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message':f'User is not valid'}, status=status.HTTP_401_UNAUTHORIZED)       

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
                
        
        
@api_view(['GET'])
def RuleValidateFrontendAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('RuleValidateFrontendAPI', 'null')
        ProcessLogFunction(process_id="", log_date="", log_output_file="", log_data_type="table_name before", log_process_name=request.data, error="")
        table_name = request.data['table_name']
        ProcessLogFunction(process_id="", log_date="", log_output_file="", log_data_type="table_name", log_process_name=table_name, error="")
        column_name = request.data['column_name']
        operator = request.data['operator']
        value = request.data['value']
        
        if operator == 'is not NULL' or operator == 'is not null':
            result = IsNotNullFunctionRuleValidate(table_name, column_name, operator, value)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(result)
            DataFetch_Static("RuleValidateFrontendAPI", "IsNotNullFunctionRuleValidate function", value_count, round(loadTime, 6))
            
            return Response({'message':'success', 'validate': result, 'status': status.HTTP_200_OK})

        if operator == 'is unique' or operator == 'is UNIQUE':
            result = IsUniqueFunctionRuleValidate(table_name, column_name, operator, value)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(result)
            DataFetch_Static("RuleValidateFrontendAPI", "IsUniqueFunctionRuleValidate function", value_count, round(loadTime, 6))
            
            return Response({'message':'success', 'validate': result, 'status': status.HTTP_200_OK})
        else:
            return Response({'message':'operator is not found please valid operator', 'status': status.HTTP_200_OK})    

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ValueValidateFrontendAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('ValueValidateFrontendAPI', 'null')
        table_name = request.data['table_name']
        column_name = request.data['column_name']
        column_value = request.data['column_value']
        operator = request.data['operator']
        value = request.data['value']
        
        
        if operator == 'is not NULL' or operator == 'is not null':
            result = IsNotNullFunctionValueValidate(table_name, column_name, column_value, operator, value)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(result)
            DataFetch_Static("ValueValidateFrontendAPI", "IsNotNullFunctionValueValidate function", value_count, round(loadTime, 6))
            
            return Response({'message':'success', 'validate': result, 'status': status.HTTP_200_OK})

        if operator == 'is unique' or operator == 'is UNIQUE':
            result = IsUniqueFunctionValueValidate(table_name, column_name, column_value, operator, value)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(result)
            DataFetch_Static("ValueValidateFrontendAPI", "IsUniqueFunctionValueValidate function", value_count, round(loadTime, 6))
            
            return Response({'message':'success', 'validate': result, 'status': status.HTTP_200_OK})
        
        if operator == 'contains' or operator == 'CONTAINS':
            result = ContainsFunctionValueValidate(table_name, column_name, column_value, operator, value)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(result)
            DataFetch_Static("ValueValidateFrontendAPI", "ContainsFunctionValueValidate function", value_count, round(loadTime, 6))
            
            return Response({'message':'success', 'validate': result, 'status': status.HTTP_200_OK})
        else:
            return Response({'message':'operator is not found please valid operator', 'status': status.HTTP_200_OK})    
       
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
        
        
def DateValidate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


@api_view(['POST'])
def TableFilterDataApi(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('TableFilterDataApi', 'null')
        sql_data = request.data['sql_data']
        table_column = request.data['table_column']
        column_name = request.data['column_name']
        search_text = request.data['search_text']
        v_check = DateValidate(search_text)
       
        DataItem = []
        for i in table_column:
            print(i)
            # if i == column_name:
            if v_check == True:
                data = [x for x in sql_data if x[i] == search_text]
                if len(data) != 0:
                    for m in data:
                        DataItem.append(m)
            # if i == column_name:                
            if v_check == False:
                data = [x for x in sql_data if x[i] == float(search_text)]
                if len(data) != 0:
                    for m in data:
                        DataItem.append(m)

           
        Item = []                
        for k in DataItem:
            Item.append(k.values())
            
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(Item)
        DataFetch_Static("TableFilterDataApi", "Model Filter function", value_count, round(loadTime, 6))    
            
        return Response({'data': Item,'status': status.HTTP_200_OK})        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
@api_view(['POST'])
def TableSortDataApi(request):
    try:
        startTime = CurrentTimeFunc()

        APICALLFUNCTION('TableSortDataApi', 'null')
        sql_data = request.data['sql_data']
        column_name = request.data['column_name']

        sorted_data = sorted(sql_data, key=lambda x: x[column_name])

        Item = []                
        for k in sorted_data:
            Item.append(k.values())
            
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(Item)
        DataFetch_Static("TableSortDataApi", "Table Sort function", value_count, round(loadTime, 6))    
        
        return Response({'data': Item,'status': status.HTTP_200_OK})        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)
        
        


def ModelFormulaCheckStart(formula):
    try:
        formula_name_info = Table_data_info.objects.get(table_id=555, column_data=formula)

        formula_set = Table_data_info.objects.get(table_id=555, table_col_id=1, table_ref_id=formula_name_info.table_ref_id)
        formula_data = eval(formula_set.column_data)
       
        return formula_data
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)     
 


def FormulaValueCheckStart(formula):
    try:
        formula_name_info = Table_data_info.objects.filter(table_id=555, column_data=formula)

        if len(formula_name_info)!=0:
            return True
        return False
    except:
        return False  

def ColumnCheckStart(df, column):
    try:
        KeyItem = []
        for key, value in df.iteritems():
            KeyItem.append(key)
        for i in KeyItem:
            if i == column:
                return True
        return False    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
            

    
def FormulaCalculationFunctionStart(formula_name):
    try:
        formula_data = ModelFormulaCheckStart(formula_name)
        fileName = formula_data['fileName']

        f = open(main_media_url+f'/media/upload_file/yahoo_finance_hist/{fileName}')
        data = json.load(f)
        f_data = data['data']

        pdData = pd.DataFrame(f_data)

        
        for i in  range(int(len(formula_data['formulaKey'])/3)):
            col1 = f'a_colA{i+1}'
            op = f'a_op{i+1}'
            col2 = f'a_colB{i+1}'
            col1_check = ColumnCheckStart(pdData, formula_data['formulaKey'][col1])
            col2_check = ColumnCheckStart(pdData, formula_data['formulaKey'][col2])

            keyValue1 = f'resultValue{i+1}'


            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '+':
                pdData['result'] = pdData[formula_data['formulaKey'][col1]] + pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '+' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] + pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == False and formula_data['formulaKey'][op] == '+' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] + pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '+' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] + int(formula_data['formulaKey'][col2])
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '/':
                pdData['result'] = pdData['result'] / int(formula_data['formulaKey'][col2])     

               
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '-':
                pdData['result'] = pdData[formula_data['formulaKey'][col1]] - pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '-' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] - pdData[formula_data['formulaKey'][col2]]    
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '-' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] - pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == False and formula_data['formulaKey'][op] == '-' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] - pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '-':
                pdData['result'] = pdData['result'] - int(formula_data['formulaKey'][col2])     
          


            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '*':
                pdData['result'] = pdData[formula_data['formulaKey'][col1]] * pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '*' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] * pdData[formula_data['formulaKey'][col2]]    
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '*' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] * pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == True and formula_data['formulaKey'][op] == '*' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] * pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '*':
                pdData['result'] = pdData['result'] * int(formula_data['formulaKey'][col2])     
          

            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '/':
                pdData['result'] = pdData[formula_data['formulaKey'][col1]] / pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '/' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] / pdData[formula_data['formulaKey'][col2]]    
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '/' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] / pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == True and formula_data['formulaKey'][op] == '/' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] / pdData[formula_data['formulaKey'][col2]] 
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '/':
                pdData['result'] = pdData['result'] / int(formula_data['formulaKey'][col2]) 
                

      
        return pdData.T.tail(1).T

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)     


    


@api_view(['POST'])
def FormulaCalculationAPIView(request):
    try:
        startTime = CurrentTimeFunc()
        
        APICALLFUNCTION('FormulaCalculationAPIView', 'null')
        formula = request.data['formula']
        ProcessLogFunction(process_id="", log_date="", log_output_file="formula 1", log_data_type="", log_process_name=formula, error="")
        # pData = FormulaCalculationStart(formula)
        # ProcessLogFunction(process_id="", log_date="", log_output_file="formula 2", log_data_type="", log_process_name=str(pData), error="")
        formula_name_info = Table_data_info.objects.get(table_id=555, column_data=formula)
        formula_set = Table_data_info.objects.get(table_id=555, table_col_id=1, table_ref_id=formula_name_info.table_ref_id)
        ProcessLogFunction(process_id="", log_date="", log_output_file="formula 2", log_data_type="", log_process_name=str(formula_set), error="")
        formula_data = eval(formula_set.column_data)
        fileName = formula_data['fileName']
        
        ProcessLogFunction(process_id="", log_date="", log_output_file="formula 2", log_data_type="", log_process_name=str(fileName), error="")

        f = open(main_media_url+f'/media/upload_file/yahoo_finance_hist/{fileName}')
        data = json.load(f)
        f_data = data['data']
        ProcessLogFunction(process_id="", log_date="", log_output_file="formula 3", log_data_type="", log_process_name=str(f_data), error="")

        pdData = pd.DataFrame(f_data)
        
        ProcessLogFunction(process_id="", log_date="", log_output_file="formula 4", log_data_type="", log_process_name=str(pdData), error="")

       
        for i in  range(int(len(formula_data['formulaKey'])/3)):
            col1 = f'a_colA{i+1}'
            op = f'a_op{i+1}'
            col2 = f'a_colB{i+1}'
            col1_check = ColumnCheckStart(pdData, formula_data['formulaKey'][col1])
            col2_check = ColumnCheckStart(pdData, formula_data['formulaKey'][col2])

            keyValue1 = f'resultValue{i+1}'

            if col1_check == False:
                formula_value_check_result = FormulaValueCheckStart(formula_data['formulaKey'][col1])
                if formula_value_check_result == True:
                    df2 = FormulaCalculationFunctionStart(formula_data['formulaKey'][col1])
                    pdData['result'] = df2
                   


            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '+':
                pdData['result'] = pdData[formula_data['formulaKey'][col1]] + pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '+' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] + pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == False and formula_data['formulaKey'][op] == '+' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] + pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '+' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] + int(formula_data['formulaKey'][col2])
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '+':
                pdData['result'] = pdData['result'] + int(formula_data['formulaKey'][col2])

               
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '-':
                pdData['result'] = pdData[formula_data['formulaKey'][col1]] - pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '-' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] - pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == False and formula_data['formulaKey'][op] == '-' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] - pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '-':
                pdData['result'] = pdData['result'] - int(formula_data['formulaKey'][col2])    
           
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '*':
                pdData['result'] = pdData[formula_data['formulaKey'][col1]] * pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '*' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] * pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == True and formula_data['formulaKey'][op] == '*' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] * pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '*':
                pdData['result'] = pdData['result'] * int(formula_data['formulaKey'][col2])    
           
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '/':
                pdData['result'] = pdData[formula_data['formulaKey'][col1]] / pdData[formula_data['formulaKey'][col2]]
            if col1_check == True and col2_check == True and formula_data['formulaKey'][op] == '/' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] / pdData[formula_data['formulaKey'][col2]]
            if col1_check == False and col2_check == True and formula_data['formulaKey'][op] == '/' and formula_data['formulaKey'][col1] == f'result{i}':
                pdData['result'] = pdData['result'] / pdData[formula_data['formulaKey'][col2]] 
            if col1_check == False and col2_check == False and formula_data['formulaKey'][op] == '/':
                pdData['result'] = pdData['result'] / int(formula_data['formulaKey'][col2])
                
        pdata = pdData.to_dict('records')   
        # pdata = pData.to_csv(index=False) 
        
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(pdata)
        DataFetch_Static("FormulaCalculationAPIView", "Json FormulaCalculation", value_count, round(loadTime, 6)) 
        
        return Response({'status': status.HTTP_200_OK, 'data':pdata})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 

        
                
@api_view(['GET'])
def GETTABLEDYNAMICFIELDFLOWAPI(request, table_id, flow_name):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('GETTABLEDYNAMICFIELDFLOWAPI', 'null')
        items = []
        flow_data = Table_data_info.objects.get(table_id=table_id, column_data=flow_name)
        flow_data_ref = Table_data_info.objects.filter(table_id=table_id, table_ref_id=flow_data.table_ref_id)
        for m in flow_data_ref:
            if m.table_col_id == 1:
                items = eval(m.column_data)
                
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(items)
        DataFetch_Static("GETTABLEDYNAMICFIELDFLOWAPI", "Table_data_info model data", value_count, round(loadTime, 6))         
           
        return Response({'message':'success','status': status.HTTP_200_OK, 'data': items},)

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  

                        

            

def FilterFunction(hist_data, filterKey, filterCon, filterConValue):
    try:
        if filterCon == "E":
            try:
                filter_data = [x for x in hist_data if x[filterKey] == filterConValue]
                return filter_data
            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        if filterCon == "C":
            try:
                filter_data = [x for x in hist_data if x[filterKey].find(filterConValue) != -1]
                return filter_data
            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    

        if filterCon == ">":
            try:
                if filterKey == "Date":
                    filter_data = [x for x in hist_data if datetime.strptime(x[filterKey], "%Y-%m-%d").timestamp() > datetime.strptime(filterConValue, "%Y-%m-%d").timestamp()]
                    return filter_data
                else:
                    filter_data = [x for x in hist_data if int(x[filterKey]) > int(filterConValue)]
                    return filter_data

            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        
        if filterCon == "<":
            try:
                if filterKey == "Date":
                    filter_data = [x for x in hist_data if datetime.strptime(x[filterKey], "%Y-%m-%d").timestamp() < datetime.strptime(filterConValue, "%Y-%m-%d").timestamp()]
                    return filter_data
                else:
                    filter_data = [x for x in hist_data if int(x[filterKey]) < int(filterConValue)]
                    return filter_data

            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        
        if filterCon == ">=":
            try:
                if filterKey == "Date":
                    filter_data = [x for x in hist_data if datetime.strptime(x[filterKey], "%Y-%m-%d").timestamp() >= datetime.strptime(filterConValue, "%Y-%m-%d").timestamp()]
                    return filter_data
                else:
                    filter_data = [x for x in hist_data if int(x[filterKey]) >= int(filterConValue)]
                    return filter_data

            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        
        if filterCon == "<=":
            try:
                if filterKey == "Date":
                    filter_data = [x for x in hist_data if datetime.strptime(x[filterKey], "%Y-%m-%d").timestamp() <= datetime.strptime(filterConValue, "%Y-%m-%d").timestamp()]
                    return filter_data
                else:
                    filter_data = [x for x in hist_data if int(x[filterKey]) <= int(filterConValue)]
                    return filter_data

            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    


    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      


@api_view(['POST'])
def JsonFilterDataAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('JsonFilterDataAPI', 'null')
        MergeData= []
        SeparateData= []
        data_object = {}
        items = []
        sl = request.data['sl']
        stepType = request.data['stepType']
        sourceType = request.data['sourceType']
        sourceInfoType = request.data['sourceInfoType']
        source = request.data['source']
        filterKey = request.data['filterKey']
        filterCon = request.data['filterCon']
        filterConValue = request.data['filterConValue']


        if stepType == "filter" and sourceType == "filter data" and sourceInfoType == "json data":
            if len(source) != 0:
                for s in source:
                    fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{s}'
                    if os.path.isfile(fileName):
                        f = open(fileName)
                        data = json.load(f)
                        hist_data = data['data']
                        if filterKey and filterCon and filterConValue:
                            data_filter = FilterFunction(hist_data, filterKey, filterCon, filterConValue)

                            data_object[s] = data_filter
                            if len(data_object) != 0:
                                SeparateData.append(data_object)
                                data_object= {}
                            for d in data_filter:
                                MergeData.append(d)
                        else:
                            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'filterKey and filterCon and filterConValue are not found'}, status=status.HTTP_400_BAD_REQUEST)   
                    else:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{s} filename is not found'}, status=status.HTTP_400_BAD_REQUEST)   
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'source json filename not found'}, status=status.HTTP_400_BAD_REQUEST)   
        else:   
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'stepType type filter and sourceInfoType json data not found'}, status=status.HTTP_400_BAD_REQUEST)   
      
        
        
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(SeparateData)
        DataFetch_Static("JsonFilterDataAPI", "json filter data", value_count, round(loadTime, 6))
           
        return Response({'message':'success','status': status.HTTP_200_OK, 'MergeData': MergeData, "data": SeparateData})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
@api_view(['POST'])
def LineChartDataAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('LineChartDataAPI', 'null')
        Data= []
        Data1= []
       
        fdata = request.data['fdata']

        for i in fdata:
            print(i)
            Data1.append(i['Date'])
            Data1.append(i['Open'])
            if len(Data1) != 0:
                Data.append(Data1)
                Data1 = []

            Data1.append(i['Date'])
            Data1.append(i['High'])
            if len(Data1) != 0:
                Data.append(Data1)
                Data1 = []

            Data1.append(i['Date'])
            Data1.append(i['Low'])
            if len(Data1) != 0:
                Data.append(Data1)
                Data1 = []

            Data1.append(i['Date'])
            Data1.append(i['Close'])
            if len(Data1) != 0:
                Data.append(Data1)
                Data1 = []

            Data1.append(i['Date'])
            Data1.append(i['Volume'])
            if len(Data1) != 0:
                Data.append(Data1)
                Data1 = []

            Data1.append(i['Date'])
            Data1.append(i['Dividends'])
            if len(Data1) != 0:
                Data.append(Data1)
                Data1 = []

            Data1.append(i['Date'])
            Data1.append(i['Stock Splits'])
            if len(Data1) != 0:
                Data.append(Data1)
                Data1 = []

        
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(Data)
        DataFetch_Static("LineChartDataAPI", "json filter data", value_count, round(loadTime, 6))
        
        return Response({'message':'success','status': status.HTTP_200_OK,"data": Data})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
        


def SourceFunction(source):
    try:
        
        sourceData = []
        data_object = {}
        for s in source:
            fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{s}'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                hist_data = data['data']
                data_object[s] = hist_data
                if len(data_object) != 0:
                    sourceData.append(data_object)
                    data_object= {}
                    
            fileName = main_media_url+f'/media/upload_file/json/{s}'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                hist_data = data['data']
                data_object[s] = hist_data
                if len(data_object) != 0:
                    sourceData.append(data_object)
                    data_object= {}
                    
            fileName = main_media_url+f'/media/upload_file/investing/json/{s}'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                hist_data = data['data']
                data_object[s] = hist_data
                if len(data_object) != 0:
                    sourceData.append(data_object)
                    data_object= {}

        return sourceData

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  



def extract_multiple_keys(data, keys):
    extracted_values = {}
    for key in keys:
        if key in data:
            extracted_values[key] = data[key]

    return extracted_values

def SourceFunctionFinal(source, sourceKey):
    try:
        DataItem = []
        sections={}
        for s in source:
            fileName = main_media_url+f'/media/upload_file/yahoo_finance_hist/{s}'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                hist_data = data['data']
                for hdata in hist_data:
                    hdata['fileKey'] = s
                    sourceKey.append('fileKey')
                    sourceKey=list(set(sourceKey))
                    DataItem.append(extract_multiple_keys(hdata, sourceKey))
               
                    
            fileName = main_media_url+f'/media/upload_file/json/{s}'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                hist_data = data['data']
                for hdata in hist_data:
                    hdata['fileKey'] = s
                    sourceKey.append('fileKey')
                    sourceKey=list(set(sourceKey))
                    DataItem.append(extract_multiple_keys(hdata, sourceKey))
                    
            fileName = main_media_url+f'/media/upload_file/investing/json/{s}'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                hist_data = data['data']
                for hdata in hist_data:
                    hdata['fileKey'] = s
                    sourceKey.append('fileKey')
                    sourceKey=list(set(sourceKey))
                    DataItem.append(extract_multiple_keys(hdata, sourceKey))

        return DataItem

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
    

def FilterFunctionFlowChart(source, sourceData, filterKey, filterCon, filterConValue):
    try:
       
        sourceData1 = []
        data_object1 = {}  

        for s in source:
            print("s", s)
            for x in sourceData:
   
                for k in x.keys():
                    if k == s:
                        fData = FilterConditionFlowChartFunction(x[s], filterKey, filterCon, filterConValue)
                        data_object1[s] = fData
                        if len(data_object1) != 0:
                            sourceData1.append(data_object1)
                            data_object1= {}
               
                            
        return sourceData1                    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


def FilterFunctionFlowChartFinal(sourceData, filterKey, filterCon, filterConValue):
    try:
        return FilterConditionFlowChartFunction(sourceData, filterKey, filterCon, filterConValue)                   
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  



def FilterConditionFlowChartFunction(hist_data, filterKey, filterCon, filterConValue):
    try:
        if filterCon == "E":
            try:
                filter_data = [x for x in hist_data if x[filterKey] == filterConValue]
                return filter_data
            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        if filterCon == "C":
            try:
                filter_data = [x for x in hist_data if x[filterKey].find(filterConValue) != -1]
                return filter_data
            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    

        if filterCon == ">":
            try:
                if filterKey == "Date":
                    filter_data = [x for x in hist_data if datetime.strptime(x[filterKey], "%Y-%m-%d").timestamp() > datetime.strptime(filterConValue, "%Y-%m-%d").timestamp()]
                    return filter_data
                else:
                    filter_data = [x for x in hist_data if int(x[filterKey]) > int(filterConValue)]
                    return filter_data

            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        
        if filterCon == "<":
            try:
                if filterKey == "Date":
                    filter_data = [x for x in hist_data if datetime.strptime(x[filterKey], "%Y-%m-%d").timestamp() < datetime.strptime(filterConValue, "%Y-%m-%d").timestamp()]
                    return filter_data
                else:
                    filter_data = [x for x in hist_data if int(x[filterKey]) < int(filterConValue)]
                    return filter_data

            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        
        if filterCon == ">=":
            try:
                if filterKey == "Date":
                    filter_data = [x for x in hist_data if datetime.strptime(x[filterKey], "%Y-%m-%d").timestamp() >= datetime.strptime(filterConValue, "%Y-%m-%d").timestamp()]
                    return filter_data
                else:
                    filter_data = [x for x in hist_data if int(x[filterKey]) >= int(filterConValue)]
                    return filter_data

            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    
        
        if filterCon == "<=":
            try:
                if filterKey == "Date":
                    filter_data = [x for x in hist_data if datetime.strptime(x[filterKey], "%Y-%m-%d").timestamp() <= datetime.strptime(filterConValue, "%Y-%m-%d").timestamp()]
                    return filter_data
                else:
                    filter_data = [x for x in hist_data if int(x[filterKey]) <= int(filterConValue)]
                    return filter_data

            except Exception as err:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)    


    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      



def FormulaFunctionFlowChart(sourceData, formulaKey):
    try:
       
        sourceData1 = []
        data_object1 = {}  

        for x in sourceData: 
            for k in x.keys():

                pdData = pd.DataFrame(x[k])
                for i in  range(int(len(formulaKey)/3)):
                    col1 = f'a_colA{i+1}'
                    op = f'a_op{i+1}'
                    col2 = f'a_colB{i+1}'
                    col1_check = ColumnCheckStart(pdData, formulaKey[col1])
                    col2_check = ColumnCheckStart(pdData, formulaKey[col2])

                    keyValue1 = f'resultValue{i+1}'

                    

                    if col1_check == True and col2_check == True and formulaKey[op] == '+':
                        pdData['result'] = pdData[formulaKey[col1]] + pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == True and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] + pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == False and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] + pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == False and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] + int(formulaKey[col2])
                    if col1_check == False and col2_check == False and formulaKey[op] == '+':
                        pdData['result'] = pdData['result'] + int(formulaKey[col2])

                    
                    if col1_check == True and col2_check == True and formulaKey[op] == '-':
                        pdData['result'] = pdData[formulaKey[col1]] - pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == True and formulaKey[op] == '-' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] - pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == False and formulaKey[op] == '-' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] - pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == False and formulaKey[op] == '-':
                        pdData['result'] = pdData['result'] - int(formulaKey[col2])    
                
                    if col1_check == True and col2_check == True and formulaKey[op] == '*':
                        pdData['result'] = pdData[formulaKey[col1]] * pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == True and formulaKey[op] == '*' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] * pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == True and formulaKey[op] == '*' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] * pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == False and formulaKey[op] == '*':
                        pdData['result'] = pdData['result'] * int(formulaKey[col2])    
                
                    if col1_check == True and col2_check == True and formulaKey[op] == '/':
                        pdData['result'] = pdData[formulaKey[col1]] / pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == True and formulaKey[op] == '/' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] / pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == True and formulaKey[op] == '/' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] / pdData[formulaKey[col2]] 
                    if col1_check == False and col2_check == False and formulaKey[op] == '/':
                        pdData['result'] = pdData['result'] / int(formulaKey[col2])
                        
                pdata = pdData.to_dict('records')
                data_object1[k] = pdata
                if len(data_object1) != 0:
                    sourceData1.append(data_object1)
                    data_object1= {}   

        return sourceData1
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      


def FormulaFunctionFlowChart(sourceData, formulaKey):
    try:
       
        sourceData1 = []
        data_object1 = {}  

        for x in sourceData: 
            for k in x.keys():

                pdData = pd.DataFrame(x[k])
                for i in  range(int(len(formulaKey)/3)):
                    col1 = f'a_colA{i+1}'
                    op = f'a_op{i+1}'
                    col2 = f'a_colB{i+1}'
                    col1_check = ColumnCheckStart(pdData, formulaKey[col1])
                    col2_check = ColumnCheckStart(pdData, formulaKey[col2])

                    keyValue1 = f'resultValue{i+1}'

                    

                    if col1_check == True and col2_check == True and formulaKey[op] == '+':
                        pdData['result'] = pdData[formulaKey[col1]] + pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == True and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] + pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == False and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] + pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == False and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] + int(formulaKey[col2])
                    if col1_check == False and col2_check == False and formulaKey[op] == '+':
                        pdData['result'] = pdData['result'] + int(formulaKey[col2])

                    
                    if col1_check == True and col2_check == True and formulaKey[op] == '-':
                        pdData['result'] = pdData[formulaKey[col1]] - pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == True and formulaKey[op] == '-' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] - pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == False and formulaKey[op] == '-' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] - pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == False and formulaKey[op] == '-':
                        pdData['result'] = pdData['result'] - int(formulaKey[col2])    
                
                    if col1_check == True and col2_check == True and formulaKey[op] == '*':
                        pdData['result'] = pdData[formulaKey[col1]] * pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == True and formulaKey[op] == '*' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] * pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == True and formulaKey[op] == '*' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] * pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == False and formulaKey[op] == '*':
                        pdData['result'] = pdData['result'] * int(formulaKey[col2])    
                
                    if col1_check == True and col2_check == True and formulaKey[op] == '/':
                        pdData['result'] = pdData[formulaKey[col1]] / pdData[formulaKey[col2]]
                    if col1_check == True and col2_check == True and formulaKey[op] == '/' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] / pdData[formulaKey[col2]]
                    if col1_check == False and col2_check == True and formulaKey[op] == '/' and formulaKey[col1] == f'result{i}':
                        pdData['result'] = pdData['result'] / pdData[formulaKey[col2]] 
                    if col1_check == False and col2_check == False and formulaKey[op] == '/':
                        pdData['result'] = pdData['result'] / int(formulaKey[col2])
                        
                pdata = pdData.to_dict('records')
                data_object1[k] = pdata
                if len(data_object1) != 0:
                    sourceData1.append(data_object1)
                    data_object1= {}   

        return sourceData1
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      



    try:
        pdData = pd.DataFrame(sourceData)
        for i in  range(int(len(formulaKey)/3)):
            col1 = f'a_colA{i+1}'
            op = f'a_op{i+1}'
            col2 = f'a_colB{i+1}'
            col1_check = ColumnCheckStart(pdData, formulaKey[col1])
            col2_check = ColumnCheckStart(pdData, formulaKey[col2])
            keyValue1 = f'resultValue{i+1}'

                    

            if col1_check == True and col2_check == True and formulaKey[op] == '+':
                pdData['result'] = pdData[formulaKey[col1]] + pdData[formulaKey[col2]]
            if col1_check == True and col2_check == True and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] + pdData[formulaKey[col2]]
            if col1_check == True and col2_check == False and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] + pdData[formulaKey[col2]]
            if col1_check == False and col2_check == False and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] + int(formulaKey[col2])
            if col1_check == False and col2_check == False and formulaKey[op] == '+':
                pdData['result'] = pdData['result'] + int(formulaKey[col2])

                    
            if col1_check == True and col2_check == True and formulaKey[op] == '-':
                pdData['result'] = pdData[formulaKey[col1]] - pdData[formulaKey[col2]]
            if col1_check == True and col2_check == True and formulaKey[op] == '-' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] - pdData[formulaKey[col2]]
            if col1_check == True and col2_check == False and formulaKey[op] == '-' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] - pdData[formulaKey[col2]]
            if col1_check == False and col2_check == False and formulaKey[op] == '-':
                pdData['result'] = pdData['result'] - int(formulaKey[col2])    
                
            if col1_check == True and col2_check == True and formulaKey[op] == '*':
                pdData['result'] = pdData[formulaKey[col1]] * pdData[formulaKey[col2]]
            if col1_check == True and col2_check == True and formulaKey[op] == '*' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] * pdData[formulaKey[col2]]
            if col1_check == False and col2_check == True and formulaKey[op] == '*' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] * pdData[formulaKey[col2]]
            if col1_check == False and col2_check == False and formulaKey[op] == '*':
                pdData['result'] = pdData['result'] * int(formulaKey[col2])    
                
            if col1_check == True and col2_check == True and formulaKey[op] == '/':
                pdData['result'] = pdData[formulaKey[col1]] / pdData[formulaKey[col2]]
            if col1_check == True and col2_check == True and formulaKey[op] == '/' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] / pdData[formulaKey[col2]]
            if col1_check == False and col2_check == True and formulaKey[op] == '/' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] / pdData[formulaKey[col2]] 
            if col1_check == False and col2_check == False and formulaKey[op] == '/':
                pdData['result'] = pdData['result'] / int(formulaKey[col2])

            pdData['fileKey'] = key            
        pdata = pdData.to_dict('records')
        # print("pdata", pdata)
        # data_object1[x] = pdata
        # if len(data_object1) != 0:
        #     sourceData1.append(data_object1)
        #     data_object1= {}   

        return pdata
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      

# def FormulaFunctionFlowChartFinal(sourceData, key, formulaKey):
def FormulaFunctionFlowChartFinal(sourceData, formulaKey):
    try:
        pdData = pd.DataFrame(sourceData)
        for i in  range(int(len(formulaKey)/3)):
            col1 = f'a_colA{i+1}'
            op = f'a_op{i+1}'
            col2 = f'a_colB{i+1}'
            col1_check = ColumnCheckStart(pdData, formulaKey[col1])
            col2_check = ColumnCheckStart(pdData, formulaKey[col2])
            keyValue1 = f'resultValue{i+1}'

                    

            if col1_check == True and col2_check == True and formulaKey[op] == '+':
                pdData['result'] = pdData[formulaKey[col1]] + pdData[formulaKey[col2]]
            if col1_check == True and col2_check == True and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] + pdData[formulaKey[col2]]
            if col1_check == True and col2_check == False and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] + pdData[formulaKey[col2]]
            if col1_check == False and col2_check == False and formulaKey[op] == '+' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] + int(formulaKey[col2])
            if col1_check == False and col2_check == False and formulaKey[op] == '+':
                pdData['result'] = pdData['result'] + int(formulaKey[col2])

                    
            if col1_check == True and col2_check == True and formulaKey[op] == '-':
                pdData['result'] = pdData[formulaKey[col1]] - pdData[formulaKey[col2]]
            if col1_check == True and col2_check == True and formulaKey[op] == '-' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] - pdData[formulaKey[col2]]
            if col1_check == True and col2_check == False and formulaKey[op] == '-' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] - pdData[formulaKey[col2]]
            if col1_check == False and col2_check == False and formulaKey[op] == '-':
                pdData['result'] = pdData['result'] - int(formulaKey[col2])    
                
            if col1_check == True and col2_check == True and formulaKey[op] == '*':
                pdData['result'] = pdData[formulaKey[col1]] * pdData[formulaKey[col2]]
            if col1_check == True and col2_check == True and formulaKey[op] == '*' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] * pdData[formulaKey[col2]]
            if col1_check == False and col2_check == True and formulaKey[op] == '*' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] * pdData[formulaKey[col2]]
            if col1_check == False and col2_check == False and formulaKey[op] == '*':
                pdData['result'] = pdData['result'] * int(formulaKey[col2])    
                
            if col1_check == True and col2_check == True and formulaKey[op] == '/':
                pdData['result'] = pdData[formulaKey[col1]] / pdData[formulaKey[col2]]
            if col1_check == True and col2_check == True and formulaKey[op] == '/' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] / pdData[formulaKey[col2]]
            if col1_check == False and col2_check == True and formulaKey[op] == '/' and formulaKey[col1] == f'result{i}':
                pdData['result'] = pdData['result'] / pdData[formulaKey[col2]] 
            if col1_check == False and col2_check == False and formulaKey[op] == '/':
                pdData['result'] = pdData['result'] / int(formulaKey[col2])

            # pdData['fileKey'] = key            
        pdata = pdData.to_dict('records')
        # print("pdata", pdata)
        # data_object1[x] = pdata
        # if len(data_object1) != 0:
        #     sourceData1.append(data_object1)
        #     data_object1= {}   

        return pdata
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      



def LineChartFlowChartFunctionTWO(sourceData, sourceKey):
    try:
        DataY= []
        DataY1 = {}
        
        DataW= []
        DataW1 = {}
        
        Data = []
        Data1 = {}
        Data2 = {}

        key1 = ""
        for x in sourceData: 
            for k in x.keys():
               
                for i in x[k]:
                    
                    for kk in range(len(sourceKey)):
                        if kk == 0:
                            key1 = sourceKey[kk]
                        if kk > 0:    
                           
                            DataY1['x'] = i[key1]
                            DataY1['y'] = i[sourceKey[kk]]
                            if len(DataY1) != 0:
                                DataY.append(DataY1)
                                DataY1 = {}

                            # if kk+1 < len(sourceKey):    
                            #     DataW1['x'] = i[key1]
                            #     DataW1['y'] = i[sourceKey[kk+2]]
                            #     if len(DataW1) != 0:
                            #         DataW.append(DataW1)
                            #         DataW1 = {}

                    

        Data1['prices'] = DataW
        if len(Data1) != 0:
            Data2['W'] = Data1
            Data.append(Data2)
            Data1 = {}
            Data2 = {}
            
        Data1['prices'] = DataY
        if len(Data1) != 0:
            Data2['Y'] = Data1
            Data.append(Data2)
            Data1 = {}
            Data2 = {}

        return Data
    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      
    
    
def TabularBlockFlowChartFunction(sourceData, sourceKey):
    try:
        Data= []
        Data1= []
        Data2= []
        for x in sourceData: 
            for k in x.keys():

                for i in range(len(x[k])):
                    if i == 0:
                        Data.append(x[k][i].values())
                    if i > 0:
                        Data.append(x[k][i].values())
                        
                        
                #     if i == 0:
                #         if len(Data1) == 0:
                #             Data.append(x[k][i].keys())
                #             Data1.append(x[k][i].keys())
                #     if i > 0:
                #         Data.append(x[k][i].values())
                
                # for i in range(len(x[k])):
                #     for mk in x[k][i].keys():
                #         for sk in sourceKey:
                #             if sk == mk:
                #                 if i == 0:
                #                     if len(Data1) == 0:
                #                         Data.append(sourceKey)
                #                         Data1.append(sourceKey)
                                       
                #                 if i > 0:
                #                     Data2.append(x[k][i][mk])
                #     if len(Data2):
                #         Data.append(Data2)
                #         Data2=[]            



        return Data
    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      
    


def TabularSingleBlogFunction(sourceData, sourceKey):
    try:
        Data= []
       
        for x in sourceData: 
            for k in x.keys():
                Data+= x[k]
               
        return Data
    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      
    
    


def SourceKeyFunction(sourceData, sourceKey):
    try:
        Data= []
        Data1= {}
        Data3= {}
        Data2= []
        for x in sourceData: 
            for k in x.keys():
                for i in range(len(x[k])):
                    for mk in x[k][i].keys():
                        for sk in sourceKey:
                            if sk == mk:
                                Data1[sk] = x[k][i][sk]

                              
                    if len(Data1) != 0:
                        Data2.append(Data1)
                        Data1={}
                        
                if len(Data2) != 0:
                    Data3[k] = Data2
                    Data.append(Data3)
                    Data2=[]
                    Data3 = {}

        return Data
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
def SourceKeyFormulaFunction(sourceData, sourceKey):
    try:
        Data= []
        Data1= {}
        Data3= {}
        Data2= []
        sourceKey.append('result')
        for x in sourceData: 
            for k in x.keys():
                
                for i in range(len(x[k])):
                    for mk in x[k][i].keys():
                        for sk in sourceKey:
                            if sk == mk:
                                Data1[sk] = x[k][i][sk]

                                
                    if len(Data1) != 0:
                        Data2.append(Data1)
                        Data1={}
                       
                if len(Data2) != 0:
                    Data3[k] = Data2
                    Data.append(Data3)
                    Data2=[]
                    Data3 = {}

        return Data
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)      
            
    
    

    

@api_view(['GET'])
def GETFLOWCHARTDATAAPI(request, flow_name):
    try:
        startTime = CurrentTimeFunc()

        APICALLFUNCTION('GETFLOWCHARTDATAAPI', 'null')
        flow_data_items= []
        processType = ""
        formula = ""
        source = []
        sourceKey = []
        sourceData = []
        finalData = []


       

        flow_data = Table_data_info.objects.get(table_id=544, column_data=flow_name)
        flow_data_ref = Table_data_info.objects.filter(table_id=544, table_ref_id=flow_data.table_ref_id)
        for m in flow_data_ref:
            if m.table_col_id == 1:
                flow_data_items = eval(m.column_data)
        

        for fd in flow_data_items:
            for k in fd.keys():
                if k == "sl" and fd[k] == 1:
                    if fd["stepType"] == "container":
                        processType= fd["processType"]
                    else:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 1 container is not found'}, status=status.HTTP_400_BAD_REQUEST)  
                if k == "sl" and fd[k] == 2:
                    if fd["stepType"] == "source" and fd["sourceType"] == "get data" and fd["sourceInfoType"] == "json data":
                        sourceKey= fd["sourceKey"]
                        source= fd["source"]
                        sourceData = SourceFunction(fd["source"])
                    else:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 2 source is not found'}, status=status.HTTP_400_BAD_REQUEST)  
                if k == "sl" and fd[k] == 3:
                    if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
                        sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
                    if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
                        formula = fd["stepType"]
                        sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])

                if k == "sl" and fd[k] == 4:
                    if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
                        sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
                    if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
                        formula = fd["stepType"]
                        sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])
               

        
        if formula == "formula":
            sourceData = SourceKeyFormulaFunction(sourceData, sourceKey)
        else:
            sourceData = SourceKeyFunction(sourceData, sourceKey)

        if processType == "linebarchart":
            finalData = LineChartFlowChartFunctionTWO(sourceData, sourceKey)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(finalData)
            DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart linebarchart data", value_count, round(loadTime, 6))
            
            return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "data": finalData, "sourceData": sourceData})

        if processType == "tabularblock":
            finalData = TabularBlockFlowChartFunction(sourceData, sourceKey)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(finalData)
            DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart tabularblock data", value_count, round(loadTime, 6))
            
            return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "head": sourceKey, "data": finalData, "sourceData": sourceData})


        if processType == 'TabularSingleBlog':
            finalData = TabularSingleBlogFunction(sourceData, sourceKey)
            
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(finalData)
            DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart TabularSingleBlog data", value_count, round(loadTime, 6))
            
            return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "data": finalData, "sourceData": sourceData})

        


    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        


        

@api_view(['POST'])
def POSTFLOWCHARTDATAAPI1(request):
    try:
        startTime = CurrentTimeFunc()

        # APICALLFUNCTION('GETFLOWCHARTDATAAPI', 'null')
        flow_data_items= []
        processType = ""
        formula = ""
        source = []
        sourceKey = []
        sourceData = []
        finalData = []


        node_data = request.data['node_data']

        # flow_data = Table_data_info.objects.get(table_id=471, column_data=flow_name)
        # flow_data_ref = Table_data_info.objects.filter(table_id=471, table_ref_id=flow_data.table_ref_id)
        # for m in flow_data_ref:
        #     if m.table_col_id == 2:
        #         flow_data_items = eval(m.column_data)
        

        # print("node_data", node_data)
        node = node_data['nodes']
        # print("node", node)
        for nd in node:
            print("nd", nd)
            for k in nd.keys():
                print("k", k)
                if k == "type":
                    if nd['type'] == "container":
                        if nd['data']['label'] == 'container':
                            processType= nd['data']['container']['processType']

                    if nd['type'] == "source":
                        if nd['data']['label'] == 'source':
                            if nd['data']['source']['sourceType'] == 'get data' and nd['data']['source']['sourceInfoType'] == 'json data':
                                sourceKey += nd['data']['source']["sourceKey"]
                                source += nd['data']['source']['source']
                                sourceData += SourceFunction(nd['data']['source']['source'])
                                
                    if nd['type'] == "filter":
                        if nd['data']['label'] == 'filter':
                            # print("nd['data']['filter']", nd['data']['filter'])
                            if nd['data']['filter']['sourceType'] == 'filter data' and nd['data']['filter']['sourceInfoType'] == 'json data':
                                sourceData = FilterFunctionFlowChart(source, sourceData, nd['data']['filter']["filterKey"], nd['data']['filter']["filterCon"],  nd['data']['filter']["filterConValue"])


        print("processType", processType)
        print("sourceKey", list(set(sourceKey)))
        print("source", source)
        # print("sourceData", sourceData)
        # print("flow_data_items", flow_data_items)

        # for fd in flow_data_items:
        #     for k in fd.keys():
        #         if k == "sl" and fd[k] == 1:
        #             if fd["stepType"] == "container":
        #                 processType= fd["processType"]
        #             else:
        #                 return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 1 container is not found'}, status=status.HTTP_400_BAD_REQUEST)  
        #         if k == "sl" and fd[k] == 2:
        #             if fd["stepType"] == "source" and fd["sourceType"] == "get data" and fd["sourceInfoType"] == "json data":
        #                 sourceKey= fd["sourceKey"]
        #                 source= fd["source"]
        #                 sourceData = SourceFunction(fd["source"])
        #             else:
        #                 return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 2 source is not found'}, status=status.HTTP_400_BAD_REQUEST)  
        #         if k == "sl" and fd[k] == 3:
        #             if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
        #                 sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
        #             if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
        #                 formula = fd["stepType"]
        #                 sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])

        #         if k == "sl" and fd[k] == 4:
        #             if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
        #                 sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
        #             if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
        #                 formula = fd["stepType"]
        #                 sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])
               

        
        # if formula == "formula":
        #     sourceData = SourceKeyFormulaFunction(sourceData, sourceKey)
        # else:
        #     sourceData = SourceKeyFunction(sourceData, sourceKey)

        # if processType == "linebarchart":
        #     finalData = LineChartFlowChartFunctionTWO(sourceData, sourceKey)
            
        #     endTime = CurrentTimeFunc()
        #     loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     value_count = ValueCountFunc(finalData)
        #     DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart linebarchart data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "data": finalData, "sourceData": sourceData})

        # if processType == "tabularblock":
        #     finalData = TabularBlockFlowChartFunction(sourceData, sourceKey)
            
        #     endTime = CurrentTimeFunc()
        #     loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     value_count = ValueCountFunc(finalData)
        #     DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart tabularblock data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "head": sourceKey, "data": finalData, "sourceData": sourceData})


        # if processType == 'TabularSingleBlog':
        #     finalData = TabularSingleBlogFunction(sourceData, sourceKey)
            
        #     endTime = CurrentTimeFunc()
        #     loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     value_count = ValueCountFunc(finalData)
        #     DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart TabularSingleBlog data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "data": finalData, "sourceData": sourceData})
        
        if processType == "tabeldata":
            finalData = TabularBlockFlowChartFunction(sourceData, sourceKey)
            
            # endTime = CurrentTimeFunc()
            # loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            # value_count = ValueCountFunc(finalData)
            # DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart tabularblock data", value_count, round(loadTime, 6))
            
            return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "head": list(set(sourceKey)), "data": finalData, "sourceData": sourceData})

        # return Response({'message':'success','status': status.HTTP_200_OK, 'data': sourceData})

        


    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def POSTFLOWCHARTDATAGETAPI(request):
    try:
        startTime = CurrentTimeFunc()

        # APICALLFUNCTION('GETFLOWCHARTDATAAPI', 'null')
        flow_data_items= []
        processType = ""
        formula = ""
        source = []
        sourceKey = []
        sourceData = []
        source1 = []
        sourceKey1 = []
        sourceData1 = []
        source2 = []
        sourceKey2 = []
        sourceData2 = []
        finalData = []


        node_data = request.data['node_data']

        # flow_data = Table_data_info.objects.get(table_id=471, column_data=flow_name)
        # flow_data_ref = Table_data_info.objects.filter(table_id=471, table_ref_id=flow_data.table_ref_id)
        # for m in flow_data_ref:
        #     if m.table_col_id == 2:
        #         flow_data_items = eval(m.column_data)
        

        print("node_data", node_data)

        for nd in node_data:
            print("nd", nd)
            if nd == 'L1':
                print("node_data[nd]", node_data[nd])
                for step1 in node_data[nd]:
                    print("step1", step1)
                    if step1 == 'data':
                        # print("node_data[nd][step1]", node_data[nd][step1])
                        if node_data[nd][step1]['type'] == "container":
                            processType= node_data[nd][step1]['data']['container']['processType']
                    if step1 == 'L2': 
                        # print("node_data[nd][step1]", node_data[nd][step1])   
                        for step2 in node_data[nd][step1]:
                            # print("step2", step2) 
                            for key1 in node_data[nd][step1].keys():
                                # print("key1", key1)   
                                if step2 == key1:
                                    if step2 == 'L21':
                                        # print("node_data[nd][step1][step2]", node_data[nd][step1][step2])
                                        for step3 in node_data[nd][step1][step2]:
                                            # print("step3", step3)
                                            for key2 in node_data[nd][step1][step2].keys():
                                                # print("key2", key2)   
                                                if step3 == key2: 
                                                    if step3 == 'data':
                                                        # print("node_data[nd][step1][step2][step3]", node_data[nd][step1][step2][step3])
                                                        if node_data[nd][step1][step2][step3]['type'] == 'source' and node_data[nd][step1][step2][step3]['data']['source']['sourceType'] == 'get data' and node_data[nd][step1][step2][step3]['data']['source']['sourceInfoType'] == 'json data':
                                                            sourceKey1 = node_data[nd][step1][step2][step3]['data']['source']["sourceKey"]
                                                            source1 = node_data[nd][step1][step2][step3]['data']['source']['source']
                                                            sourceData1 = SourceFunction(node_data[nd][step1][step2][step3]['data']['source']['source'])
                                                    else:
                                                        # print("node_data[nd][step1][step2][step3]", node_data[nd][step1][step2][step3])
                                                        if node_data[nd][step1][step2][step3]['type'] == 'filter' and node_data[nd][step1][step2][step3]['data']['filter']['sourceType'] == 'filter data' and node_data[nd][step1][step2][step3]['data']['filter']['sourceInfoType'] == 'json data':
                                                            sourceData1 = FilterFunctionFlowChart(source1, sourceData1, node_data[nd][step1][step2][step3]['data']['filter']["filterKey"], node_data[nd][step1][step2][step3]['data']['filter']["filterCon"],  node_data[nd][step1][step2][step3]['data']['filter']["filterConValue"])
                                    if step2 == 'L22':
                                        # print("node_data[nd][step1][step2]", node_data[nd][step1][step2])
                                        for step3 in node_data[nd][step1][step2]:
                                            # print("step3", step3)
                                            for key2 in node_data[nd][step1][step2].keys():
                                                # print("key2", key2)   
                                                if step3 == key2: 
                                                    if step3 == 'data':
                                                        # print("node_data[nd][step1][step2][step3]", node_data[nd][step1][step2][step3])
                                                        if node_data[nd][step1][step2][step3]['type'] == 'source' and node_data[nd][step1][step2][step3]['data']['source']['sourceType'] == 'get data' and node_data[nd][step1][step2][step3]['data']['source']['sourceInfoType'] == 'json data':
                                                            sourceKey2 = node_data[nd][step1][step2][step3]['data']['source']["sourceKey"]
                                                            source2 = node_data[nd][step1][step2][step3]['data']['source']['source']
                                                            sourceData2 = SourceFunction(node_data[nd][step1][step2][step3]['data']['source']['source'])
                                                    else:
                                                        # print("node_data[nd][step1][step2][step3]", node_data[nd][step1][step2][step3])
                                                        if node_data[nd][step1][step2][step3]['type'] == 'filter' and node_data[nd][step1][step2][step3]['data']['filter']['sourceType'] == 'filter data' and node_data[nd][step1][step2][step3]['data']['filter']['sourceInfoType'] == 'json data':
                                                            sourceData2 = FilterFunctionFlowChart(source2, sourceData2, node_data[nd][step1][step2][step3]['data']['filter']["filterKey"], node_data[nd][step1][step2][step3]['data']['filter']["filterCon"],  node_data[nd][step1][step2][step3]['data']['filter']["filterConValue"])

                    if step1 == 'L3_merge':
                        print("node_data[nd][step1]", node_data[nd][step1])
                        if node_data[nd][step1]['type'] == 'filter' and node_data[nd][step1]['data']['filter']['sourceType'] == 'filter data' and node_data[nd][step1]['data']['filter']['sourceInfoType'] == 'json data':
                            source= source1+source2
                            sourceData = sourceData1+sourceData2
                            sourceData = FilterFunctionFlowChart(source, sourceData, node_data[nd][step1]['data']['filter']["filterKey"], node_data[nd][step1]['data']['filter']["filterCon"], node_data[nd][step1]['data']['filter']["filterConValue"])


        #     for k in nd.keys():
        #         print("k", k)
        #         if k == "type":
        #             if nd['type'] == "container":
        #                 if nd['data']['label'] == 'container':
        #                     processType= nd['data']['container']['processType']

        #             if nd['type'] == "source":
        #                 if nd['data']['label'] == 'source':
        #                     if nd['data']['source']['sourceType'] == 'get data' and nd['data']['source']['sourceInfoType'] == 'json data':
        #                         sourceKey += nd['data']['source']["sourceKey"]
        #                         source += nd['data']['source']['source']
        #                         sourceData += SourceFunction(nd['data']['source']['source'])
                                
        #             if nd['type'] == "filter":
        #                 if nd['data']['label'] == 'filter':
        #                     # print("nd['data']['filter']", nd['data']['filter'])
        #                     if nd['data']['filter']['sourceType'] == 'filter data' and nd['data']['filter']['sourceInfoType'] == 'json data':
        #                         sourceData = FilterFunctionFlowChart(source, sourceData, nd['data']['filter']["filterKey"], nd['data']['filter']["filterCon"],  nd['data']['filter']["filterConValue"])


        print("processType", processType)
        # print("sourceKey", list(set(sourceKey)))
        # print("source", source)
        # print("sourceData", sourceData)
        # print("flow_data_items", flow_data_items)

        # for fd in flow_data_items:
        #     for k in fd.keys():
        #         if k == "sl" and fd[k] == 1:
        #             if fd["stepType"] == "container":
        #                 processType= fd["processType"]
        #             else:
        #                 return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 1 container is not found'}, status=status.HTTP_400_BAD_REQUEST)  
        #         if k == "sl" and fd[k] == 2:
        #             if fd["stepType"] == "source" and fd["sourceType"] == "get data" and fd["sourceInfoType"] == "json data":
        #                 sourceKey= fd["sourceKey"]
        #                 source= fd["source"]
        #                 sourceData = SourceFunction(fd["source"])
        #             else:
        #                 return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 2 source is not found'}, status=status.HTTP_400_BAD_REQUEST)  
        #         if k == "sl" and fd[k] == 3:
        #             if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
        #                 sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
        #             if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
        #                 formula = fd["stepType"]
        #                 sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])

        #         if k == "sl" and fd[k] == 4:
        #             if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
        #                 sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
        #             if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
        #                 formula = fd["stepType"]
        #                 sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])
               

        
        # if formula == "formula":
        #     sourceData = SourceKeyFormulaFunction(sourceData, sourceKey)
        # else:
        #     sourceData = SourceKeyFunction(sourceData, sourceKey)

        # if processType == "linebarchart":
        #     finalData = LineChartFlowChartFunctionTWO(sourceData, sourceKey)
            
        #     endTime = CurrentTimeFunc()
        #     loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     value_count = ValueCountFunc(finalData)
        #     DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart linebarchart data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "data": finalData, "sourceData": sourceData})

        # if processType == "tabularblock":
        #     finalData = TabularBlockFlowChartFunction(sourceData, sourceKey)
            
        #     endTime = CurrentTimeFunc()
        #     loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     value_count = ValueCountFunc(finalData)
        #     DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart tabularblock data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "head": sourceKey, "data": finalData, "sourceData": sourceData})


        # if processType == 'TabularSingleBlog':
        #     finalData = TabularSingleBlogFunction(sourceData, sourceKey)
            
        #     endTime = CurrentTimeFunc()
        #     loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     value_count = ValueCountFunc(finalData)
        #     DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart TabularSingleBlog data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "data": finalData, "sourceData": sourceData})
        
        sourceKey = sourceKey1+sourceKey2

        if processType == "tabeldata":
            finalData = TabularBlockFlowChartFunction(sourceData, list(set(sourceKey)))
            
            # endTime = CurrentTimeFunc()
            # loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            # value_count = ValueCountFunc(finalData)
            # DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart tabularblock data", value_count, round(loadTime, 6))
            
            return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "head": list(set(sourceKey)), "data": finalData, "sourceData": sourceData})

        # return Response({'message':'success','status': status.HTTP_200_OK, 'data': sourceData, 'sourceData': sourceData})
        # return Response({'message':'success','status': status.HTTP_200_OK})

        


    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        


@api_view(['POST'])
def POSTFLOWCHARTDATAAPI(request):
    try:
        startTime = CurrentTimeFunc()

        # APICALLFUNCTION('GETFLOWCHARTDATAAPI', 'null')
        flow_data_items= []
        processType = ""
        formula = ""
        source = []
        sourceKey = []
        sourceData = []
        finalData = []


        node_data = request.data['node_data']

        # flow_data = Table_data_info.objects.get(table_id=471, column_data=flow_name)
        # flow_data_ref = Table_data_info.objects.filter(table_id=471, table_ref_id=flow_data.table_ref_id)
        # for m in flow_data_ref:
        #     if m.table_col_id == 2:
        #         flow_data_items = eval(m.column_data)
        

        # print("node_data", node_data)
        node = node_data['nodes']
        edge = node_data['edges']
        # print("node", node)
        # print("edge", edge)

        count = 0
        lenCount = len(node)
        print("lenCount", lenCount)
        itemDic = {}
        sourcesection = {}

        targetValue = 0
        mergeDataValue = {}
        msection = {} 

        for n in node:
            # print("e", e)
            # print("e['source']", e['source'])
            # print("e['target']", e['target'])
            # edgeData = [x for x in edge if x['source'] == e['source']]
            # print("edgeData", edgeData)

           
            if n['type'] == "container" and n['data']['label'] == 'container':
                section = {}
                section['id'] =  n['id']
                section['type'] =  n['type']
                section['data'] =  { 'container' :  n['data']['container'] }
                # itemDic['L1'] = section

                edgeData = [x for x in edge if x['source'] == n['id']]
                print("edgeData", edgeData)
               
                edgeLenCount = len(edgeData)
                print("edgeLenCount", edgeLenCount)
                ecount = 0
                scsection={ }
                for e in edgeData:
                    print("e['source']", e['source'])
                    print("e['target']", e['target'])
                    ecount+=1

                    nodeData = [x for x in node if x['id'] == e['target']]
                    print("nodeData", nodeData)
                    for nd in nodeData:
                        if nd['type'] == "source" and nd['data']['label'] == 'source':
                            ssection = {}
                            ssection['id'] =  nd['id']
                            ssection['type'] =  nd['type']
                            ssection['data'] =  { 'source' :  nd['data']['source'] }
                            # scsection[f'L2{ecount}'] = ssection

                            sedgeData = [x for x in edge if x['source'] == nd['id']]

                            print("sedgeData", sedgeData)
               
                            sedgeLenCount = len(sedgeData)
                            print("sedgeLenCount", sedgeLenCount)
                            sescount = 0
                            sscsection={ }
                            for se in sedgeData:
                                print("se['source']", se['source'])
                                print("se['target']", se['target'])
                                sescount+=1
                                snodeData = [x for x in node if x['id'] == se['target']]
                                print("snodeData", snodeData)
                                for snd in snodeData:
                                    if snd['type'] == "filter" and snd['data']['label'] == 'filter':
                                        print("snd", snd)
                                        fsection = {}
                                        fsection['id'] =  snd['id']
                                        fsection['type'] =  snd['type']
                                        fsection['data'] =  { 'filter' :  snd['data']['filter'] }
                                        scsection[f'L2{ecount}'] = { 'data': ssection, f'L2{ecount}{sescount}': fsection }

                                        medgeData = [x for x in edge if x['source'] == snd['id']]
                                        print("medgeData", medgeData)
                                        print("medgeData[0]['target']", medgeData[0]['target'])
                                        sectionmerge = {
                                            'source':  medgeData[0]['source'],
                                            'target':  medgeData[0]['target'],
                                            'key':  f'L2{ecount}{sescount}',
                                        }
                                        mergeDataValue[f'L2{ecount}{sescount}']=sectionmerge
                                        # medgeLenCount = len(medgeData)
                                        # print("medgeLenCount", medgeLenCount)
                                        # mcount = 0
                                        # sscsection={ }

                # sourcesection['L2'] = scsection
                keyItem = []
                for key in mergeDataValue.keys():
                    # print("key", key)
                    keyItem.append(key)
                print("keyItem", keyItem) 
                if len(keyItem) == 2:  
                    if mergeDataValue[keyItem[0]]['target'] == mergeDataValue[keyItem[1]]['target']:
                        # print("mergeDataValue[keyItem[0]]['target']", mergeDataValue[keyItem[0]]['target'] )
                        # print("mergeDataValue[keyItem[1]]['target']", mergeDataValue[keyItem[1]]['target'] )
                        mergenodeData = [x for x in node if x['id'] ==  mergeDataValue[keyItem[0]]['target']]
                        print("mergenodeData", mergenodeData)
                        for mnd in mergenodeData:
                            if mnd['type'] == "filter" and mnd['data']['label'] == 'filter':
                                
                                msection['id'] =  mnd['id']
                                msection['key'] =  keyItem
                                msection['type'] =  mnd['type']
                                msection['data'] =  { 'filter' :  mnd['data']['filter'] }

                itemDic['L1'] = {'data': section, 'L2': scsection, 'L3_merge': msection}
        # for e in edge:
        #     # print("e", e)
        #     # print("e['source']", e['source'])
        #     # print("e['target']", e['target'])
        #     # edgeData = [x for x in edge if x['source'] == e['source']]
        #     # print("edgeData", edgeData)

        #     count +=1
        #     if count == 1:
        #         nodeData = [x for x in node if x['id'] == e['source']]
        #         print("nodeData", nodeData)
        #         for nd in nodeData:
        #             if nd['type'] == "container" and nd['data']['label'] == 'container':
        #                 print("nd", nd)
        #                 # itemDic['L1'] 
        #                 section = {}
        #                 section['id'] =  nd['id']
        #                 section['type'] =  nd['type']
        #                 section['data'] =  { 'container' :  nd['data']['container'] }
        #                 itemDic['L1'] = section


        print("mergeDataValue", mergeDataValue)
        # print("sourcesection", sourcesection)
        # print("itemDic", itemDic)




        # for nd in node:
        #     print("nd", nd)
        #     for k in nd.keys():
        #         print("k", k)
        #         if k == "type":
        #             if nd['type'] == "container":
        #                 if nd['data']['label'] == 'container':
        #                     processType= nd['data']['container']['processType']

        #             if nd['type'] == "source":
        #                 if nd['data']['label'] == 'source':
        #                     if nd['data']['source']['sourceType'] == 'get data' and nd['data']['source']['sourceInfoType'] == 'json data':
        #                         sourceKey += nd['data']['source']["sourceKey"]
        #                         source += nd['data']['source']['source']
        #                         sourceData += SourceFunction(nd['data']['source']['source'])
                                
        #             if nd['type'] == "filter":
        #                 if nd['data']['label'] == 'filter':
        #                     # print("nd['data']['filter']", nd['data']['filter'])
        #                     if nd['data']['filter']['sourceType'] == 'filter data' and nd['data']['filter']['sourceInfoType'] == 'json data':
        #                         sourceData = FilterFunctionFlowChart(source, sourceData, nd['data']['filter']["filterKey"], nd['data']['filter']["filterCon"],  nd['data']['filter']["filterConValue"])


        # print("processType", processType)
        # print("sourceKey", list(set(sourceKey)))
        # print("source", source)
        # print("sourceData", sourceData)
        # print("flow_data_items", flow_data_items)

        # for fd in flow_data_items:
        #     for k in fd.keys():
        #         if k == "sl" and fd[k] == 1:
        #             if fd["stepType"] == "container":
        #                 processType= fd["processType"]
        #             else:
        #                 return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 1 container is not found'}, status=status.HTTP_400_BAD_REQUEST)  
        #         if k == "sl" and fd[k] == 2:
        #             if fd["stepType"] == "source" and fd["sourceType"] == "get data" and fd["sourceInfoType"] == "json data":
        #                 sourceKey= fd["sourceKey"]
        #                 source= fd["source"]
        #                 sourceData = SourceFunction(fd["source"])
        #             else:
        #                 return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 2 source is not found'}, status=status.HTTP_400_BAD_REQUEST)  
        #         if k == "sl" and fd[k] == 3:
        #             if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
        #                 sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
        #             if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
        #                 formula = fd["stepType"]
        #                 sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])

        #         if k == "sl" and fd[k] == 4:
        #             if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
        #                 sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
        #             if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
        #                 formula = fd["stepType"]
        #                 sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])
               

        
        # if formula == "formula":
        #     sourceData = SourceKeyFormulaFunction(sourceData, sourceKey)
        # else:
        #     sourceData = SourceKeyFunction(sourceData, sourceKey)

        # if processType == "linebarchart":
        #     finalData = LineChartFlowChartFunctionTWO(sourceData, sourceKey)
            
        #     endTime = CurrentTimeFunc()
        #     loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     value_count = ValueCountFunc(finalData)
        #     DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart linebarchart data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "data": finalData, "sourceData": sourceData})

        # if processType == "tabularblock":
        #     finalData = TabularBlockFlowChartFunction(sourceData, sourceKey)
            
        #     endTime = CurrentTimeFunc()
        #     loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     value_count = ValueCountFunc(finalData)
        #     DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart tabularblock data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "head": sourceKey, "data": finalData, "sourceData": sourceData})


        # if processType == 'TabularSingleBlog':
        #     finalData = TabularSingleBlogFunction(sourceData, sourceKey)
            
        #     endTime = CurrentTimeFunc()
        #     loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     value_count = ValueCountFunc(finalData)
        #     DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart TabularSingleBlog data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "data": finalData, "sourceData": sourceData})
        
        # if processType == "tabeldata":
        #     finalData = TabularBlockFlowChartFunction(sourceData, sourceKey)
            
        #     # endTime = CurrentTimeFunc()
        #     # loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        #     # value_count = ValueCountFunc(finalData)
        #     # DataFetch_Static("GETFLOWCHARTDATAAPI", "json flowchart tabularblock data", value_count, round(loadTime, 6))
            
        #     return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "head": list(set(sourceKey)), "data": finalData, "sourceData": sourceData})

        return Response({'message':'success','status': status.HTTP_200_OK, 'data': itemDic})

        


    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  



def find_key(data, target_key, path=None):
    """
    Recursively search for a key in multi-layer JSON data.

    :param data: The JSON data (can be a dict, list, etc.)
    :param target_key: The key to search for
    :param path: Internal parameter to keep track of the current path
    :return: A list of tuples containing the key path and value
    """
    if path is None:
        path = []

    results = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                results.append((path + [key], value))
            results.extend(find_key(value, target_key, path + [key]))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            results.extend(find_key(item, target_key, path + [f"[{index}]"]))

    return results

def modify_json_value(data, key_path, new_value):
    """Modify a value in a multi-layer JSON object.

    Args:
        data (dict): The JSON data as a Python dictionary.
        key_path (list): A list of keys representing the path to the value.
        new_value: The new value to set.
    """

    current = data
    for key in key_path[:-1]:
        if key not in current:
            return  # Key not found, do nothing
        current = current[key]

    current[key_path[-1]] = new_value



# Function to add a value in a multi-layer JSON
def add_value(json_obj, key_list, value):
    current = json_obj
    for key in key_list[:-1]:
        # Create nested dictionaries if the key doesn't exist
        if key not in current:
            current[key] = {}
        current = current[key]
    # Add the value to the last key
    current[key_list[-1]] = value


def FilterTypeCheck(n):
    try:
        section = {}
        if n['type'] == "container" and n['data']['label'] == 'container':
            section['id'] =  n['id']
            section['type'] =  n['type']
            section['data'] =  { 'container' :  n['data']['container'] }

        if n['type'] == "source" and n['data']['label'] == 'source':
            section['id'] =  n['id']
            section['type'] =  n['type']
            section['data'] =  { 'source' :  n['data']['source'] }

        if n['type'] == "filter" and n['data']['label'] == 'filter':
            section['id'] =  n['id']
            section['type'] =  n['type']
            section['data'] =  { 'filter' :  n['data']['filter'] } 

        if n['type'] == "join" and n['data']['label'] == 'join':
            section['id'] =  n['id']
            section['type'] =  n['type']
            section['data'] =  { 'join' :  n['data']['join'] }

        if n['type'] == "formula" and n['data']['label'] == 'formula':
            section['id'] =  n['id']
            section['type'] =  n['type']
            section['data'] =  { 'formula' :  n['data']['formula'] }            

          
        return section
    except Exception as error:
        print("error", error)


def KeyFindOut(KeyData):
    try:
        keyItem = []
        for fk in KeyData:
            keyItem.append(fk)
        return list(set(keyItem))
    except Exception as error:
        print("error", error)            

def FlowChartData(node_data):
    try:
        # print("nnncdkdkd")
        processType = ""
        formula = ""
        source = []
        sourceKey = []
        sourceData = []
        finalData = []
        fl1 = {}
        fl2 = {}
        fl3 = {}
        fl4 = {}
        fl5 = {}
        dpkey = ''
        dataType = ''
        for nd in node_data:
            if nd != "merge_data":
                if  node_data[nd]['data']['type'] == 'container':
                    processType = node_data[nd]['data']['data']['container']['processType']

                count = 0
                for key in node_data[nd]: #nd=nodeid
                
                    if key != 'data':  # key=nodeid
                        count+=1
                        # if node_data[nd][key]['data']['type'] == 'source' and node_data[nd][key]['data']['data']['source']['sourceType'] == 'get data' and node_data[nd][key]['data']['data']['source']['sourceInfoType'] == 'json data':
                        if node_data[nd][key]['data']['type'] == 'source' and node_data[nd][key]['data']['data']['source']['sourceType'] == 'get data':
                            if node_data[nd][key]['data']['data']['source']['sourceInfoType'] == 'json data':
                                sourceSection = {}
                                sourceSection["source"] = node_data[nd][key]['data']['data']['source']["source"]
                                sourceSection["sourceKey"] = node_data[nd][key]['data']['data']['source']["sourceKey"]
                                sourceSection["sourceData"] = SourceFunctionFinal(node_data[nd][key]['data']['data']['source']["source"], node_data[nd][key]['data']['data']['source']["sourceKey"])
                                fl1[key] = sourceSection
                                # sourceKey = node_data[nd][key]['data']['data']['source']["sourceKey"]
                                dataType = node_data[nd][key]['data']['data']['source']['sourceInfoType']
                            elif node_data[nd][key]['data']['data']['source']['sourceInfoType'] == 'external file creation':
                                #external file create=tion function call
                                print("hello")
                        depth = find_depth(node_data[nd][key])
                        print("Depth of JSON:", depth)
                        print("depth[:-2] of JSON:", depth[:-2])
                        countdp = 0
                        countdf = 0
                        for dp in depth:
                            print("dp", dp)
                            print("dp[0]", dp[0])
                            key_to_find = dp[0]
                            results = find_key(node_data, key_to_find)

                            if len(results) !=0:
                                for path, value in results:
                                    if value['data']['type'] == 'filter':
                                        if value['data']['data']['filter']['sourceType'] == 'filter data' and value['data']['data']['filter']['sourceInfoType'] == 'json data':
                                            countdp+=1
                                            if countdp == 1:
                                                filter_result = find_key(fl1, key)

                                                if len(filter_result) !=0:
                                                    for path1, value1 in filter_result:
                                                        filter1Section = {}
                                                        filter1Section["source"] = value1["source"]
                                                        filter1Section["sourceKey"] = value1["sourceKey"]
                                                        filter1Section["sourceData"] = FilterFunctionFlowChartFinal(value1["sourceData"], value['data']['data']['filter']["filterKey"], value['data']['data']['filter']["filterCon"], value['data']['data']['filter']["filterConValue"])
                                                        fl2[dp[0]] = filter1Section
                                                        dpkey=dp[0]
                                                        sourceKey = KeyFindOut(filter1Section["sourceData"][0])        

                                            if countdp == 2:
                                                filter_result2 = find_key(fl2, dpkey)
                                                if len(filter_result2) !=0:
                                                    for path2, value2 in filter_result2:
                                                        filter2Section = {}
                                                        filter2Section["source"] = value2["source"]
                                                        filter2Section["sourceKey"] = value2["sourceKey"]
                                                        filter2Section["sourceData"] = FilterFunctionFlowChartFinal(value2["sourceData"], value['data']['data']['filter']["filterKey"], value['data']['data']['filter']["filterCon"], value['data']['data']['filter']["filterConValue"])
                                                        fl3[dp[0]] = filter2Section
                                                        dpkey=dp[0]
                                                        sourceKey = KeyFindOut(filter2Section["sourceData"][0])   

                                        else:
                                            print("filter")

                                    elif value['data']['type'] == 'formula':
                                        #formula 
                                        # print("formula value['data']['data']", value['data']['data'])

                                        if value['data']['data']['formula']['sourceType'] == 'formula data' and value['data']['data']['formula']['sourceInfoType'] == 'json data':
                                            countdf+=1
                                            if countdf ==1:
                                                formula_result = find_key(fl1, key)

                                                if len(formula_result) !=0:
                                                    for path1, value1 in formula_result:
                                                        formula1Section = {}
                                                        formula1Section["source"] = value1["source"]
                                                        formula1Section["sourceKey"] = value1["sourceKey"]
                                                        # formula1Section["sourceData"] = FormulaFunctionFlowChartFinal(value1["sourceData"], value1["source"][0], value['data']['data']['formula']['formula'])
                                                        formula1Section["sourceData"] = FormulaFunctionFlowChartFinal(value1["sourceData"], value['data']['data']['formula']['formula'])
                                                        # print("formula1  value['data']['data']['formula']['formula']", value['data']['data']['formula']['formula'])
                                                        fl2[dp[0]] = formula1Section
                                                        dpkey=dp[0]
                                                        sourceKey = KeyFindOut(formula1Section["sourceData"][0])   

                                            if countdf == 2:
                                                formula_result2 = find_key(fl2, key)

                                                if len(formula_result2) !=0:
                                                    for path2, value2 in formula_result2:
                                                        formula2Section = {}
                                                        formula2Section["source"] = value2["source"]
                                                        formula2Section["sourceKey"] = value2["sourceKey"]
                                                        formula2Section["sourceData"] = FormulaFunctionFlowChartFinal(value2["sourceData"], value['data']['data']['formula']['formula'])
                                                        # print("formula1  value['data']['data']['formula']['formula']", value['data']['data']['formula']['formula'])
                                                        fl3[dp[0]] = formula2Section
                                                        dpkey=dp[0]
                                                        sourceKey = KeyFindOut(formula2Section["sourceData"][0]) 
            
            if nd == "merge_data":
                # print("node_data[nd]", node_data[nd])
                # print("node_data[nd]['target']", node_data[nd]['target'])

                # join_depth = find_depth(node_data[nd]['target'])
                # print("Join Depth of JSON:", join_depth)
                # MergeDataItem = []
                for skey in node_data[nd]['source']:
                    # print("skey", skey)
                    mresults1 = find_key(fl1, skey)
                    if len(mresults1) !=0:
                        for path, value in mresults1:
                            fl4[value['source'][0]] = value["sourceData"]


                    mresults2 = find_key(fl2, skey)
                    if len(mresults2) !=0:
                        for path, value in mresults2:
                            fl4[value['source'][0]] = value["sourceData"]

                    mresults3 = find_key(fl3, skey)
                    if len(mresults3) !=0:
                        for path, value in mresults3:
                            fl4[value['source'][0]] = value["sourceData"]


                join_find_key_result = find_key(node_data, node_data[nd]['target'])

                if len(join_find_key_result) !=0:
                    for jk in join_find_key_result[0][1]:
                        # print("jk", jk)
                        if jk != 'data':
                            print("join_find_key_result[0][1][jk]", join_find_key_result[0][1][jk])
                            if join_find_key_result[0][1][jk]['data']['type'] == 'formula': 
                                # print("join_find_key_result[0][1][jk]['data']['data']['formula']", join_find_key_result[0][1][jk]['data']['data']['formula'])
                                # print("join_find_key_result[0][1][jk]['data']['data']['formula']", len(join_find_key_result[0][1][jk]['data']['data']['formula']))
                                # FormulaFunctionFlowChart()

                                for key in fl4:
                                    fl5[key] = FormulaFunctionFlowChartFinal(fl4[key], key, join_find_key_result[0][1][jk]['data']['data']['formula'])
                                    sourceKey = KeyFindOut(fl5[key][0]) 
                                         
                                # print("formula_data", formula_data)


            #     # if node_data[nd]['data']['type'] == 'filter' and node_data[nd]['data']['data']['filter']['sourceType'] == 'filter data' and node_data[nd]['data']['data']['filter']['sourceInfoType'] == 'json data':
            #     #     for k in fl4:
            #     #         # print("k", k)
            #     #         # print("k", fl4[k])
            #     #         fl5[k] = FilterFunctionFlowChartFinal(fl4[k], node_data[nd]['data']['data']['filter']["filterKey"], node_data[nd]['data']['data']['filter']["filterCon"], node_data[nd]['data']['data']['filter']["filterConValue"])


        # print("hello processType", processType)
        # print("hello fl1", fl1)
        return processType, fl1, fl2, fl3, fl4, fl5, sourceKey, dataType
        # return processType, finalData
        # return fl2
    except Exception as error:
        print("exception e", error)        
        

@api_view(['POST'])
def POSTFLOWCHARTDATAEDGEAPI(request):
    try:
        startTime = CurrentTimeFunc()

        # flow_data_items= []
        # processType = ""
        # formula = ""
        # source = []
        # sourceKey = []
        # sourceData = []
        # finalData = []
        node_data=[]
        flow_name = request.data['flow_name']
        flow_data = Table_data_info.objects.get(table_id=471, column_data=flow_name)
        flow_data_ref = Table_data_info.objects.filter(table_id=471, table_ref_id=flow_data.table_ref_id)
        for m in flow_data_ref:
            if m.table_col_id == 2:
                # node_data = eval(m.column_data)
                node_data = json.loads(m.column_data)
               
        # node_data = request.data['node_data']
        node = node_data['nodes']
        edge = node_data['edges']


        itemData = []
        sectionDic = {}
        medgeSourceIdBefore = ''
        medgeTargetIdBefore = ''
        beforePath = []

        count =0
        for e in edge:
            count +=1  
            key_to_find = e['source']
            results = find_key(sectionDic, key_to_find)

            if len(results) !=0:
                for path, value in results:
                    add_value(sectionDic, path+[e['target']], {})

         
            if count ==1:
                medgeSourceIdBefore = e['source']   
                medgeTargetIdBefore = e['target'] 
                add_value(sectionDic, [e['source'],  e['target']], {})

        secDic = {'target': ''}
        sourceItem = []
        data_section = {}
        target = ''
        for e in edge:
            if secDic['target'] == e['target']:
                target = e['target']
                edgeData = [x for x in edge if x['target'] == e['target']]
                for ed in edgeData:
                    sourceItem.append(ed['source'])

                nodeData = [x for x in node if x['id'] == e['target']]
                print("nodeData", nodeData)
                for nd in nodeData:
                    data_section = FilterTypeCheck(nd)
            else:
                secDic['target'] = e['target']
           
        sectionDic['merge_data'] = { 'source': list(set(sourceItem)), 'target': target, 'data': data_section }
 
        for n in node:
            key_to_find = n['id']
            results = find_key(sectionDic, key_to_find)
            if len(results) !=0:
                for path, value in results:
                    section = FilterTypeCheck(n)
                    modify_json_value(sectionDic, path+['data'], section)

        # print("sectionDic", sectionDic)            
        processType, fl1, fl2, fl3, fl4, fl5, sourceKey, dataType = FlowChartData(sectionDic)
        # print("processType", processType)
        return Response({'message':'success','status': status.HTTP_200_OK, 'dataType':dataType, 'sourceKey':sourceKey, 'data': sectionDic, 'fl1': fl1, 'fl2': fl2, 'fl3':fl3, 'fl4':fl4, 'fl5':fl5})
        # return Response({'message':'success','status': status.HTTP_200_OK, 'data': sectionDic})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


# Recursive function to traverse JSON
def traverse_json(data, prefix=""):
    flow_data_items= []
    processType = ""
    formula = ""
    source = []
    sourceKey = []
    sourceData = []
    finalData = []

    if isinstance(data, dict):
        for key, value in data.items():
            traverse_json(value, f"{prefix}.{key}" if prefix else key)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            traverse_json(value, f"{prefix}[{index}]")
    else:
        print(f"{prefix}: {data}")
        if data == "container":
            processType= data
            print("5591 processType", processType)
            # return processType

    # print("processType", processType)

def find_all_keys(data, parent_key=''):
    """
    Recursively find all keys in a nested JSON object.
    
    :param data: JSON object (dictionary or list)
    :param parent_key: Parent key (used for nested keys, optional)
    :return: List of keys
    """
    keys = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            keys.append(full_key)
            keys.extend(find_all_keys(value, full_key))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            full_key = f"{parent_key}[{index}]" if parent_key else f"[{index}]"
            keys.extend(find_all_keys(item, full_key))
    
    return keys


def find_all_keys_specific_key(data, key):
    """
    Recursively find all values of a given key in a nested JSON-like structure.
    """
    results = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                results.append(v)
            results.extend(find_all_keys_specific_key(v, key))
    elif isinstance(data, list):
        for item in data:
            results.extend(find_all_keys_specific_key(item, key))
    return results


# def find_depth(data):
#     if isinstance(data, dict):
#         return 1 + max((find_depth(value) for value in data.values()), default=0)
#     elif isinstance(data, list):
#         return 1 + max((find_depth(item) for item in data), default=0)
#     else:
#         return 0

# def find_depth(data):
#     data1={}
#     if isinstance(data, dict):
#         for k, v in data.items():
#             if k == 'data':
#                 pass 
#             else:
#                 data1[k] = v
#         return 1 + max((find_depth(value) for value in data1.values()), default=0)
#     elif isinstance(data, list):
#         return 1 + max((find_depth(item) for item in data1), default=0)
#     else:
#         return 0

def find_depth(data, depth=0):
    result = []
    
    # If data is a dictionary, iterate through its keys
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'data':
                pass
            else:    
                result.append((key, depth))  # Add key and current depth to result
                result.extend(find_depth(value, depth + 1))  # Recurse into the value with increased depth
    
    # If data is a list, iterate through its elements
    elif isinstance(data, list):
        for item in data:
            result.extend(find_depth(item, depth + 1))  # Recurse into list item with increased depth
    
    return result


@api_view(['POST'])
def POSTFLOWCHARTFINALAPI(request):
    try:
        flow_data_items= []
        processType = ""
        formula = ""
        source = []
        sourceKey = []
        sourceData = []
        finalData = []

        node_data = request.data['node_data']
        # print("node_data", node_data)
        # processType = traverse_json(node_data)
        # all_keys = find_all_keys(node_data)
        # for key in all_keys:
        #     print(key)
        #     print(key.split("."))
        # all_ids = find_all_keys_specific_key(node_data, "id")
        # print("all_ids", list(set(all_ids)))
        # print("processType", processType)
        for nd in node_data:
            print("nd", nd)
            if nd != "merge_data":
                print("node_data[nd]", node_data[nd])

                # depth = find_depth(node_data[nd])
                # print("Depth of JSON:", depth)

                if  node_data[nd]['data']['type'] == 'container':
                    # print("node_data[nd]['data']['type']['data']", node_data[nd]['data']['data'])
                    processType = node_data[nd]['data']['data']['container']['processType']
            
                for key in node_data[nd]:
                    print("key", key)
                    # if node_data[nd][key]['data']['type'] == 'source' and node_data[nd][key]['data']['data']['source']['sourceType'] == 'get data' and node_data[nd][key]['data']['data']['source']['sourceInfoType'] == 'get data':
                    #     print("node_data[nd][key]['data']['type']", node_data[nd][key]['data']['type'])
                    #     print("node_data[nd][key]['data']['data']", node_data[nd][key]['data']['data'])
                    #     print("sourceKey", node_data[nd][key]['data']['data']['source']["sourceKey"])
                    #     print("source", node_data[nd][key]['data']['data']['source']["source"])
                        # if nd['data']['source']['sourceType'] == 'get data' and nd['data']['source']['sourceInfoType'] == 'json data':
                        # sourceKey += nd['data']['source']["sourceKey"]
                        # source += nd['data']['source']['source']
                        # sourceData += SourceFunction(nd['data']['source']['source'])
                        # if node_data[nd][key]['data']['type'] == 'filter':
                        #     print("node_data[nd][key]['data']['type']", node_data[nd][key]['data']['type'])
                        #     print("node_data[nd][key]['data']['data']", node_data[nd][key]['data']['data'])
    

                   
                    if key != 'data':  
                        # print("node_data[nd][key]['data']['type']", node_data[nd][key]['data']['type'])
                        # print("node_data[nd][key]['data']['data']", node_data[nd][key]['data']['data']) 
                        print("node_data[nd][key]['data']['data']['source']['sourceType']", node_data[nd][key]['data']['data']['source']['sourceType']) 
                        # print("node_data[nd][key]['data']['data']['source']['sourceInfoType']", node_data[nd][key]['data']['data']['source']['sourceInfoType']) 
                        if node_data[nd][key]['data']['type'] == 'source' and node_data[nd][key]['data']['data']['source']['sourceType'] == 'get data' and node_data[nd][key]['data']['data']['source']['sourceInfoType'] == 'json data':
                            print("hello correct")
                        #     print("node_data[nd][key]['data']['type']", node_data[nd][key]['data']['type'])
                        #     # print("node_data[nd][key]['data']['data']", node_data[nd][key]['data']['data'])
                            # print("sourceKey", node_data[nd][key]['data']['data']['source']["sourceKey"])
                            # print("source", node_data[nd][key]['data']['data']['source']["source"])
                            sourceKey1 = node_data[nd][step1][step2][step3]['data']['source']["sourceKey"]
                            source1 = node_data[nd][step1][step2][step3]['data']['source']['source']
                            sourceData1 = SourceFunction(node_data[nd][step1][step2][step3]['data']['source']['source'])
                        
                        print("len key", len(node_data[nd][key]))
                        print("node_data[nd]", node_data[nd])
                        depth = find_depth(node_data[nd][key])
                        print("Depth of JSON:", depth)
                        for dp in depth[:-2]:
                            print("dp", dp)
                            print("dp[0]", dp[0])
                            key_to_find = dp[0]
                            results = find_key(node_data, key_to_find)

                            if len(results) !=0:
                                for path, value in results:
                                    print("path", path)
                                    print("value", value)
                                    print("value['data']", value['data'])
                                    print("value['data']['data']", value['data']['data'])

                                    if value['data']['type'] == 'filter' and value['data']['data']['filter']['sourceType'] == 'filter data' and value['data']['data']['filter']['sourceInfoType'] == 'json data':
                                        print("hello data")
                                        # source= source1+source2
                                        # sourceData = sourceData1+sourceData2
                                        # sourceData = FilterFunctionFlowChart(source, sourceData, node_data[nd][step1]['data']['filter']["filterKey"], node_data[nd][step1]['data']['filter']["filterCon"], node_data[nd][step1]['data']['filter']["filterConValue"])

                        # for m in range(depth):
                        #     print("m", m)
            if nd == "merge_data":
                print("node_data[nd]", node_data[nd])

        
        print("processType", processType)
        return Response({'message':'success','status': status.HTTP_200_OK})
        # return Response({'message':'success','status': status.HTTP_200_OK, 'data': sectionDic})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        


class FlowChartDataAPIVIEW(APIView, PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, processType, sourceKey, data, sourceData):
        return Response({
            'message':'success',
            'status': status.HTTP_200_OK, 
            "processType": processType,  
            "head": sourceKey,
            'count': self.page.paginator.count, 
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            "data": data, 
            "sourceData": sourceData
        })

    def get(self, request, flow_name):
        try:
            startTime = CurrentTimeFunc()

            APICALLFUNCTION('FlowChartDataAPIVIEW', 'null')

            flow_data_items= []
            processType = ""
            formula = ""
            source = []
            sourceKey = []
            sourceData = []
            finalData = []


        

            flow_data = Table_data_info.objects.get(table_id=544, column_data=flow_name)
            flow_data_ref = Table_data_info.objects.filter(table_id=544, table_ref_id=flow_data.table_ref_id)
            for m in flow_data_ref:
                if m.table_col_id == 1:
                    flow_data_items = eval(m.column_data)
            

            for fd in flow_data_items:
                for k in fd.keys():
                    if k == "sl" and fd[k] == 1:
                        if fd["stepType"] == "container":
                            processType= fd["processType"]
                        else:
                            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 1 container is not found'}, status=status.HTTP_400_BAD_REQUEST)  
                    if k == "sl" and fd[k] == 2:
                        if fd["stepType"] == "source" and fd["sourceType"] == "get data" and fd["sourceInfoType"] == "json data":
                            sourceKey= fd["sourceKey"]
                            source= fd["source"]
                            sourceData = SourceFunction(fd["source"])
                        else:
                            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 2 source is not found'}, status=status.HTTP_400_BAD_REQUEST)  
                    if k == "sl" and fd[k] == 3:
                        if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
                            sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
                        if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
                            formula = fd["stepType"]
                            sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])

                    if k == "sl" and fd[k] == 4:
                        if fd["stepType"] == "filter" and fd["sourceType"] == "filter data" and fd["sourceInfoType"] == "json data":
                            sourceData = FilterFunctionFlowChart(source, sourceData, fd["filterKey"], fd["filterCon"],  fd["filterConValue"])
                        if fd["stepType"] == "formula" and fd["sourceType"] == "formula data" and fd["sourceInfoType"] == "json data":
                            formula = fd["stepType"]
                            sourceData = FormulaFunctionFlowChart(sourceData, fd["formulaKey"])
               
           

            if formula == "formula":
                sourceData = SourceKeyFormulaFunction(sourceData, sourceKey)
            else:
                sourceData = SourceKeyFunction(sourceData, sourceKey)

            if processType == "linebarchart":
                finalData = LineChartFlowChartFunctionTWO(sourceData, sourceKey)
                
                endTime = CurrentTimeFunc()
                loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(finalData)
                DataFetch_Static("FlowChartDataAPIVIEW", "json flowchart linebarchart data", value_count, round(loadTime, 6))
                
                return Response({'message':'success','status': status.HTTP_200_OK, "processType": processType, "data": finalData, "sourceData": sourceData})

            if processType == "tabularblock":
                finalData = TabularBlockFlowChartFunction(sourceData, sourceKey)
                
                endTime = CurrentTimeFunc()
                loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(finalData)
                DataFetch_Static("FlowChartDataAPIVIEW", "json flowchart tabularblock data", value_count, round(loadTime, 6))

                results = self.paginate_queryset(finalData, request, view=self)
                return self.get_paginated_response(processType, sourceKey, results, sourceData)
                
            if processType == 'TabularSingleBlog':
                finalData = TabularSingleBlogFunction(sourceData, sourceKey)
                
                endTime = CurrentTimeFunc()
                loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(finalData)
                DataFetch_Static("FlowChartDataAPIVIEW", "json flowchart TabularSingleBlog data", value_count, round(loadTime, 6))
                
                
                results = self.paginate_queryset(finalData, request, view=self)
                return self.get_paginated_response(processType, sourceKey, results, sourceData)    

       

        except Exception as err:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
            
            
            
@api_view(['GET'])
def GETUIAPI(request, api_name, user):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('GETUIAPI', 'null')
      
        TableDataRef = []
        Data = []
        func_name = ""
        username = ""
        api_name_value = Table_data_info.objects.filter(table_id=579, table_col_id=1, column_data=api_name)
        if len(api_name_value) != 0:
            for m in api_name_value:
                TableDataRef += Table_data_info.objects.filter(table_id=579, table_ref_id=m.table_ref_id)

        for k in TableDataRef:
            if k.table_id == 579 and k.table_col_id==3:
                if k.column_data == "UIGETAPI1":
                    func_name = k.column_data
                if k.column_data == "UIGETAPI2":
                    func_name = k.column_data

            if k.table_id == 579 and k.table_col_id==4:
                if k.column_data == user:
                    username = k.column_data   
                          

            if k.table_id == 579 and k.table_col_id==7:
                if k.column_name == "api_parameter" and func_name == "UIGETAPI1" and username == user:
                    Data = UIGETAPI1(user, api_name, eval(k.column_data))    
                if k.column_name == "api_parameter" and func_name == "UIGETAPI2" and username == user:
                    Data = UIGETAPI2(user, api_name, eval(k.column_data))    
             
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(Data)
        DataFetch_Static("GETUIAPI", "GETUIAPI function", value_count, round(loadTime, 6))

        return Response({'status': status.HTTP_200_OK, "message":"success", "data": Data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
@api_view(['GET'])
def CUSTOM2UIAPI(request, api_name, user):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('CUSTOM2UIAPI', 'null')
      
        TableDataRef = []
        Data = []
        func_name = ""
        username = ""
        api_name_value = Table_data_info.objects.filter(table_id=579, table_col_id=1, column_data=api_name)
        if len(api_name_value) != 0:
            for m in api_name_value:
                TableDataRef += Table_data_info.objects.filter(table_id=579, table_ref_id=m.table_ref_id)

        for k in TableDataRef:
            if k.table_id == 579 and k.table_col_id==3:
                if k.column_data == "CustomTest":
                    func_name = k.column_data
              

            if k.table_id == 579 and k.table_col_id==4:
                if k.column_data == user:
                    username = k.column_data   
                          

            if k.table_id == 579 and k.table_col_id==7:
                if k.column_name == "api_parameter" and func_name == "CustomTest" and username == user:
                    Data = Custom2(user, api_name, eval(k.column_data))    
                 
             
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(Data)
        DataFetch_Static("CUSTOM2UIAPI", "CUSTOM2UIAPI function", value_count, round(loadTime, 6))

        return Response({'status': status.HTTP_200_OK, "message":"success", "data": Data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def POSTUIAPI(request, api_name, user):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('POSTUIAPI', 'null')
        
        TableDataRef = []
        Data = []
        func_name = ""
        username = ""
        api_name_value = Table_data_info.objects.filter(table_id=579, table_col_id=1, column_data=api_name)
        if len(api_name_value) != 0:
            for m in api_name_value:
                TableDataRef += Table_data_info.objects.filter(table_id=579, table_ref_id=m.table_ref_id)

        for k in TableDataRef:
            if k.table_id == 579 and k.table_col_id==3:
                if k.column_data == "UIPOSTAPI":
                    func_name = k.column_data
  
            if k.table_id == 579 and k.table_col_id==4:
                if k.column_data == user:
                    username = k.column_data   
                          

            if k.table_id == 579 and k.table_col_id==7:
                if k.column_name == "api_parameter" and func_name == "UIPOSTAPI" and username == user:
                    Data = UIPOSTAPI(user, api_name, eval(k.column_data))    
                     

    
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(Data)
        DataFetch_Static("POSTUIAPI", "POSTUIAPI function", value_count, round(loadTime, 6))
        
        return Response({'status': status.HTTP_200_OK, "message":"success", "data": Data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  



@api_view(['GET'])
def AllFlowChartNameAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('AllFlowChartNameAPI', 'null')
        
        finalData = []
        refId = []
        sections = {}
        flow_data = Table_data_info.objects.filter(table_id=544)

        for k in flow_data:
            refId.append(k.table_ref_id)
                   
        refId = list(set(refId))

        for m in refId:
            for i in flow_data:
                if i.table_ref_id==m:
                    if i.table_col_id == 1:
                        flow_data_items = eval(i.column_data)
                        for fd in flow_data_items:
                            for k in fd.keys():
                                if k == "flowchart_name":
                                    if fd["flowchart_name"]:
                                        sections['flowchart_name'] = fd["flowchart_name"]
                                    else:
                                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'flowchart_name is not found'}, status=status.HTTP_400_BAD_REQUEST)  
                
                                if k == "sl" and fd[k] == 1:
                                    if fd["stepType"] == "container":
                                        sections['processType'] = fd["processType"]
                                    else:
                                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'step 1 container is not found'}, status=status.HTTP_400_BAD_REQUEST)  
                
            if sections != "":
                finalData.append(sections)   
                sections = {}      


        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(finalData)
        DataFetch_Static("AllFlowChartNameAPI", "AllFlowChartNameAPI function", value_count, round(loadTime, 6))

        return Response({'message':'success','status': status.HTTP_200_OK, "data": finalData })


    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
class YahooHistFileNameAPIVIEW(APIView, PageNumberPagination):
    page_size = 15

    def get(self, request):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('YahooHistFileNameAPIVIEW', 'null')
            fileName = main_media_url+'/media/upload_file/yahoo_finance_hist'
            dir_list = os.listdir(fileName)

            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(dir_list)
            DataFetch_Static("YahooHistFileNameAPIVIEW", "YahooHistFileName function", value_count, round(loadTime, 6))
        
            results = self.paginate_queryset(dir_list, request, view=self)
            return self.get_paginated_response(results)

        except Exception as err:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


class YahooInfoFileNameAPIVIEW(APIView, PageNumberPagination):
    page_size = 15

    def get(self, request):
        try:
            startTime = CurrentTimeFunc()
            APICALLFUNCTION('YahooInfoFileNameAPIVIEW', 'null')
            item = []
            section = {}
            fileName = main_media_url+'/media/upload_file/yahoo_finance'
            dir_list = [os.path.splitext(filename)[0] for filename in os.listdir(fileName)]
            
            for m in dir_list:
                section['symbol'] = m
                if len(section) != 0:
                    item.append(section)
                    section = {}
                    
            endTime = CurrentTimeFunc()
            loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
            value_count = ValueCountFunc(item)
            DataFetch_Static("YahooInfoFileNameAPIVIEW", "YahooInfoFileName function", value_count, round(loadTime, 6))        

            results = self.paginate_queryset(item, request, view=self)
            return self.get_paginated_response(results)

        except Exception as err:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])
def SearchLikeAPI(request, search_key):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('SearchLikeAPI', 'null')
        
        item = []
        # fileName = '/home/itbusaah/idriver_education_djangoproject/media/upload_file/yahoo_finance'
        # dir_list = [os.path.splitext(filename)[0] for filename in os.listdir(fileName)]
        
        file_name_list = JsonFileNameYahooFinanceInfo()
        dir_list = [os.path.splitext(filename)[0] for filename in file_name_list]

        item = [idx for idx in dir_list if idx[0].lower() == search_key.lower() or idx[0:2].lower() == search_key.lower() or idx[0:3].lower() == search_key.lower()]  
       
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(item)
        DataFetch_Static("SearchLikeAPI", "SearchLike function", value_count, round(loadTime, 6)) 
           
        return Response({'status': status.HTTP_200_OK, "data":[{'symbol': item}]})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  



        

@api_view(['POST'])
def WathListNameAPI(request):
    try:
        
        APICALLFUNCTION('WathListNameAPI', 'null')
        
        user_id = request.data['user_id']
        watchlist_name = request.data['watchlist_name']
        now_utc = datetime.utcnow()
        time = datetime.strftime(now_utc, '%Y-%m-%d %H:%M:%S')
        count_number = Table_data_info.objects.filter(table_id=580).count()
        watchlist = Table_data_info.objects.filter(table_id=580, column_data=watchlist_name)
        for m in watchlist:
            watchlist = Table_data_info.objects.filter(table_id=580, table_ref_id=m.table_ref_id)
            if len(watchlist) != 0:
                for w in watchlist:
                    if w.table_id == 580 and w.table_col_id ==1 and w.column_data == user_id:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Watchlist name already exists.'}, status=status.HTTP_400_BAD_REQUEST)  

        Table_data_info.objects.create(table_id=580, table_col_id=1, user_id=user_id, column_data=user_id, table_ref_id=count_number+1, col_data_type="String", column_name='user_id') 
        Table_data_info.objects.create(table_id=580, table_col_id=2, user_id=user_id, column_data=watchlist_name, table_ref_id=count_number+1, col_data_type="String", column_name='watchlist_name') 
        Table_data_info.objects.create(table_id=580, table_col_id=3, user_id=user_id, column_data=time, table_ref_id=count_number+1, col_data_type="String", column_name='time') 
       

        return Response({'status': status.HTTP_200_OK, "message":"Watchlist name created sucessfully"})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def WathListItemNameAPI(request):
    try:
        APICALLFUNCTION('WathListItemNameAPI', 'null')
        
        user_id = request.data['user_id']
        watchlist_item_name = request.data['watchlist_item_name']
        symbol = request.data['symbol']

        count_number = Table_data_info.objects.filter(table_id=581).count()
        watchlist = Table_data_info.objects.filter(table_id=581, column_data=watchlist_item_name)

        for m in watchlist:
            watchlist = Table_data_info.objects.filter(table_id=581, user_id=user_id, table_ref_id=m.table_ref_id)
            if len(watchlist) != 0:
                for w in watchlist:
                    if w.table_id == 581 and w.table_col_id ==3 and w.column_name == "flag" and w.table_ref_id == w.table_ref_id and w.column_data=="True" and w.user_id == user_id:
                        watch_data = Table_data_info.objects.get(table_id=581, table_col_id=w.table_col_id, column_data=w.column_data, table_ref_id=w.table_ref_id)
                        watch_data.column_data = "False"
                        watch_data.save()
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Watchlist item name remove sucessfully.'}, status=status.HTTP_400_BAD_REQUEST)  
                    
                    if w.table_id == 581 and w.table_col_id ==3 and w.column_name == "flag" and w.table_ref_id == w.table_ref_id and w.column_data=="False" and w.user_id == user_id:
                        watch_data = Table_data_info.objects.get(table_id=581, table_col_id=w.table_col_id, column_data=w.column_data, table_ref_id=w.table_ref_id)
                        watch_data.column_data = "True"
                        watch_data.save()
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Watchlist item name added sucessfully.'}, status=status.HTTP_400_BAD_REQUEST)  

        Table_data_info.objects.create(table_id=581, table_col_id=1, user_id=user_id, column_data=watchlist_item_name, table_ref_id=count_number+1, col_data_type="String", column_name='watchlist_item_name') 
        Table_data_info.objects.create(table_id=581, table_col_id=2, user_id=user_id, column_data=symbol, table_ref_id=count_number+1, col_data_type="String", column_name='symbol') 
        Table_data_info.objects.create(table_id=581, table_col_id=3, user_id=user_id, column_data="True", table_ref_id=count_number+1, col_data_type="Boolean", column_name='flag') 
       

        return Response({'status': status.HTTP_200_OK, "message":"Watchlist item name added sucessfully"})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
        
@api_view(['POST'])
def CurrentPriceHistoricalDataAPI(request):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('CurrentPriceHistoricalDataAPI', 'null')
        
        symbol = request.data['symbol']
        data = CurrentPriceHistoricalData(symbol)
        
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(data)
        DataFetch_Static("CurrentPriceHistoricalDataAPI", "CurrentPriceHistoricalData function", value_count, round(loadTime, 6))
        

        return Response({'status': status.HTTP_200_OK, "message":"Data is found", "data": data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
@api_view(['GET'])
def GETDynamicTableJsonFieldAPI(request, table_id):
    try:
        startTime = CurrentTimeFunc()
        APICALLFUNCTION('GETDynamicTableJsonFieldAPI', 'null')
         
        dataJson = JsonDynamicModel.objects.filter(table_id=table_id)
        serializer = GETDynamicTableJsonFieldSerializer(dataJson, many=True)
        
        endTime = CurrentTimeFunc()
        loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
        value_count = ValueCountFunc(serializer.data)
        DataFetch_Static("GETDynamicTableJsonFieldAPI", "GETDynamicTableJsonField function", value_count, round(loadTime, 6))
       

        return Response({'status': status.HTTP_200_OK, "message":"Data is found", "data": serializer.data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
                
                
# @api_view(['GET'])
# def SearchNewsDataAPI(request):
#     try:
#         string = request.data['string']
#         data = SearchNews(string)

#         return Response({'status': status.HTTP_200_OK, "message":"Data is found", "data": data})
#     except Exception as err:
#         return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)


def lobby(request):
    return render(request, 'chat/lobby.html')
    
    
    
@api_view(['POST'])
def ChangeLogAPI(request):
    try:
        gm = time.strftime("%a, %d %b %Y %X",
                        time.gmtime())
        currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
        currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%d-%m-%Y %H:%M:%S')

        folder_path = request.data['folder_path']
        api_url = request.data['api_url']


        fileName = main_media_url+'/media/upload_file/investing/json/change_log.json'
        # ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/change_log.json', api_url=main_url+f'/media/upload_file/investing/json/change_log.json')

        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
          
            compareValue = [x for x in array_data if x['folder_path'] == folder_path]
            if len(compareValue)!=0:
                for j in range(len(array_data)):
                    if array_data[j]['folder_path'] ==  folder_path:
                        array_data[j]['response_time'] = currenttimedate
                        array_data[j]['folder_path'] = folder_path
                        array_data[j]['api_url'] = api_url
                        file_data={}
                        with open(fileName, 'w', encoding='utf-8') as file:
                            file_data["data"]=array_data
                            json.dump(file_data, file, indent=4)
                
                    
            else:            
                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "response_time": currenttimedate,
                    "folder_path": folder_path,
                    "api_url": api_url,
                }

                write_json(y)

        return Response({'message':'Change Log Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors {err}'}, status=status.HTTP_400_BAD_REQUEST)  
    

@api_view(['POST'])
def CodeJsonWriteAPI(request):
    try:
        gm = time.strftime("%a, %d %b %Y %X",
                        time.gmtime())
        currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
        currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%d-%m-%Y')

        
        user = request.data['user']
        job_name = request.data['job_name']
        code = request.data['code']
        


        fileName = main_media_url+f'/media/upload_file/investing/json/code.json'
        ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/code.json', api_url=main_url+f'/media/upload_file/investing/json/code.json')

        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
        
            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    
                    
                    
                    
                    
                    
                    
                    json.dump(file_data, file, indent=4)
            y = {
                "user": user,
                "job_name": job_name,
                "code": code,
            }

            write_json(y)
            
            table_ref_id_count = Table_data_info.objects.filter(table_id=612).count()  

            user1 = Table_data_info(table_id=612, table_col_id=1, user_id="", column_data=user, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='user') 
            user1.save()  
            job_name1 = Table_data_info(table_id=612, table_col_id=2, user_id="", column_data=job_name, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='job_name') 
            job_name1.save()  
            code1 = Table_data_info(table_id=612, table_col_id=3, user_id="", column_data=code, table_ref_id=table_ref_id_count+1, col_data_type="String", column_name='code') 
            code1.save()  

        return Response({'message':'Code josn Added Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
        
        
@api_view(['GET'])
def JobDataAPI(request, job_name):
    try:
        # sections = {}
        # items = []
        # refId = []
        # filter_data = Table_data_info.objects.filter(table_id=612)
        # for k in filter_data:
        #     refId.append(k.table_ref_id)
                    
        # refId = list(set(refId))

        # for m in refId:
        #     for i in filter_data:
        #         if i.table_ref_id==m:
        #             sections[i.column_name]=i.column_data
        #             sections['table_ref_id']=i.table_ref_id
        #     if sections != "":
        #         items.append(sections)   
        #         sections = {}
        fileName = main_media_url+f'/media/upload_file/investing/json/casual_process_code.json'
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            casual_code = data['data']
            # print("casual_code", casual_code)  
            job_data = [x for x in casual_code if x['Process_Name'] == job_name]
            return Response({'message':"success",'status': status.HTTP_200_OK, "job_data": job_data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)                        




@api_view(['GET'])
def JobDeleteAPI(request):
    try:
        sections = {}
        items = []
        refId = []
        filter_data = Table_data_info.objects.filter(table_id=542)
        for k in filter_data:
            refId.append(k.table_ref_id)
                    
        refId = list(set(refId))

        for m in refId:
            for i in filter_data:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_ref_id']=i.table_ref_id
            if sections != "":
                items.append(sections)   
                sections = {}

        # print("items", items)    
        job_data = [x for x in items if x['Process_Status'] == 'Done' or x['Process_Status'] == 'Cancel' or x['Process_Status'] == 'Overtime']
        if len(job_data)!=0:
            for jd in job_data:
                record = Table_data_info.objects.filter(table_id=542, table_ref_id=jd['table_ref_id'])
                if record:
                    for r in record:
                        table_data = Table_data_info.objects.get(table_data_id=r.table_data_id)
                        table_data.delete()

        return Response({'status': status.HTTP_200_OK, 'message':"Job Deleted Successfully"})
        # return Response({'message':"success",'status': status.HTTP_200_OK, "job_data": job_data})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)                        
                


from media.upload_file.process.CustomABC import *

@api_view(['GET'])
def CustomABCAPI(request):
    try:
        job_name = request.data['job_name']
        Custom(job_name)       
        return Response({'status': status.HTTP_200_OK, 'message':"success"})
    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)    
        
        
        
@api_view(['DELETE'])
def ChangeLogDeleteAPI(request):
    try:
        gm = time.strftime("%a, %d %b %Y %X",
                        time.gmtime())
        currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
        currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%d-%m-%Y')

        folder_path = request.data['folder_path']

        fileName = main_media_url+f'/media/upload_file/investing/json/change_log.json'
        ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/change_log.json', api_url=main_url+f'/media/upload_file/investing/json/change_log.json')

        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
          
            compareValue = [x for x in array_data if x['folder_path'] != folder_path]
            file_data={}
            with open(fileName, 'w', encoding='utf-8') as file:
                file_data["data"]=compareValue
                json.dump(file_data, file, indent=4)

            

        return Response({'message':'Change Log Deleted Successfully','status': status.HTTP_200_OK},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
@api_view(['POST'])
def PipeLineAPICreateCodeWriteAPI(request):
    try:

        print("5334")

        gm = time.strftime("%a, %d %b %Y %X",
                        time.gmtime())
        currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
        currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%d-%m-%Y')

        print("5343")
        
        user = request.data['user']
        api_name = request.data['api_name']
        api_url = request.data['api_url']
        api_method = request.data['api_method']
        api_data_fetch_type = request.data['api_data_fetch_type']
        code = request.data['code']

        print("5352")

        # paramList = eval(request.data['paramList'])

       

        paramList=""
        try:
            paramList = eval(request.data['paramList'])
        except:
            paramList=request.data['paramList']

        print("5356 paramList", paramList)    
        
        # a=''
        # b=''

        # num1=1
        # num2=1
        
        # for key, values in paramList.items():
        #     if key == 'a':
        #         if type(values) == str:
        #             a = values
        #         elif type(values) == int:  
        #             num1=values
        #     if key == 'b':
        #         if type(values) == str:
        #             b = values
        #         elif type(values) == int:  
        #             num2=values
                    
        # if len(a) != 0 and len(b)!=0:
        final_code = f'''
{code}
            '''
#             final_code = f'''
# a='{a}'
# b='{b}'
# {code}
#             '''
#         else:           
#             final_code = f'''
# {code}
#             '''
#             final_code = f'''
# a={num1}
# b={num2}
# {code}
#             '''
      

       

        fileName = main_media_url+f'/media/upload_file/investing/json/pipelineapicreatecode.json'
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
            compareValue = [x for x in array_data if x['api_name'] == api_name and x['user'] == user]
            if len(compareValue)!=0:
                for j in range(len(array_data)):
                    if array_data[j]['api_name'] ==  api_name and array_data[j]['user'] ==  user:
                        array_data[j]['user'] = user
                        array_data[j]['api_name'] = api_name
                        array_data[j]['api_url'] = api_url
                        array_data[j]['api_method'] = api_method
                        array_data[j]['api_data_fetch_type'] = api_data_fetch_type
                        array_data[j]['code'] = final_code
                        array_data[j]['paramList'] = paramList
                        file_data={}
                        with open(fileName, 'w', encoding='utf-8') as file:
                            file_data["data"]=array_data
                            json.dump(file_data, file, indent=4)
            
            else:
                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                y = {
                    "user": user,
                    "api_name": api_name,
                    "api_url": api_url,
                    "api_method": api_method,
                    "api_data_fetch_type": api_data_fetch_type,
                    "code": final_code,
                    "paramList": paramList,
                }
    
                write_json(y)
            
        return Response({'message':'PipeLine Api created or updated Successfully','status': status.HTTP_200_OK},)
        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
@api_view(['POST'])
def MultiPipeLineAPI(request):
    try:
        gm = time.strftime("%a, %d %b %Y %X",
                        time.gmtime())
        currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
        currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%d-%m-%Y')

        
        user = request.data['user']
        pipeline_name = request.data['pipeline_name']
        code = request.data['code']
        paramList = eval(request.data['paramList'])
        
        a=0
        b=0

        for key, values in paramList.items():
            fileName = main_media_url+f'/media/upload_file/investing/json/multi_pipeline_code.json'
            if os.path.isfile(fileName):
                f = open(fileName)
                data = json.load(f)
                array_data = data['data']

                dataT = [x for x in array_data if x['pipeline_name'] == values and x['user'] == user]
                if len(dataT)!=0:
                    if key == 'a':
                        a = dataT[0]['output']
                    if key == 'b':
                        b = dataT[0]['output']
                else:
                    if key == 'a':
                        a = values
                    if key == 'b':
                        b = values


        





        final_code = f'''
a={a}
b={b}
{code}
        '''
     



    
        loc = {}
        exec(final_code,  globals(), loc)    
   

        fileName = main_media_url+f'/media/upload_file/investing/json/multi_pipeline_code.json'
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
        
            
            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            y = {
                "user": user,
                "pipeline_name": pipeline_name,
                "code": final_code,
                "output": loc['result'],
                "paramList": paramList,
            }
    
            write_json(y)

        return Response({'message':'Pipeline Created Successfully','status': status.HTTP_201_CREATED},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
        
# @api_view(['GET'])
@api_view(['POST'])
def GETUIDynamicAPI(request, api_name, user):
    try:
        sections = {}
        items = []
        refId = []

        print("5531 request.data", request.data)
        
        paramList=""
        try:
            paramList = eval(request.data['paramList'])
        except:
            paramList=request.data
        # print("5531 request.data", request.data)
        # paramList = request.data['paramList']
        print("5531 paramList", paramList)
        
        # a=''
        # b=''

        # num1=1
        # num2=1
        
        # for key, values in paramList.items():
        #     if key == 'a':
        #         if type(values) == str:
        #             a = values
        #         elif type(values) == int:  
        #             num1=values
        #     if key == 'b':
        #         if type(values) == str:
        #             b = values
        #         elif type(values) == int:  
        #             num2=values
                    
        # if len(a) != 0 and len(b)!=0:
        #     a = a
        #     b = b
        # else: 
        #     a=num1          
        #     b=num2          


        print("5560")
        api_name_value = Table_data_info.objects.filter(table_id=579)
        for k in api_name_value:
            refId.append(k.table_ref_id)
                    
        refId = list(set(refId))

        for m in refId:
            for i in api_name_value:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_ref_id']=i.table_ref_id
            if sections != "":
                items.append(sections)   
                sections = {}

        item_data = [x for x in items if x['api_name'] == api_name and x['user'] == user] 
        print("5582 item_data paramList", item_data, paramList)
        api_code_obj = ApiCodeRun(item_data, paramList)
        result_dict=api_code_obj.api_code_result
        print("result_dict", result_dict)
       
        # g_obj = GlobalJson(main_media_url+f'/media/upload_file/investing/json/global_parameter.json')

        # global_parameter=g_obj.var1
         
       
        # fileName = main_media_url+f'/media/upload_file/investing/json/pipelineapicreatecode.json'
        # if os.path.isfile(fileName):
        #     f = open(fileName)
        #     data = json.load(f)
        #     array_data = data['data']

        #     result_dict = {}

        #     for id in item_data:
        #         item_arr_data = [x for x in array_data if x['api_name'] == id['api_name'] and x['user'] == id['user'] and x['api_url'] == id['api_url'] and x['api_method'] == id['api_file'] and x['api_data_fetch_type'] == id['api_data_fetch_type']] 
        #         for m in item_arr_data:
        #             loc = paramList
        #             # loc = {'a': a,'b': b}
        #             print("5594")
        #             # abc={'Table_data_info': Table_data_info, 'main_media_url': main_media_url, 'os': os, 'json': json}
        #             globals = eval(global_parameter)
        #             exec(m['code'], globals, loc) 
        #             # exec(m['code'], globals(), loc) 
        #             # exec(m['code'], {'a':a, 'b':b}, loc) 
        #             print("5598")

        #             result_dict['result']=loc['result']

                     
        return Response({'status': status.HTTP_200_OK, "message":"success", "data": result_dict})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  

        
@api_view(['DELETE'])
def PipeLineDeleteAPI(request, api_name, user):
    try:
        gm = time.strftime("%a, %d %b %Y %X",
                        time.gmtime())
        currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
        currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%d-%m-%Y')

        

        fileName = main_media_url+f'/media/upload_file/investing/json/pipelineapicreatecode.json'
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            
          
            compareValue = [x for x in array_data if x['api_name'] != api_name]
            # compareValue = [x for x in array_data if x['api_name'] != api_name and x['user'] != user]
            file_data={}
            with open(fileName, 'w', encoding='utf-8') as file:
                file_data["data"]=compareValue
                json.dump(file_data, file, indent=4)


        return Response({'message':'Data Deleted Successfully','status': status.HTTP_200_OK},)
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
@api_view(['GET'])
def GETALLTABLECOLUMN(request):
    try:
        tableItem = []
        tableSections = {}
        columnItem = []
        columnSections = {}
        table_info = Table_info_dtl.objects.all().order_by('-table_id')

        for t in table_info:
            print("1357 t", t.table_id, t.table_name)
            tableSections['table']=t.table_name
            tableSections['id']=t.table_id

            table_col_info = Table_col_info.objects.filter(table_id=t.table_id)
            print("1365 table_col_info", table_col_info)
            for c in table_col_info:
                print("1367 c", c.table_col_id, c.column_name)
                columnSections['no']=c.table_col_id
                columnSections['name']=c.column_name
                if len(columnSections)!=0:
                    columnItem.append(columnSections)
                    columnSections={}
            print("1373", columnItem)        
            tableSections['column']=columnItem       
            if len(tableSections)!=0:
                tableItem.append(tableSections)
                tableSections={}
                columnItem=[]

        return Response({'message':"success",'status': status.HTTP_200_OK, "data": tableItem})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)
    
@api_view(['POST'])
def ServerProcessApi(request):
    try:
        DataList = []
        fileName = main_media_url+f'/media/upload_file/investing/json/casual_process.json'
        ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/casual_process.json', api_url=main_url+f'/media/upload_file/investing/json/casual_process.json')
        
        DataList.append(request.data)

        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']


            for i in DataList:
                compareValue = [x for x in array_data if x['Process_Id'] == i['Process_Id'] and x['Process_Name'] == i['Process_Name'] and x['Time'] == i['Time']]
                if len(compareValue)!=0:
                    for j in range(len(array_data)):
                        if array_data[j]['Process_Id'] ==  i['Process_Id'] and array_data[j]['Process_Name'] ==  i['Process_Name'] and array_data[j]['Time'] ==  i['Time']:
                            array_data[j]['Process_Name'] = i['Process_Name']
                            array_data[j]['Schedule'] = i['Schedule']
                            array_data[j]['Start_Date'] = i['Start_Date']
                            array_data[j]['End_Date'] = i['End_Date']
                            array_data[j]['Time'] = i['Time']
                            array_data[j]['Process_Id'] = i['Process_Id']
                            array_data[j]['Process_Status'] = "Done"
                            array_data[j]['Process_Type'] = i['Process_Type']
                            array_data[j]['Process_Relation'] = i['Process_Relation']
                            array_data[j]['Flowchart_Name'] = i['Flowchart_Name']
                            array_data[j]['Process_Code'] = i['Process_Code']
                            array_data[j]['Function_Name'] = i['Function_Name']
                            array_data[j]['Server_Name'] = i['Server_Name']
                
                            file_data={}
                            with open(fileName, 'w', encoding='utf-8') as file:
                                file_data["data"]=array_data
                                json.dump(file_data, file, indent=4)

                else:          
                    def write_json(new_data, filename=fileName):
                        with open(filename, 'r+') as file:
                            file_data = json.load(file)
                            file_data["data"].append(new_data)
                            file.seek(0)
                            json.dump(file_data, file, indent=4)
                
                    y = {
                        "Process_Name": i['Process_Name'],
                        "Schedule": i['Schedule'],
                        "Start_Date": i['Start_Date'],
                        "End_Date": i['End_Date'],
                        "Time": i['Time'],
                        "Process_Id": i['Process_Id'],
                        "Process_Status": i['Process_Status'],
                        "Process_Type": i['Process_Type'],
                        "Process_Relation": i['Process_Relation'],
                        "Flowchart_Name": i['Flowchart_Name'],
                        "Process_Code": i['Process_Code'],
                        "Function_Name": i['Function_Name'],
                        "Server_Name": i['Server_Name'],
                    }

                    write_json(y)




        # if os.path.isfile(fileName):
        #     def write_json(new_data, filename=fileName):
        #         with open(filename, 'r+') as file:
        #             file_data = json.load(file)
        #             file_data["data"].append(new_data)
        #             file.seek(0)
        #             json.dump(file_data, file, indent=4)

             
        #     write_json(request.data)    
        return Response({'message':"Server Process Successfully created.",'status': status.HTTP_200_OK})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def ServerProcessCodeApi(request):
    try:
        User = request.data['User']
        Process_Name = request.data['Process_Name']
        Code = request.data['Code']
        fileName = f'/home/ubuntu/idriver_education_djangoproject/media/upload_file/investing/json/casual_process_code.json'
        ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/casual_process_code.json', api_url=main_url+f'/media/upload_file/investing/json/casual_process_code.json')
        if os.path.isfile(fileName):
            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)

            y={
                "User":User,
                "Process_Name":Process_Name,
                "Code":Code,
            } 
            write_json(y)    
        return Response({'message':"Server Process Code Successfully created.",'status': status.HTTP_200_OK})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        

def ProcessDataFunction(Process_Name):
    try:
        sections = {}
        items = []
        refId = []
        filter_data = Table_data_info.objects.filter(table_id=542)
        for k in filter_data:
            refId.append(k.table_ref_id)
                    
        refId = list(set(refId))

        for m in refId:
            for i in filter_data:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_ref_id']=i.table_ref_id
            if sections != "":
                items.append(sections)   
                sections = {}
                
        process_data = [x for x in items if x['Process_Name'] == Process_Name]
        # process_data = [x for x in items if x['Process_Name'] == Process_Name and x['Process_Id'] == Process_Id]


        return process_data
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
@api_view(['POST'])
def ServerProcessJsonGETUpdateDelete(request):
    try:
     

        paramList = eval(request.data['paramList'])
        Action = request.data['Action']

        DataItem=[]
        
        fileName = main_media_url+f'/media/upload_file/investing/json/process_log1.json'
        ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/process_log1.json', api_url=main_url+f'/media/upload_file/investing/json/process_log1.json')
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['process_log1']

        DataF=array_data

        if Action == 'GET':
            for keys, values in paramList.items():
                dataT = [x for x in DataF if x[keys].find(values) != -1]
                DataF = dataT

                for p in DataF:
                    processData = ProcessDataFunction(p['Process_Name'])
                    # processData = ProcessDataFunction(p['Process_Name'], p['Process_Id'].split('-')[0])
                    p['Schedule'] = processData[0]['Schedule']
                    p['Start_Date'] = processData[0]['Start_Date']
                    p['End_Date'] = processData[0]['End_Date']
                    p['Process_Type'] = processData[0]['Process_Type']
                    p['Process_Relation'] = processData[0]['Process_Relation']
                    p['Flowchart_Name'] = processData[0]['Flowchart_Name']
                    p['Process_Code'] = processData[0]['Process_Code']
                    p['Function_Name'] = processData[0]['Function_Name']
                    DataItem.append(p)

               
            return Response({'message':"success",'status': status.HTTP_200_OK, "data": DataItem})
        
        if Action == 'GET5':
            now_utc = datetime.utcnow()
            now_utc1 = datetime.utcnow()+timedelta(minutes = 5)
            currenttimedate = datetime.strftime(now_utc, '%Y-%m-%d %H:%M:%S')
            currenttimedate2 = datetime.strftime(now_utc1, '%Y-%m-%d %H:%M:%S')
            currenttimestamp = datetime.strptime(currenttimedate, "%Y-%m-%d %H:%M:%S").timestamp()
            currenttimestamp2 = datetime.strptime(currenttimedate2, "%Y-%m-%d %H:%M:%S").timestamp()
            for keys, values in paramList.items():
                dataT = [x for x in DataF if x[keys].find(values) != -1]
                DataF = dataT
            
            for i in DataF:
                runtimestamp = datetime.strptime(i['RunTime'], "%Y-%m-%d %H:%M:%S").timestamp()
                if runtimestamp >= currenttimestamp:
                    if runtimestamp <= currenttimestamp2:
                        processData = ProcessDataFunction(i['Process_Name'])
                        i['Schedule'] = processData[0]['Schedule']
                        i['Start_Date'] = processData[0]['Start_Date']
                        i['End_Date'] = processData[0]['End_Date']
                        i['Process_Type'] = processData[0]['Process_Type']
                        i['Process_Relation'] = processData[0]['Process_Relation']
                        i['Flowchart_Name'] = processData[0]['Flowchart_Name']
                        i['Process_Code'] = processData[0]['Process_Code']
                        i['Function_Name'] = processData[0]['Function_Name']
                        DataItem.append(i)
                        


               
            return Response({'message':"success",'status': status.HTTP_200_OK, "data": DataItem})
        
        if Action == 'UPDATE':
            index=[]
            for keys, values in paramList.items():

                if keys == 'From':
                    count = len(list(values))
                    loop_count = 0
                    for keyf1, valuesf1 in values.items():
                        loop_count+=1
                        if count == loop_count:
                            for j in range(len(DataF)):
                                if DataF[j][keyf1] == valuesf1:
                                    index.append(j)


                if keys == 'To':
                    DataValue=[]
                    section={}
                    DataValue.append(values)
                    section['process_log1']=DataValue
                    print("section index", section, index)
                        
                    for m in index:
                        data["process_log1"][m].update(section["process_log1"][0])
                    with open(fileName, 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4)
               

            return Response({'status': status.HTTP_200_OK, 'message':"Updated Successfully Done",})  



        if Action == 'DELETE':
            for keys, values in paramList.items():
                dataT = [x for x in DataF if x[keys] != values]
                DataF = dataT

            
            section={}
            section['process_log1'] =  DataF  
            with open(fileName, 'w', encoding='utf-8') as file:
                json.dump(section, file, indent=4)

                    
            return Response({'status': status.HTTP_200_OK, 'message':"Delete Successfully Done",})               

   
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
@api_view(['GET'])
def ServerProcessTrueData(request):
    try:
        sections = {}
        items = []
        refId = []
        filter_data = Table_data_info.objects.filter(table_id=542)
        for k in filter_data:
            refId.append(k.table_ref_id)
                    
        refId = list(set(refId))

        for m in refId:
            for i in filter_data:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_ref_id']=i.table_ref_id
            if sections != "":
                items.append(sections)   
                sections = {}
                
        process_data = [x for x in items if x['Flag'] == "True"]
        
        return Response({'message':"success",'status': status.HTTP_200_OK, "data": process_data})
        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
        
@api_view(['GET'])
def ValidateApi(request, objType, ConfKey):
    try:
        sections = {}
        items = []
        refId = []
        if objType == "ConfKey":
            filter_data = Table_data_info.objects.filter(table_id=620)
            for k in filter_data:
                refId.append(k.table_ref_id)
                        
            refId = list(set(refId))

            for m in refId:
                for i in filter_data:
                    if i.table_ref_id==m:
                        sections[i.column_name]=i.column_data
                        sections['table_ref_id']=i.table_ref_id
                if sections != "":
                    items.append(sections)   
                    sections = {}
                    
            validate_data = [x for x in items if x['ConfKey'] == ConfKey]
            if len(validate_data)!=0:
                return Response({'message':f"{ConfKey} already existed",'status': status.HTTP_200_OK, "result": True})
            else:
                return Response({'message':f"{ConfKey} doesn't already existed",'status': status.HTTP_200_OK, "result": False})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def ChangeLogFileTransferAPI(request):
    try:
        
        folder_path = request.data['folder_path']
        # response_content = eval(request.data['response_content'])
        response_content = bytes(request.data['response_content'], 'utf-8')
        file_size = request.data['file_size']
        file_modify_time = request.data['file_modify_time']
        # print("6046 api_url", api_url)
        # response = requests.get(api_url)
        # print("6048 response_content", response_content)
        # print("6048 response_content", type(response_content))
        file_size1 = os.path.getsize(os.getcwd()+folder_path)
        file_modify_time1 = os.path.getmtime(os.getcwd()+folder_path)
        # print("6059 file_size1", file_size, file_size1, type(file_size), type(file_size1))
        # print("6059 file_modify_time file_modify_time1", file_modify_time, file_modify_time1, type(file_modify_time), type(file_modify_time1))
        # if int(file_size) > int(file_size1) or float(file_modify_time) > float(file_modify_time1):
        if float(file_modify_time) > float(file_modify_time1):
            upload_file = os.getcwd()+folder_path  
            open(upload_file, "wb").write(response_content)
            # open(upload_file, "wb").write(response.content) 
            return Response({'status': status.HTTP_200_OK, 'message':"file transfer successfully"})
        else:
            return Response({'status': status.HTTP_200_OK, 'message':"file transfer successfully"})

    except:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':'Something errors'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
def OnePointerCalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'
        fileNameRuleX = main_media_url+f'/media/upload_file/investing/json/rulex.json'
        fileNameRuleY = main_media_url+f'/media/upload_file/investing/json/ruley.json'

        if os.path.isfile(fileNameRule) and os.path.isfile(fileNameRuleX) and os.path.isfile(fileNameRuleY):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            frx = open(fileNameRuleX)
            rule_data_x = json.load(frx)
            fry = open(fileNameRuleY)
            rule_data_y = json.load(fry)


            dfList = []
            SumList=[]
            count=0

        
            # starting_point = request.data['starting_point']
            # starting_value = request.data['starting_value']
            # daygap = request.data['daygap']
            # value_range_list2 = request.data['value_range_list2']
            which_day = request.data['which_day']
            which_point_add = request.data['which_point_add']
            new_point = request.data['new_point']
            new_point_value = request.data['new_point_value']
        

            # main_data, summary_data, range_point= PointerCalculationOne(starting_point, starting_value, rule_data, value_range_list2, daygap,  which_day, which_point_add, new_point, SumList)
            main_data, summary_data, range_point= PointerCalculationOne(rule_data, rule_data_x, rule_data_y, which_day, which_point_add, new_point, new_point_value, SumList)
            # print("6282 main_data", main_data)
            # print("6283 summary_data", summary_data)
            return Response({'status': status.HTTP_200_OK, "main_data": main_data, 'summary_data':summary_data, "range_point": range_point})



    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
def TwoPointerCalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'
        fileNameRuleX = main_media_url+f'/media/upload_file/investing/json/rulex.json'
        fileNameRuleY = main_media_url+f'/media/upload_file/investing/json/ruley.json'

        if os.path.isfile(fileNameRule) and os.path.isfile(fileNameRuleX) and os.path.isfile(fileNameRuleY):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            frx = open(fileNameRuleX)
            rule_data_x = json.load(frx)
            fry = open(fileNameRuleY)
            rule_data_y = json.load(fry)

            dfList = []
            SumList=[]
            count=0

        
            starting_point = request.data['starting_point']
            print("starting_point", starting_point)
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            first_run = request.data['first_run']
            value_range_list2 = request.data['value_range_list2']
            
        
            if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
                file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                file_name2 = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
                file_name3 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2.xlsx'
                file_name4 =  main_media_url+'/media/upload_file/investing/xlsx/new_point_data.xlsx'
                file_name5 =  main_media_url+'/media/upload_file/investing/xlsx/point_value.xlsx'

                summary_df_backup = pd.read_excel(file_name1)
                raw_data_df_backup = pd.read_excel(file_name2)
                summary2_df_backup = pd.read_excel(file_name3)
                new_point_data_df_backup = pd.read_excel(file_name4)
                point_value_df_backup = pd.read_excel(file_name5)

                file_name1_backup =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file_backup.xlsx'
                file_name2_backup = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file_backup.xlsx'
                file_name3_backup =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2_backup.xlsx'
                file_name4_backup =  main_media_url+'/media/upload_file/investing/xlsx/new_point_data_backup.xlsx'
                file_name5_backup =  main_media_url+'/media/upload_file/investing/xlsx/point_value_backup.xlsx'

                sum_max_df1 = pd.read_excel(file_name1)
                try:
                    exist_data = sum_max_df1['first_run'].iloc[0]
                    if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                        ExcelFileWrite(file_name1_backup, summary_df_backup)
                        ExcelFileWrite(file_name2_backup, raw_data_df_backup)
                        ExcelFileWrite(file_name3_backup, summary2_df_backup)
                        ExcelFileWrite(file_name4_backup, new_point_data_df_backup)
                        ExcelFileWrite(file_name5_backup, point_value_df_backup)
                        empty_df = pd.DataFrame()
                        empty_df.to_excel(file_name1, index=False)
                        empty_df.to_excel(file_name2, index=False)
                        empty_df.to_excel(file_name3, index=False)
                        empty_df.to_excel(file_name4, index=False)
                        empty_df.to_excel(file_name5, index=False)
                except:
                    ExcelFileWrite(file_name1_backup, summary_df_backup)
                    ExcelFileWrite(file_name2_backup, raw_data_df_backup)
                    ExcelFileWrite(file_name3_backup, summary2_df_backup)
                    ExcelFileWrite(file_name4_backup, new_point_data_df_backup)
                    ExcelFileWrite(file_name5_backup, point_value_df_backup)

                    empty_df = pd.DataFrame()
                    empty_df.to_excel(file_name1, index=False)
                    empty_df.to_excel(file_name2, index=False)
                    empty_df.to_excel(file_name3, index=False)
                    empty_df.to_excel(file_name4, index=False)
                    empty_df.to_excel(file_name5, index=False)


          
            main_data, range_point= PointerCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, dfList, count, SumList, daygap, first_run)
          
            return Response({'status': status.HTTP_200_OK, "main_data": main_data, "range_point": range_point})


    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['POST'])
def TwoPointerCalculationSummaryAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'

        if os.path.isfile(fileNameRule):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            dfList = []
            SumList=[]
            count=0

            starting_point = request.data['starting_point']
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            first_run = request.data['first_run']
            value_range_list2 = request.data['value_range_list2']
            minp_value = request.data['minp_value']
            point_id = request.data['point_id']

            # if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
            file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
            sum_max_df1 = pd.read_excel(file_name1)
            try:
                exist_data = sum_max_df1['first_run'].iloc[0]
                if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                    # empty_df = pd.DataFrame()
                    # empty_df.to_excel(file_name1, index=False)
                    return Response({'status': status.HTTP_200_OK, "summary_data": JsonConvertData(sum_max_df1) })
            except:
                # empty_df = pd.DataFrame()
                # empty_df.to_excel(file_name1, index=False)

                main_df = pd.read_excel(main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx')
                # sum_max_df = main_df[main_df['MinP'] == minp_value]
                sum_max_df = main_df[main_df['point_id'] == point_id]
                sum_max_df.insert(0, "starting_point", starting_point, True)
                sum_max_df.insert(1, "starting_value", starting_value, True)
                sum_max_df.insert(2, "daygap", daygap, True)
                sum_max_df.insert(3, "value_range_0", value_range_list2[0], True)
                sum_max_df.insert(4, "value_range_1", value_range_list2[1], True)
                sum_max_df.insert(5, "created_time", strftime("%Y-%m-%d %H:%M:%S", gmtime()), True)
                sum_max_df.insert(17, "remarks", "sum_max_value", True)
                sum_max_df.insert(18, "first_run", first_run, True)
                sum_max_df.insert(23, "Left_Day", 0, True)
                sum_max_df.insert(24, "Left_Point", 0, True)
                sum_max_df.insert(25, "Left_pv", 0, True)
                sum_max_df.insert(26, "Right_Day", 0, True)
                sum_max_df.insert(27, "Right_Point", 0, True)
                sum_max_df.insert(28, "Right_pv", 0, True)
        
                ExcelFileWrite(main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx', sum_max_df)
                file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                summary_df = pd.read_excel(file_name1)
                summary_data = JsonConvertData(summary_df)
                        
                return Response({'status': status.HTTP_200_OK, "summary_data": summary_data})


    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
def PointerCalculationSummaryDataUpdateAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'

        if os.path.isfile(fileNameRule):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            dfList = []
            SumList=[]

            d1lp1 = request.data['d1lp1']
            d1rp1 = request.data['d1rp1']
            d2lp2 = request.data['d2lp2']
            d3lp3 = request.data['d3lp3']
            pv0 = request.data['pv0']
            pv1 = request.data['pv1']
            pv2 = request.data['pv2']
            pv3 = request.data['pv3']

            # print("d1lp1", d1lp1)

            file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
            sum_max_df1 = pd.read_excel(file_name1)
            exist_data = sum_max_df1['first_run'].iloc[0]
            if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                sum_max_df1.at[0, 'd1lp1'] = d1lp1
                sum_max_df1.at[0, 'd1rp1'] = d1rp1
                sum_max_df1.at[0, 'd2lp2'] = d2lp2
                sum_max_df1.at[0, 'd3lp3'] = d3lp3
                sum_max_df1.at[0, 'pv0'] = pv0
                sum_max_df1.at[0, 'pv1'] = pv1
                sum_max_df1.at[0, 'pv2'] = pv2
                sum_max_df1.at[0, 'pv3'] = pv3
         
                sum_max_df1.to_excel(file_name1, index=False) 

            summary_df = pd.read_excel(file_name1)
            summary_data = JsonConvertData(summary_df)
                       
            return Response({'status': status.HTTP_200_OK, "summary_data": summary_data})


    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
def TwoPointerMinPCalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'

        if os.path.isfile(fileNameRule):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            dfList = []
            SumList=[]
            count=0

        
            starting_point = request.data['starting_point']
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            first_run = request.data['first_run']
            value_range_list2 = request.data['value_range_list2']
            # point_add = request.data['point_add']
            # new_point = request.data['new_point']

            # input_p = request.data['input_p']
          
            # d1_point0 = request.data['d1_point0']
            # d2_point2 = request.data['d2_point2']
        
            
            # if point_add == "YES" or point_add == "Yes" or point_add == "yes": 
            #     new_point = new_point
            #     file_name1 = main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
            #     print("6331")
            #     sum_max_df1 = pd.read_excel(file_name1, engine='openpyxl')
            #     print("sum_max_df1", sum_max_df1)
            #     try:
            #         exist_data = sum_max_df1['first_run'].iloc[0]
            #         if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
            #             sum_max_df1.at[0, 'd1_point1'] = new_point
            #             sum_max_df1.to_excel(file_name1, index=False)
            #     except:
            #         print("")

            # print("6268")

            if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
                file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                file_name2 = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
                # print("6347")
                sum_max_df1 = pd.read_excel(file_name1)
                # print("6349")
                try:
                    exist_data = sum_max_df1['first_run'].iloc[0]
                    if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                        empty_df = pd.DataFrame()
                        empty_df.to_excel(file_name1, index=False)
                        empty_df.to_excel(file_name2, index=False)
                except:
                    empty_df = pd.DataFrame()
                    empty_df.to_excel(file_name1, index=False)
                    empty_df.to_excel(file_name2, index=False)

            minp_data= PointerCalculationMinp(starting_point, starting_value, rule_data, value_range_list2, dfList, count, SumList, daygap, first_run)

            return Response({'status': status.HTTP_200_OK, 'minp_data': minp_data})

    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
def ThreePointerCalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'

        if os.path.isfile(fileNameRule):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            dfList = []
            SumList=[]
            count=0

        
            starting_point = request.data['starting_point']
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            first_run = request.data['first_run']
            value_range_list2 = request.data['value_range_list2']

           
            if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
                file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                file_name2 = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
                sum_max_df1 = pd.read_excel(file_name1)
                try:
                    exist_data = sum_max_df1['first_run'].iloc[0]
                    if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                        empty_df = pd.DataFrame()
                        empty_df.to_excel(file_name1, index=False)
                        empty_df.to_excel(file_name2, index=False)
                except:
                    empty_df = pd.DataFrame()
                    empty_df.to_excel(file_name1, index=False)
                    empty_df.to_excel(file_name2, index=False)

            summary_data= PointerCalculation3(starting_point, starting_value, rule_data, value_range_list2, dfList, count, SumList, daygap, first_run, input_p, d1_point0,  d1_point1, d2_point2, minp_value)
            return Response({'status': status.HTTP_200_OK, 'summary_data':summary_data})


    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        



@api_view(['POST'])
def ThreePointerLeftRightCalculationAPI(request, apikey):
    try:
        result, message = UserLogin(apikey, "ThreePointerLeftRightCalculationAPI")
        if result == True:
            # result1, message1, main_data = UserMetaProfileCheck(14, "AA.json")
            # return Response({"message": message1, "result":result1, "main_data": main_data})
            fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'
            fileNameRuleX = main_media_url+f'/media/upload_file/investing/json/rulex.json'
            fileNameRuleY = main_media_url+f'/media/upload_file/investing/json/ruley.json'

            if os.path.isfile(fileNameRule) and os.path.isfile(fileNameRuleX) and os.path.isfile(fileNameRuleY):
                fr = open(fileNameRule)
                rule_data = json.load(fr)
                frx = open(fileNameRuleX)
                rule_data_x = json.load(frx)
                fry = open(fileNameRuleY)
                rule_data_y = json.load(fry)

                dfList = []
                SumList=[]
                count=0

                L1 = request.data['L1']
                R1 = request.data['R1']
                L2 = request.data['L2']
                starting_point = request.data['starting_point']
                print("starting_point", starting_point)
                starting_value = request.data['starting_value']
                daygap = request.data['daygap']
                first_run = request.data['first_run']
                value_range_list2 = request.data['value_range_list2']
                
            
                if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
                    file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                    file_name2 = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
                    file_name3 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2.xlsx'
                    file_name4 =  main_media_url+'/media/upload_file/investing/xlsx/new_point_data.xlsx'
                    file_name5 =  main_media_url+'/media/upload_file/investing/xlsx/point_value.xlsx'

                    summary_df_backup = pd.read_excel(file_name1)
                    raw_data_df_backup = pd.read_excel(file_name2)
                    summary2_df_backup = pd.read_excel(file_name3)
                    new_point_data_df_backup = pd.read_excel(file_name4)
                    point_value_df_backup = pd.read_excel(file_name5)

                    file_name1_backup =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file_backup.xlsx'
                    file_name2_backup = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file_backup.xlsx'
                    file_name3_backup =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2_backup.xlsx'
                    file_name4_backup =  main_media_url+'/media/upload_file/investing/xlsx/new_point_data_backup.xlsx'
                    file_name5_backup =  main_media_url+'/media/upload_file/investing/xlsx/point_value_backup.xlsx'

                    sum_max_df1 = pd.read_excel(file_name1)
                    try:
                        exist_data = sum_max_df1['first_run'].iloc[0]
                        if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                            ExcelFileWrite(file_name1_backup, summary_df_backup)
                            ExcelFileWrite(file_name2_backup, raw_data_df_backup)
                            ExcelFileWrite(file_name3_backup, summary2_df_backup)
                            ExcelFileWrite(file_name4_backup, new_point_data_df_backup)
                            ExcelFileWrite(file_name5_backup, point_value_df_backup)
                            empty_df = pd.DataFrame()
                            empty_df.to_excel(file_name1, index=False)
                            empty_df.to_excel(file_name2, index=False)
                            empty_df.to_excel(file_name3, index=False)
                            empty_df.to_excel(file_name4, index=False)
                            empty_df.to_excel(file_name5, index=False)
                    except:
                        ExcelFileWrite(file_name1_backup, summary_df_backup)
                        ExcelFileWrite(file_name2_backup, raw_data_df_backup)
                        ExcelFileWrite(file_name3_backup, summary2_df_backup)
                        ExcelFileWrite(file_name4_backup, new_point_data_df_backup)
                        ExcelFileWrite(file_name5_backup, point_value_df_backup)

                        empty_df = pd.DataFrame()
                        empty_df.to_excel(file_name1, index=False)
                        empty_df.to_excel(file_name2, index=False)
                        empty_df.to_excel(file_name3, index=False)
                        empty_df.to_excel(file_name4, index=False)
                        empty_df.to_excel(file_name5, index=False)


            
                main_data, range_point= ThreePointerLeftRightCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, dfList, count, SumList, daygap, first_run, L1, R1, L2)
                return Response({'status': status.HTTP_200_OK, "main_data": main_data, "range_point": range_point})
        else:
            return Response({'status': status.HTTP_200_OK, "message": message})


    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or Authentication Fails or {error}'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
def ThreePointerLeftRightDayBasisCalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'
        fileNameRuleX = main_media_url+f'/media/upload_file/investing/json/rulex.json'
        fileNameRuleY = main_media_url+f'/media/upload_file/investing/json/ruley.json'

        if os.path.isfile(fileNameRule) and os.path.isfile(fileNameRuleX) and os.path.isfile(fileNameRuleY):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            frx = open(fileNameRuleX)
            rule_data_x = json.load(frx)
            fry = open(fileNameRuleY)
            rule_data_y = json.load(fry)

            dfList = []
            SumList=[]
            count=0

        
            starting_point = request.data['starting_point']
            print("6705 starting_point", starting_point)
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            first_run = request.data['first_run']
            value_range_list2 = request.data['value_range_list2']
            right_day2 = request.data['right_day2']
            
        
            if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
                file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                file_name2 = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
                file_name3 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2.xlsx'
                file_name4 =  main_media_url+'/media/upload_file/investing/xlsx/new_point_data.xlsx'
                file_name5 =  main_media_url+'/media/upload_file/investing/xlsx/point_value.xlsx'

                summary_df_backup = pd.read_excel(file_name1)
                raw_data_df_backup = pd.read_excel(file_name2)
                summary2_df_backup = pd.read_excel(file_name3)
                new_point_data_df_backup = pd.read_excel(file_name4)
                point_value_df_backup = pd.read_excel(file_name5)

                file_name1_backup =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file_backup.xlsx'
                file_name2_backup = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file_backup.xlsx'
                file_name3_backup =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2_backup.xlsx'
                file_name4_backup =  main_media_url+'/media/upload_file/investing/xlsx/new_point_data_backup.xlsx'
                file_name5_backup =  main_media_url+'/media/upload_file/investing/xlsx/point_value_backup.xlsx'

                sum_max_df1 = pd.read_excel(file_name1)
                try:
                    exist_data = sum_max_df1['first_run'].iloc[0]
                    if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                        ExcelFileWrite(file_name1_backup, summary_df_backup)
                        ExcelFileWrite(file_name2_backup, raw_data_df_backup)
                        ExcelFileWrite(file_name3_backup, summary2_df_backup)
                        ExcelFileWrite(file_name4_backup, new_point_data_df_backup)
                        ExcelFileWrite(file_name5_backup, point_value_df_backup)
                        empty_df = pd.DataFrame()
                        empty_df.to_excel(file_name1, index=False)
                        empty_df.to_excel(file_name2, index=False)
                        empty_df.to_excel(file_name3, index=False)
                        empty_df.to_excel(file_name4, index=False)
                        empty_df.to_excel(file_name5, index=False)
                except:
                    ExcelFileWrite(file_name1_backup, summary_df_backup)
                    ExcelFileWrite(file_name2_backup, raw_data_df_backup)
                    ExcelFileWrite(file_name3_backup, summary2_df_backup)
                    ExcelFileWrite(file_name4_backup, new_point_data_df_backup)
                    ExcelFileWrite(file_name5_backup, point_value_df_backup)

                    empty_df = pd.DataFrame()
                    empty_df.to_excel(file_name1, index=False)
                    empty_df.to_excel(file_name2, index=False)
                    empty_df.to_excel(file_name3, index=False)
                    empty_df.to_excel(file_name4, index=False)
                    empty_df.to_excel(file_name5, index=False)


          
            main_data, range_point= ThreePointerLeftRightDayBasisCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, dfList, count, SumList, daygap, first_run, right_day2)
          
            return Response({'status': status.HTTP_200_OK, "main_data": main_data, "range_point": range_point})


    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        



@api_view(['POST'])
def FourPointerLeftRightCalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'
        fileNameRuleX = main_media_url+f'/media/upload_file/investing/json/rulex.json'
        fileNameRuleY = main_media_url+f'/media/upload_file/investing/json/ruley.json'

        if os.path.isfile(fileNameRule) and os.path.isfile(fileNameRuleX) and os.path.isfile(fileNameRuleY):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            frx = open(fileNameRuleX)
            rule_data_x = json.load(frx)
            fry = open(fileNameRuleY)
            rule_data_y = json.load(fry)

            dfList = []
            SumList=[]
            count=0

           
        
            L1 = request.data['L1']
            R1 = request.data['R1']
            L2 = request.data['L2']
            L3 = request.data['L3']
            starting_point = request.data['starting_point']
            print("starting_point", starting_point)
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            first_run = request.data['first_run']
            value_range_list2 = request.data['value_range_list2']
            
        
            if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
                file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                file_name2 = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
                file_name3 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2.xlsx'
                file_name4 =  main_media_url+'/media/upload_file/investing/xlsx/new_point_data.xlsx'
                file_name5 =  main_media_url+'/media/upload_file/investing/xlsx/point_value.xlsx'

                summary_df_backup = pd.read_excel(file_name1)
                raw_data_df_backup = pd.read_excel(file_name2)
                summary2_df_backup = pd.read_excel(file_name3)
                new_point_data_df_backup = pd.read_excel(file_name4)
                point_value_df_backup = pd.read_excel(file_name5)

                file_name1_backup =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file_backup.xlsx'
                file_name2_backup = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file_backup.xlsx'
                file_name3_backup =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2_backup.xlsx'
                file_name4_backup =  main_media_url+'/media/upload_file/investing/xlsx/new_point_data_backup.xlsx'
                file_name5_backup =  main_media_url+'/media/upload_file/investing/xlsx/point_value_backup.xlsx'

                sum_max_df1 = pd.read_excel(file_name1)
                try:
                    exist_data = sum_max_df1['first_run'].iloc[0]
                    if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                        ExcelFileWrite(file_name1_backup, summary_df_backup)
                        ExcelFileWrite(file_name2_backup, raw_data_df_backup)
                        ExcelFileWrite(file_name3_backup, summary2_df_backup)
                        ExcelFileWrite(file_name4_backup, new_point_data_df_backup)
                        ExcelFileWrite(file_name5_backup, point_value_df_backup)
                        empty_df = pd.DataFrame()
                        empty_df.to_excel(file_name1, index=False)
                        empty_df.to_excel(file_name2, index=False)
                        empty_df.to_excel(file_name3, index=False)
                        empty_df.to_excel(file_name4, index=False)
                        empty_df.to_excel(file_name5, index=False)
                except:
                    ExcelFileWrite(file_name1_backup, summary_df_backup)
                    ExcelFileWrite(file_name2_backup, raw_data_df_backup)
                    ExcelFileWrite(file_name3_backup, summary2_df_backup)
                    ExcelFileWrite(file_name4_backup, new_point_data_df_backup)
                    ExcelFileWrite(file_name5_backup, point_value_df_backup)

                    empty_df = pd.DataFrame()
                    empty_df.to_excel(file_name1, index=False)
                    empty_df.to_excel(file_name2, index=False)
                    empty_df.to_excel(file_name3, index=False)
                    empty_df.to_excel(file_name4, index=False)
                    empty_df.to_excel(file_name5, index=False)


          
            main_data, range_point= FourPointerLeftRightCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, dfList, count, SumList, daygap, first_run, L1, R1, L2, L3)
          
            return Response({'status': status.HTTP_200_OK, "main_data": main_data, "range_point": range_point})
    
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        



@api_view(['POST'])
def ThreePointerMinpCalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'

        if os.path.isfile(fileNameRule):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            dfList = []
            SumList=[]
            count=0

        
            starting_point = request.data['starting_point']
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            first_run = request.data['first_run']
            value_range_list2 = request.data['value_range_list2']

            input_p = request.data['input_p']
        
            d1_point0 = request.data['d1_point0']
            d1_point1 = request.data['d1_point1']
            d2_point2 = request.data['d2_point2']
        


            if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
                file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                file_name2 = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
                sum_max_df1 = pd.read_excel(file_name1)
                try:
                    exist_data = sum_max_df1['first_run'].iloc[0]
                    if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                        empty_df = pd.DataFrame()
                        empty_df.to_excel(file_name1, index=False)
                        empty_df.to_excel(file_name2, index=False)
                except:
                    empty_df = pd.DataFrame()
                    empty_df.to_excel(file_name1, index=False)
                    empty_df.to_excel(file_name2, index=False)

            minp_data= PointerCalculation3Minp(starting_point, starting_value, rule_data, value_range_list2, dfList, count, SumList, daygap, first_run, input_p, d1_point0,  d1_point1, d2_point2)
            return Response({'status': status.HTTP_200_OK, 'minp_data':minp_data})


    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
def ThreePointerD3CalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'

        if os.path.isfile(fileNameRule):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            dfList = []
            SumList=[]
            count=0

        
            starting_point = request.data['starting_point']
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            first_run = request.data['first_run']
            value_range_list2 = request.data['value_range_list2']

            input_p = request.data['input_p']
        
            d1_point0 = request.data['d1_point0']
            d1_point1 = request.data['d1_point1']
            d2_point2 = request.data['d2_point2']
        

            minp_value = request.data['minp_value']
           


            if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
                file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                file_name2 = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
                # file_name3 = main_media_url+'/media/upload_file/investing/xlsx/new_point_data.xlsx'

                # empty_df3 = pd.DataFrame()
                # empty_df3.to_excel(file_name3, index=False)

                sum_max_df1 = pd.read_excel(file_name1)
                try:
                    exist_data = sum_max_df1['first_run'].iloc[0]
                    if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                        empty_df = pd.DataFrame()
                        empty_df.to_excel(file_name1, index=False)
                        empty_df.to_excel(file_name2, index=False)
                except:
                    empty_df = pd.DataFrame()
                    empty_df.to_excel(file_name1, index=False)
                    empty_df.to_excel(file_name2, index=False)

            summary_data= PointerCalculationd3(starting_point, starting_value, rule_data, value_range_list2, dfList, count, SumList, daygap, first_run, input_p, d1_point0,  d1_point1, d2_point2, minp_value)
            return Response({'status': status.HTTP_200_OK, 'summary_data':summary_data})


    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
def MainPointerCalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'
        fileNameRuleX = main_media_url+f'/media/upload_file/investing/json/rulex.json'
        fileNameRuleY = main_media_url+f'/media/upload_file/investing/json/ruley.json'

        if os.path.isfile(fileNameRule) and os.path.isfile(fileNameRuleX) and os.path.isfile(fileNameRuleY):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            frx = open(fileNameRuleX)
            rule_data_x = json.load(frx)
            fry = open(fileNameRuleY)
            rule_data_y = json.load(fry)

            SumList=[]

            starting_point = request.data['starting_point']
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            value_range_list2 = request.data['value_range_list2']
            

            file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2.xlsx'
            empty_df = pd.DataFrame()
            empty_df.to_excel(file_name1, index=False)

           
            main_data, summary_data, summary_data2,  range_point = MainPointerCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, SumList, daygap)
            # main_data, range_point = MainPointerCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, SumList, daygap)
            # result = MainPointerCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, SumList, daygap)
            # if result == True:
            #     return Response({'status': status.HTTP_200_OK, 'message':'success'})
            return Response({'status': status.HTTP_200_OK, "main_data": main_data, 'summary_data': summary_data, "summary_data2": summary_data2,  "range_point": range_point})


    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['POST'])
def ThreePointerD3MinpCalculationAPI(request):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'

        if os.path.isfile(fileNameRule):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            dfList = []
            SumList=[]
            count=0

        
            starting_point = request.data['starting_point']
            starting_value = request.data['starting_value']
            daygap = request.data['daygap']
            first_run = request.data['first_run']
            value_range_list2 = request.data['value_range_list2']

            input_p = request.data['input_p']
        
            d1_point0 = request.data['d1_point0']
            d1_point1 = request.data['d1_point1']
            d2_point2 = request.data['d2_point2']
        

            if first_run == "YES" or first_run == "Yes" or first_run == "yes":  
                file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
                file_name2 = main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
                sum_max_df1 = pd.read_excel(file_name1)
                try:
                    exist_data = sum_max_df1['first_run'].iloc[0]
                    if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
                        empty_df = pd.DataFrame()
                        empty_df.to_excel(file_name1, index=False)
                        empty_df.to_excel(file_name2, index=False)
                except:
                    empty_df = pd.DataFrame()
                    empty_df.to_excel(file_name1, index=False)
                    empty_df.to_excel(file_name2, index=False)

            minp_data= PointerCalculationd3Minp(starting_point, starting_value, rule_data, value_range_list2, dfList, count, SumList, daygap, first_run, input_p, d1_point0,  d1_point1, d2_point2)
            return Response({'status': status.HTTP_200_OK, 'minp_data':minp_data})

    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)        





@api_view(['GET'])
def FetchNewPointData(request):
    try:
        
        file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/new_point_data.xlsx'
        new_point_df = pd.read_excel(file_name1) 

        new_point_data = JsonConvertData(new_point_df)
                
        left_data = [x for x in new_point_data if x['which_point_add'] == "Left"]
        right_data = [x for x in new_point_data if x['which_point_add'] == "Right"]

        main_file_name =  main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx'
        main_df = pd.read_excel(main_file_name)

        file_name =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
        summary_df = pd.read_excel(file_name)

        file_name3 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2.xlsx'
        summary_df3 = pd.read_excel(file_name3)

        file_name4 =  main_media_url+'/media/upload_file/investing/xlsx/point_value.xlsx'
        summary_df4 = pd.read_excel(file_name4)

        main_data = JsonConvertData(main_df)
        summary_data = JsonConvertData(summary_df)
        summary_data2 = JsonConvertData(summary_df3)
        point_value = JsonConvertData(summary_df4)


        return Response({'message':"success",'status': status.HTTP_200_OK, "left_data": left_data, "right_data": right_data, "main_data": main_data, "summary_data": summary_data, "summary_data2": summary_data2, "point_value": point_value})
        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        


@api_view(['GET'])
def GETDAPI(request):
    try:
        sections = {}
        items = []
        refId = []

       
        api_name_value = Table_data_info.objects.filter(table_id=1)
        for k in api_name_value:
            refId.append(k.table_ref_id)
                    
        refId = list(set(refId))

        for m in refId:
            for i in api_name_value:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_ref_id']=i.table_ref_id
            if sections != "":
                items.append(sections)   
                sections = {}

        result, message, main_data = userMetaDataModel(data=items, datasource="User", user_id=14)        
                     
        return Response({'status': status.HTTP_200_OK, "message":"success", "data": main_data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])
def GETDJSONAPI(request):
    try:
        result, message, main_data = userMetaDataJson(fileName=main_media_url+f"/media/upload_file/yahoo_finance_hist/AA.json", datasource='AA.json', user_id=14)                  
        return Response({'status': status.HTTP_200_OK, "message":"success", "data": main_data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])
def GETFileDataAPI(request):
    try:
        # file_name = request.data['file_name']
        result, message, main_data = WrapperMultiFileCheck(file_name="process_log")
        # WrapperMultiFileCheck(file_name="process_log.json")
        # result, message, main_data = userMetaDataJson()                  
        return Response({'status': status.HTTP_200_OK, "message":"success", "data": main_data})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])
def GETCosineSimilarityAPI(request):
    try:
        # file_name = request.data['file_name']
        result, message, main_data1, main_data2, input_df, Dic, DicF = CosineSimilarity()
        if result == True:
            return Response({'status': status.HTTP_200_OK, "message":"success", "main_data1": main_data1, "main_data2": main_data2, "input_df": input_df, "Dic": Dic, "DicF": DicF, })
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': message}, status=status.HTTP_400_BAD_REQUEST)  

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


def SendMessage(email, subject, message):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/message.json'
        # ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/message.json', api_url=main_url+f'/media/upload_file/investing/json/message.json')
        curdate, curdatestamp, curdatetime, curdatetimestamp, curdate5, curtimestamp5, curdate_5, curtimestamp_5 = dtm()
        if os.path.isfile(fileName):
            # f = open(fileName)
            # data = json.load(f)
            # array_data = data['data']

            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)

            y = {
                "message_id": str(generate_unique_random_number()),
                "inbound":[
                    {
                        "email": email,
                        "subject": subject,
                        "message": message,
                        "is_read": 'False',
                        "time": curdatetime,
                    }
                ],
                "outbound":[]
            }
            write_json(y)

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def SendNotificationMessageAPI(request):
    try:
        email = request.data['email']
        subject = request.data['subject']
        message = request.data['message']

        SendMessage(email, subject, message)

        return Response({'status': status.HTTP_200_OK, "message":"Message successfully send."})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])
def GetMessageAPI(request, email):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/message.json'
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']
        unread_data = []
        for d in array_data:
            inbound_data = [x for x in d['inbound'] if x['email'] == email and x['is_read'] == 'False']
            if len(inbound_data) != 0:
                unread_data.append(d)
           
        # print("unread_data", unread_data)

        return Response({'status': status.HTTP_200_OK, "message":"success", 'data': unread_data})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['PUT'])
def UpdateMessageAPI(request, message_id):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/message.json'
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']
        unread_data = []
        for i in range(len(array_data)):
            for key in array_data[i].keys():
                if key == 'message_id':
                    if array_data[i][key] == message_id:
                        compareValue = [x for x in array_data[i]['inbound'] if x['is_read'] == 'False']
                        if len(compareValue)!=0:
                            for j in range(len(array_data[i]['inbound'])):
                                if array_data[i]['inbound'][j]['is_read'] ==  'False':
                                    array_data[i]['inbound'][j]['email'] = array_data[i]['inbound'][j]['email']
                                    array_data[i]['inbound'][j]['subject'] = array_data[i]['inbound'][j]['subject']
                                    array_data[i]['inbound'][j]['message'] = array_data[i]['inbound'][j]['message']
                                    array_data[i]['inbound'][j]['is_read'] = "True"
                                    array_data[i]['inbound'][j]['time'] = array_data[i]['inbound'][j]['time']
                                    file_data={}
                                    with open(fileName, 'w', encoding='utf-8') as file:
                                        file_data["data"]=array_data
                                        json.dump(file_data, file, indent=4)  


        return Response({'status': status.HTTP_200_OK, "message":"user have been seen the message successfully"})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  



def SendOutboundMessage(message_id, email, message):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/message.json'
        # ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/message.json', api_url=main_url+f'/media/upload_file/investing/json/message.json')
        curdate, curdatestamp, curdatetime, curdatetimestamp, curdate5, curtimestamp5, curdate_5, curtimestamp_5 = dtm()
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            for i in range(len(array_data)):
                for key in array_data[i].keys():
                    if key == 'message_id':
                        if array_data[i][key] == message_id:
                            new_data = {
                                "email": email,
                                "message": message,
                                "time": curdatetime,
                            }
                            array_data[i]['outbound'].append(new_data)
                            file_data={}
                            with open(fileName, 'w', encoding='utf-8') as file:
                                file_data["data"]=array_data
                                json.dump(file_data, file, indent=4) 
                                

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def SendOutboundMessageAPI(request):
    try:
        message_id = request.data['message_id']
        email = request.data['email']
        message = request.data['message']

        SendOutboundMessage(message_id, email, message)

        return Response({'status': status.HTTP_200_OK, "message":"Outbound Message successfully send."})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


def SendInboundMessage(message_id, email, subject, message):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/message.json'
        # ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/message.json', api_url=main_url+f'/media/upload_file/investing/json/message.json')
        curdate, curdatestamp, curdatetime, curdatetimestamp, curdate5, curtimestamp5, curdate_5, curtimestamp_5 = dtm()
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            for i in range(len(array_data)):
                for key in array_data[i].keys():
                    if key == 'message_id':
                        if array_data[i][key] == message_id:
                            new_data = {
                                "email": email,
                                "subject": subject,
                                "message": message,
                                "is_read": 'False',
                                "time": curdatetime,
                            }
                            array_data[i]['inbound'].append(new_data)
                            file_data={}
                            with open(fileName, 'w', encoding='utf-8') as file:
                                file_data["data"]=array_data
                                json.dump(file_data, file, indent=4) 


    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def SendInboundMessageAPI(request):
    try:
        message_id = request.data['message_id']
        email = request.data['email']
        subject = request.data['subject']
        message = request.data['message']

        SendInboundMessage(message_id, email, subject, message)

        return Response({'status': status.HTTP_200_OK, "message":"Inbound Message successfully send."})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


def BalanceSimulationJson(name, starting_point, starting_vlaue, left_side, right_side, all_starting_tabular_data, user_email):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/balance_simulation.json'
        # ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/message.json', api_url=main_url+f'/media/upload_file/investing/json/message.json')
        curdate, curdatestamp, curdatetime, curdatetimestamp, curdate5, curtimestamp5, curdate_5, curtimestamp_5 = dtm()
        if os.path.isfile(fileName):
            f = open(fileName)
            data = json.load(f)
            array_data = data['data']
            compareData = [x for x in array_data if x['name'] == name and x['user_email'] == user_email ]
            if len(compareData)!=0:
                for j in range(len(array_data)):
                    if array_data[j]['user_email'] ==  user_email and array_data[j]['name'] ==  name:
                        array_data[j]['user_email'] = user_email
                        array_data[j]['name'] = name
                        array_data[j]['starting_point'] = starting_point
                        array_data[j]['starting_vlaue'] = starting_vlaue
                        array_data[j]['left_side'] = left_side
                        array_data[j]['right_side'] = right_side
                        array_data[j]['right_side'] = right_side
                        array_data[j]['all_starting_tabular_data'] = all_starting_tabular_data
                        array_data[j]['time'] = curdatetime
                        file_data={}
                        with open(fileName, 'w', encoding='utf-8') as file:
                            file_data["data"]=array_data
                            json.dump(file_data, file, indent=4)  

            else:

                def write_json(new_data, filename=fileName):
                    with open(filename, 'r+') as file:
                        file_data = json.load(file)
                        file_data["data"].append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)

                y = {
                    "user_email": user_email,
                    "name": name,
                    "starting_point": starting_point,
                    "starting_vlaue": starting_vlaue,
                    "left_side": left_side,
                    "right_side": right_side,
                    "all_starting_tabular_data": all_starting_tabular_data,
                    "time": curdatetime,
                }
                write_json(y)

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def BalanceSimulationAPI(request):
    try:
        name = request.data['name']
        starting_point = request.data['starting_point']
        starting_vlaue = request.data['starting_vlaue']
        left_side = request.data['left_side']
        right_side = request.data['right_side']
        all_starting_tabular_data = request.data['all_starting_tabular_data']
        user_email = request.data['user_email']
        # fileName = main_media_url+f'/media/upload_file/investing/json/balance_simulation.json'
        # f = open(fileName)
        # data = json.load(f)
        # array_data = data['data']
        # compareData = [x for x in array_data if x['name'] == name and x['user_email'] == user_email ]
        # # if len(compareData)!=0:
        #     return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{name} name is already existed.'}, status=status.HTTP_400_BAD_REQUEST)  

        BalanceSimulationJson(name, starting_point, starting_vlaue, left_side, right_side, all_starting_tabular_data, user_email)

        return Response({'status': status.HTTP_200_OK, "message":"Balance Simulation successfully created."})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])
def GETBalanceSimulationAPI(request):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/balance_simulation.json'
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']
        Datalist = []
        for m in array_data:
            Datalist.append({
                'name': m['name'],
                'user_email': m['user_email']
            })      
        return Response({'status': status.HTTP_200_OK, "message":"Balance Simulation successfully fetch data.", "data": Datalist})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])
def GETBalanceSimulationByNameAPI(request, name, user_email):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/balance_simulation.json'
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']
        compareData = [x for x in array_data if x['name'] == name and x['user_email'] == user_email ]
      
        return Response({'status': status.HTTP_200_OK, "message":"Balance Simulation successfully fetch data by name.", "data": compareData})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


def generateArray(start, end, step = 5):
    result = []
    if start <= end: 
        # Case where start is less than or equal to end, step forward by step
        for i in range(start, end-step, step):
            result.append(i)
    else:
        #  Case where start is greater than end, step backward by step
        for i in  range(start, end-step, -step):
            result.append(i) 

    return result
        

@api_view(['POST'])
def ALLStartingPointAPI(request):
    try:
        scalList = request.data['scalList']
        resultList = request.data['resultList']
        
        LeftSideSum=0
        RightSideSum=0
        LeftClosingPoint=0
        RightClosingPoint=0
        LeftSideSoldValue=0
        RightSideSoldValue=0
        DataList=[]
        for starting_point in scalList:
            for i in range(len(resultList)):
                # print("7515", i)
                item = resultList[i]
                # print("item", item)
                if len(str(item['Sold'])) != 0 and item['Sold'] !=0 and item["side"]== "left":
                    if item["type"] == "ES" and item["side"]== "left":
                        LeftSideSoldValue += (float(item['value']) - float(item['Sold']))*10
                    else:
                        LeftSideSoldValue += (float(item['value']) - float(item['Sold']))

                if len(str(item['Sold'])) != 0 and item['Sold'] !=0 and item["side"]== "right":
                    if item["type"] == "ES" and item["side"]== "right":
                        RightSideSoldValue += (float(item['value']) - float(item['Sold']))*10
                    else:
                        RightSideSoldValue += (float(item['value']) - float(item['Sold']))

                if item["type"] == "MES" and item["side"] == "left" and len(str(item['Sold'])) != 0 and item['Sold'] !=0:
                    LeftSideSum+=0     
                elif item["type"] == "MES" and  item["side"]== "left":
                    LeftSideSum += float(item['value'])
                    if float(item['point']) > float(starting_point):
                        LeftClosingPoint +=0
                    if float(item['point']) < float(starting_point):
                        LeftClosingPoint -= (abs(float(starting_point)-float(item['point'])))
                    

                if item["type"]  == "ES" and item["side"] == "left" and len(str(item['Sold'])) != 0 and item['Sold'] !=0:
                    LeftSideSum+=0  
                elif item["type"]  == "ES" and item["side"] == "left":
                    LeftSideSum += float(item['value']) * 10
                    if float(item['point']) > float(starting_point):
                        LeftClosingPoint +=0
                    if float(item['point']) < float(starting_point):
                        LeftClosingPoint -= (abs(float(starting_point)-float(item['point']))*10)

                if item["type"] == "ST" and item["side"] == "left" and len(str(item['Sold'])) != 0 and item['Sold'] !=0:
                    LeftSideSum+=0     
                elif item["type"]  == "ST" and  item["side"] == "left": 
                    LeftSideSum += 0
                    if float(item['point']) < float(starting_point):
                        LeftClosingPoint +=abs(float(starting_point)-float(item['point']))
                    # if float(item['point']) > float(starting_point):
                    #     LeftClosingPoint -= abs(float(starting_point)-float(item['point']))

                if item["type"]  == "MES" and  item["side"] == "right" and len(str(item['Sold'])) != 0 and item['Sold'] !=0:
                    RightSideSum+=0     
                elif item["type"]  == "MES" and  item["side"] == "right":
                    RightSideSum += float(item['value'])
                    if float(item['point']) < float(starting_point):
                        RightClosingPoint +=0
                    if float(item['point']) > float(starting_point):
                         RightClosingPoint -= (abs(float(starting_point)-float(item['point'])))

                if item["type"]  == "ES" and  item["side"] == "right" and len(str(item['Sold'])) != 0 and item['Sold'] !=0:
                    RightSideSum+=0     
                elif item["type"] == "ES" and  item["side"]== "right":
                    RightSideSum += float(item['value']) * 10
                    if float(item['point']) < float(starting_point):
                        RightClosingPoint +=0
                    if float(item['point']) > float(starting_point):
                        RightClosingPoint -= (abs(float(starting_point)-float(item['point']))*10)

                if item["type"]  == "ST" and  item["side"] == "right" and len(str(item['Sold'])) != 0 and item['Sold'] !=0:
                    RightSideSum+=0    
                elif item["type"]  == "ST" and  item["side"] == "right": 
                    RightSideSum += 0
                    if float(item['point']) > float(starting_point):
                        RightClosingPoint -=abs(float(starting_point)-float(item['point']))
                    if float(item['point']) < float(starting_point):
                        RightClosingPoint += abs(float(starting_point)-float(item['point']))
            
            DataList.append({
                'starting_point': starting_point,
                'LeftSideSum': LeftSideSum,
                'RightSideSum': RightSideSum,
                'TotalSum': LeftSideSum+RightSideSum,
                'LeftClosingPoint': LeftClosingPoint+LeftSideSoldValue,
                'RightClosingPoint': RightClosingPoint+RightSideSoldValue,
                'TotalClosingPoint': (LeftClosingPoint+LeftSideSoldValue)+(RightClosingPoint+RightSideSoldValue),
                'TotalGainPoint': (LeftSideSum+RightSideSum)+(LeftClosingPoint+RightClosingPoint),
                'TotalGainValue': ((LeftSideSum+RightSideSum)+(LeftClosingPoint+RightClosingPoint))*5,
                'TotalRelializedValue': round(((LeftSideSoldValue+RightSideSoldValue)*5), 2),
                'TotalSummaryValue': (((LeftSideSum+RightSideSum)+(LeftClosingPoint+RightClosingPoint))*5)+((LeftSideSoldValue+RightSideSoldValue)*5),
            })

            LeftSideSum=0
            RightSideSum=0
            LeftClosingPoint=0
            RightClosingPoint=0
            LeftSideSoldValue=0
            RightSideSoldValue=0
         
        # print("DataList", DataList)

        return Response({'status': status.HTTP_200_OK, "message":"All Starting Point Balance Simulation.", "data": DataList})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def FormBuilderDataSaveAPI(request):
    try:
        form_data = request.data['form_data']
        type_data = request.data['type_data']

        # print("form_data", form_data)
        # print("form_data.keys()", form_data.keys())

        unique_table_ref_id = generate_unique_random_number()

        if type_data == 'Normal Type':
            f_data = Table_col_info.objects.filter(table_id=form_data['tableId'])
            for fd in f_data: 
                if fd.column_name in form_data.keys():
                    Table_data_info.objects.create(table_id=fd.table_id, table_col_id=fd.table_col_id, column_name=fd.column_name, column_data=form_data[fd.column_name], table_ref_id=unique_table_ref_id)
      
        return Response({'status': status.HTTP_200_OK, "message":"Successfully form data Saved"})

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])
def GETDYNAMICTABLEDATAINFOPI(request, table_id):
    try:
        # table_id = request.data['table_id']
        sections = {}
        items = []
        refId = []

       
        api_name_value = Table_data_info.objects.filter(table_id=table_id)
        for k in api_name_value:
            refId.append(k.table_ref_id)
                    
        refId = list(set(refId))

        for m in refId:
            for i in api_name_value:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_ref_id']=i.table_ref_id
                    sections['table_id']=i.table_id
                    sections['id']=i.table_data_id
                    sections['tab_rel_id']=i.tab_rel_id
                    sections['user_id']=i.user_id
            if sections != "":
                items.append(sections)   
                sections = {}

                     
        return Response({'status': status.HTTP_200_OK, "message":"success", "data": items})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

@api_view(['PUT'])
def UPDATEDYNAMICTABLEDATAINFOPI(request):
    try:
        table_data = request.data['table_data']
      
       
        for td in table_data:
          
            remove_key_td = without_keys(td, ['id', 'table_id', 'table_ref_id', 'tab_rel_id', 'user_id'])

            length_of_update_key = len(remove_key_td)
            count = 0
            for key, value in remove_key_td.items():
                try:
                    table_id_ref_data = Table_data_info.objects.get(table_id=td['table_id'], table_ref_id=td['table_ref_id'], column_name=key)
                    table_id_ref_data.column_data = value
                    table_id_ref_data.save()
                    count +=1 
                except Exception as error:
                    if  length_of_update_key >= count:
                        table_id_info_col_data = Table_col_info.objects.get(table_id=td['table_id'], column_name=key)
                        Table_data_info.objects.create(table_id=td['table_id'], table_col_id=table_id_info_col_data.table_col_id, column_data=value, column_name=key, table_ref_id=td['table_ref_id'], tab_rel_id= td['tab_rel_id'], user_id= td['user_id']) 
        
        return Response({'status': status.HTTP_200_OK, "message":"Successfully Updated"})
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
