# web scrapping api
import json
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import datetime
from datetime import datetime
import schedule
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
import requests
import py_compile



# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

from accountapp.DynamicFunction.Process_Log import ProcessLogFunction, InternalProcessLogFunction


def DateFormatingConvert(timed):
    currenttimestamp = datetime.strptime(
                timed, "%B %d, %Y").timestamp()
    currenttimedate =datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y')
    return currenttimedate  


def WebScrapFunction(Process_Id, web_data, Process_Name):
    gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    try: 
        exec(web_data)
        # url = "https://www.apple.com/newsroom/"
        # API_ENDPOINT = "https://itb-usa.a2hosted.com/account/apple-news-data-list/"
        # r = requests.get(url)
        # s= BeautifulSoup(r.text, "lxml")
        # applenews_tags= s.find_all("li", class_="tile-item")
        # appleNewsTime=[]
        # appleNewsTitle=[]
        # appleNewsURL=[]
        # appleNewsAllList=[]
        
        # print("106 start loop")
        # for i in applenews_tags:
        
        #     print("106 start loop in")
        #     appletile_tags= i.find_all("a", class_="tile")
                        
        #     for j in appletile_tags:
        #         appleheadline_tags= j.find_all("div", class_="tile__headline")
        #         for headlined in appleheadline_tags:
        #             appleNewsTitle.append(headlined.text.strip())
        
        #         appletime_tags= j.find_all("div", class_="tile__timestamp")
        #         for timed in appletime_tags:
        #             dateTime = DateFormatingConvert(timed.text)
        #             appleNewsTime.append(dateTime)
        
        
        #     for link in appletile_tags:
        #         appleNewsURL.append("https://www.apple.com/"+link.get('href'))
        
        
        
        # print("106 decoration data")
        # for timeindex in range(len(appleNewsTime)):
        #     for titleindex in range(len(appleNewsTitle)):
        #         for urlindex in range(len(appleNewsURL)):
        
        #             if timeindex==titleindex and urlindex==timeindex and urlindex==titleindex:
        #                 appleNewsDict = {
        #                     'time': appleNewsTime[timeindex],
        #                     'presenttimestand': appleNewsTime[0],
        #                     'headline': appleNewsTitle[titleindex],
        #                     'url': appleNewsURL[urlindex],
        #                 }
        
        #                 if appleNewsDict != "":
        #                     appleNewsAllList.append(appleNewsDict)
        #                     appleNewsDict={}
        # print("106 apicall", appleNewsAllList)
        # r = requests.post(url=API_ENDPOINT, json=appleNewsAllList)
        # print("75", r.text)
        # ProcessLogFunction(process_id="", log_date="", log_output_file="webssmsm", log_data_type="sucnsnns", log_process_name="", error="")

    except Exception as err:
        print("130 error", err)
        ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file="", log_data_type="error", log_process_name=Process_Name, error=err)
        # return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
def WrapperCodeValidate(web_data):
    gm = time.strftime("%a, %d %b %Y %X",
                  time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    try: 
        py_compile.compile(web_data, doraise=True)
        print("Code is valid.")
    except py_compile.PyCompileError as err:
        print(f"Code is not valid. Error: {err}")
        ProcessLogFunction(process_id="", log_date=currenttimedate, log_output_file="", log_data_type="error", log_process_name="", error=err)    
        
        