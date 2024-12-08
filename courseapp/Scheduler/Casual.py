
# web scrapping api
import json
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
# import datetime
from datetime import datetime, timedelta
import schedule
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
import requests

from django.conf import settings 

import heapq as hq 
import threading


# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

#import model
from courseapp.models import Table_data_info
from accountapp.DynamicFunction.Process_Log import ProcessLogFunction


from media.upload_file.process.CNBC import *
from media.upload_file.process.Reuters import *
from media.upload_file.process.APPLE import *
from media.upload_file.process.C3Ai import *
from media.upload_file.process.Custom import *



sucessList = []
errorList = []



  
    

def Process_Status_Change(Process_Id, table_ref_id, Process_Name, ProcessNotStarted):
    gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    try:
        
        process_data = Table_data_info.objects.filter(table_id=542, table_ref_id=table_ref_id)
        if len(process_data)!=0:
            for pd in process_data:
                if pd.table_col_id == 7:
                    process_update_data = Table_data_info.objects.get(table_id=542, table_col_id=pd.table_col_id, table_ref_id=pd.table_ref_id)
                    process_update_data.column_data = ProcessNotStarted
                    process_update_data.save()
                    # ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file="", log_data_type="inprogress", log_process_name=Process_Name, error=ProcessNotStarted)
                    

    except Exception as err:
        ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file="", log_data_type="errorwith server1 ", log_process_name=Process_Name, error=err)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)


         
def Process_Status_Update(Process_Id, table_ref_id, Process_Name):
    gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    try:
        process_data = Table_data_info.objects.filter(table_id=542, table_ref_id=table_ref_id)
        if len(process_data)!=0:
            for pd in process_data:
                if pd.table_col_id == 7:
                    process_update_data = Table_data_info.objects.get(table_id=542, table_col_id=pd.table_col_id, table_ref_id=pd.table_ref_id)
                    process_update_data.column_data = "Done"
                    process_update_data.save()
                    ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file="success with server1", log_data_type="Process Done", log_process_name=Process_Name, error="")

                    

    except Exception as err:
        ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file="", log_data_type="error with server1", log_process_name=Process_Name, error=err)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)  
 

def WrapperCodeValidate(Process_Id, code_string, Process_Name):
    gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    try:
        compiled_code = compile(code_string, filename='<string>', mode='exec')
        print("Syntax is correct.")
        return compiled_code
    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file="", log_data_type="error with server1", log_process_name=Process_Name, error=f"SyntaxError: {e}")
        # InternalProcessLogFunction(process_id="", log_date=currenttimedate, status_code={status.HTTP_400_BAD_REQUEST}, message=e)

         

def WrapperProcess(Process_Id, web_data, Process_Name, table_ref_id):
    gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    try:
        
        if "CNBC.py" == web_data:
            CNBC()
            Process_Status_Update(Process_Id, table_ref_id, Process_Name)
        elif "Reuters.py" == web_data:   
            Reuters()
            Process_Status_Update(Process_Id, table_ref_id, Process_Name)
        elif "APPLE.py" == web_data:   
            APPLE()
            Process_Status_Update(Process_Id, table_ref_id, Process_Name)
        elif "C3Ai.py" == web_data:   
            C3Ai()
            Process_Status_Update(Process_Id, table_ref_id, Process_Name)
        elif "Custom.py" == web_data:   
            Custom()
            Process_Status_Update(Process_Id, table_ref_id, Process_Name)
        
        # print("WrapperProcess", web_data)
        # result_code = WrapperCodeValidate(Process_Id, web_data, Process_Name)
        # print("141 result_code", result_code)
        # if result_code is not None:
        #     try:
        #         exec(result_code)
        #         Process_Status_Update(Process_Id, table_ref_id, Process_Name)
        #     except Exception as err:
        #         ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file="", log_data_type="error with server1", log_process_name=Process_Name, error=err)    

        # exec(WrapperCodeValidate(web_data))
        # exec(web_data)
        # WebScrapFunction(Process_Id, web_data, Process_Name)
    except Exception as err:
        ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file="", log_data_type="error with server1", log_process_name=Process_Name, error=err)


def Schedule_Start_Function(Process_Id, table_ref_id, Process_Name):
    gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
    currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    try:
        schedule_data = Table_data_info.objects.filter(table_id=542, column_data=Process_Id)
        if len(schedule_data)!=0:
            for s in schedule_data:
                data = Table_data_info.objects.filter(table_id=542, table_ref_id=s.table_ref_id)
                if len(data)!=0:
                    for d in data:
                        if d.table_col_id == 11:
                            WrapperProcess(Process_Id, d.column_data, Process_Name, table_ref_id)
                            # Process_Status_Update(Process_Id, table_ref_id, Process_Name)

    except Exception as err:
        ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file=" ", log_data_type="error with server1", log_process_name=Process_Name, error=err)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)  

        

def processStart(runTime, Process_Id):
    gm = time.strftime("%a, %d %b %Y %X",time.gmtime())
    currenttimestamp = datetime.strptime(gm, "%a, %d %b %Y %X").timestamp()
    currenttimedate = datetime.fromtimestamp(currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
    sec = datetime.fromtimestamp(currenttimestamp).strftime('%S') 
    try:
 
                        
        Process_data = Table_data_info.objects.get(table_id=542, column_data=Process_Id)
        print("187 Process_data", Process_data, Process_data.table_ref_id)
        
        sections = {}
        items = []
        refId = []
        casual_data = Table_data_info.objects.filter(table_id=542, table_ref_id=Process_data.table_ref_id)
        print("193 casual_data ", casual_data)
        for k in casual_data:
            refId.append(k.table_ref_id)
                   
        refId = list(set(refId))

        for m in refId:
            for i in casual_data:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_ref_id']=i.table_ref_id
            # if sections != "":
            #     # items.append(sections)   
            #     sections = {}
                
        print("207 sections data", sections)  
        
        # for i in items:
        #     runTime1 = datetime.strptime(i['Time'], "%Y-%m-%d %H:%M:%S") + timedelta(0, int(sec))
        #     if i['Process_Status'] != 'Done' and i['Process_Status'] != 'Process Invalid' and datetime.strptime(str(runTime1), "%Y-%m-%d %H:%M:%S").timestamp() < currenttimestamp:
        #         Process_Status_Change(i['Process_Id'], i['table_ref_id'], i['Process_Name'], 'Process Invalid')
        #     elif i['Process_Status'] != 'Process Invalid' and i['Process_Status'] != 'Done' and datetime.strptime(str(runTime1), "%Y-%m-%d %H:%M:%S").timestamp() == currenttimestamp:
        # if datetime.strptime(runTime, "%Y-%m-%d %H:%M:%S").timestamp() == currenttimestamp:
            # scheduler = BackgroundScheduler()
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(printCasual, 'interval', minutes=1)
        # scheduler.start()    
        # scheduler =  BlockingScheduler()
        print("runTime", runTime)
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(Schedule_Start_Function, 'date', run_date=runTime, args=[sections['Process_Id'], sections['table_ref_id'], sections['Process_Name']])
        # print("242",  scheduler.get_jobs())
        # scheduler.start()
        # if datetime.strptime(queue[0][0], "%Y-%m-%d %H:%M:%S").timestamp() == currenttimestamp:
        Schedule_Start_Function(sections['Process_Id'], sections['table_ref_id'], sections['Process_Name'])
        
       
        

    except Exception as err:
        ProcessLogFunction(process_id=Process_Id, log_date=currenttimedate, log_output_file=" ", log_data_type="error", log_process_name=Process_Name, error=err)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)        
        


def DataStore():
    try:
        sections = {}
        items = []
        refId = []
        casual_data = Table_data_info.objects.filter(table_id=542)
        for k in casual_data:
            refId.append(k.table_ref_id)
                   
        refId = list(set(refId))

        for m in refId:
            for i in casual_data:
                if i.table_ref_id==m:
                    sections[i.column_name]=i.column_data
                    sections['table_ref_id']=i.table_ref_id
            if sections != "":
                items.append(sections)   
                sections = {}
        
        
        unprocess_data = [x for x in items if x['Process_Status'] == 'unprocess' and x['Server_Name'] == 'Server1']
        
        inprocess_data = [x for x in items if x['Process_Status'] == 'Inprogress' and x['Server_Name'] == 'Server1']
        
        return unprocess_data, inprocess_data
        
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)


def CasualFunction():
    try:
        global queue  
        # queue = []
        gm = time.strftime("%a, %d %b %Y %X",
                  time.gmtime())
        currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
                        
        currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
      
        sec = datetime.fromtimestamp(
                        currenttimestamp).strftime('%S')                
                        
      
       
                        
        data = DataStore()
       
        for i in data:
            print("134 timestamp ", datetime.strptime(i['Time'], "%Y-%m-%d %H:%M:%S").timestamp(), currenttimestamp)
           
            runTime = datetime.strptime(i['Time'], "%Y-%m-%d %H:%M:%S") + timedelta(0, int(sec))
            
            if datetime.strptime(str(runTime), "%Y-%m-%d %H:%M:%S").timestamp() == currenttimestamp:
                Schedule_Start_Function(i['Process_Id'], i['table_ref_id'], i['Process_Name'])
            
            # hq.heappush(queue, (str(runTime), i['Process_Id']))
            # Process_Status_Change(i['Process_Id'], i['table_ref_id'], i['Process_Name'], 'Inprogress')
            

          
                
        # hq.heapify(queue) 
        # print("275 queue", queue)        
        # print("275 queue", queue[0][0], queue[0][1]) 
        # if len(queue) != 0:
            # time.sleep(30)
        # print("359", currenttimedate, queue[0][0], datetime.strptime(queue[0][0], "%Y-%m-%d %H:%M:%S").timestamp(), currenttimestamp)
        # ProcessLogFunction(process_id="", log_date=currenttimedate, log_output_file=" ", log_data_type="data", log_process_name=str(queue), error="")
        # if datetime.strptime(queue[0][0], "%Y-%m-%d %H:%M:%S").timestamp() == currenttimestamp:
        # # if queue[0][0] == currenttimedate:
        #     print("process start")
        #     processStart(queue[0][0], queue[0][1])
        #     hq.heappop(queue)

        # while len(queue) != 0:
        #     print("285 queue",  queue[0][0], queue[0][1])

        #     processStart(queue[0][0], queue[0][1])
        #     hq.heappop(queue)
            
            # print("365 abc", abc)
            # if abc != "Done":
            #     print("Not Done abc")
            #     time.sleep(1)
            # else:
            #     # pro =  hq.heappop(queue)
            #     print("285 queue",  queue[0][0], queue[0][1])
            #     # pro = hq.heappop(queue)
            #     # print("285 pro",  pro[0][0], pro[0][1])
            #     abc = processStart(queue[0][0], queue[0][1])
            #     hq.heappop(queue)
                
                
                
            #     interrupts = DataStore()
            #     print("379 interrupts", interrupts)
            #     for i in interrupts:
            #         print("379 interrupts i", i)
            #         runTime = datetime.strptime(i['Time'], "%Y-%m-%d %H:%M:%S") + timedelta(0, int(sec))
            #         hq.heappush(queue, (str(runTime), i['Process_Id']))
            #         Process_Status_Change(i['Process_Id'], i['table_ref_id'], i['Process_Name'], 'Inprogress')
                    
                
                
                
                # print("285 pro", pro)
            
            
            
            
            
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)
        
        
def QueueFunction():
    try:
        # global queue  
        # queue = []
        # queue = settings.QUEUE
        
        gm = time.strftime("%a, %d %b %Y %X",
                  time.gmtime())
        currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
                        
        currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d %H:%M:%S')
      
        sec = datetime.fromtimestamp(
                        currenttimestamp).strftime('%S')                
                        
      
       
                        
        unprocess_data, inprocess_data  = DataStore()
        # a, b, c = len(unprocess_data), len(inprocess_data), len(queue)
        # a, b = len(unprocess_data), len(inprocess_data)
        # ProcessLogFunction(process_id="", log_date=currenttimedate, log_output_file="len(unprocess_data), len(inprocess_data), len(queue)", log_data_type=a, log_process_name=b, error="")

        
        # if len(unprocess_data)!=0 and len(inprocess_data)==0:
        if len(unprocess_data)!=0:
       
            for i in unprocess_data:
                print("134 timestamp ", datetime.strptime(i['Time'], "%Y-%m-%d %H:%M:%S").timestamp(), currenttimestamp)
               
                runTime = datetime.strptime(i['Time'], "%Y-%m-%d %H:%M:%S") + timedelta(0, int(sec))
                
                if datetime.strptime(str(runTime), "%Y-%m-%d %H:%M:%S").timestamp() == currenttimestamp:
                    Process_Status_Change(i['Process_Id'], i['table_ref_id'], i['Process_Name'], 'Inprogress')
                    t1 = threading.Thread(target=Schedule_Start_Function, args=(i['Process_Id'], i['table_ref_id'], i['Process_Name']))
                    t1.start()
                    main_thread = threading.current_thread()
                    

                    for t1 in threading.enumerate():
                    	if t1 is main_thread:
                    	    continue
                    	t1.join()
                    	

                    # t1.join()
                    # Schedule_Start_Function(i['Process_Id'], i['table_ref_id'], i['Process_Name'])
                
            #     hq.heappush(queue, (str(runTime), i['Process_Id']))
            #     Process_Status_Change(i['Process_Id'], i['table_ref_id'], i['Process_Name'], 'Inprogress')
    
            # hq.heapify(queue) 
            # print("275 queue", queue)        
            # print("275 queue", queue[0][0], queue[0][1]) 
            # if len(queue) != 0:
                # time.sleep(30)
            # print("359", currenttimedate, queue[0][0], datetime.strptime(queue[0][0], "%Y-%m-%d %H:%M:%S").timestamp(), currenttimestamp)
            # ProcessLogFunction(process_id="", log_date=currenttimedate, log_output_file=" ", log_data_type="data", log_process_name=str(queue), error="")
            # if datetime.strptime(queue[0][0], "%Y-%m-%d %H:%M:%S").timestamp() == currenttimestamp:
            # # if queue[0][0] == currenttimedate:
            #     print("process start")
            #     processStart(queue[0][0], queue[0][1])
            #     hq.heappop(queue)
    
            # if len(queue) != 0:
            #     print("285 queue",  queue[0][0], queue[0][1])
            #     if datetime.strptime(queue[0][0], "%Y-%m-%d %H:%M:%S").timestamp() == currenttimestamp:
            #         # processStart(queue[0][0], queue[0][1])
            #         # t1 = threading.Thread(target=processStart, args=(queue[0][0], queue[0][1]))
            #         hq.heappop(queue)
                    
        # elif len(unprocess_data)!=0 and len(inprocess_data)!=0:  
        #     for i in unprocess_data:
        #         print("413", datetime.strptime(i['Time'], "%Y-%m-%d %H:%M:%S").timestamp(), currenttimestamp)
               
        #         runTime = datetime.strptime(i['Time'], "%Y-%m-%d %H:%M:%S") + timedelta(0, int(sec))
        #         hq.heappush(queue, (str(runTime), i['Process_Id']))
        #         Process_Status_Change(i['Process_Id'], i['table_ref_id'], i['Process_Name'], 'Inprogress')
                
        # elif len(unprocess_data)==0 and len(inprocess_data)!=0: 
        #     if len(queue) != 0:
        #         print("285 queue",  queue[0][0], queue[0][1])
        #         ProcessLogFunction(process_id="", log_date=currenttimedate, log_output_file=" ", log_data_type="data", log_process_name=str(queue), error="")
        #         ProcessLogFunction(process_id="", log_date=currenttimedate, log_output_file=" ", log_data_type="inprogress running", log_process_name="inprogress running", error="")
        #         if datetime.strptime(queue[0][0], "%Y-%m-%d %H:%M:%S").timestamp() == currenttimestamp:
        #             # processStart(queue[0][0], queue[0][1])
        #             hq.heappop(queue)
    

                
        # else:
        #     ProcessLogFunction(process_id="", log_date=currenttimedate, log_output_file=" ", log_data_type="do nothing", log_process_name="do nothing", error="")
            
                    
            
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)  


def JobStart():
    scheduler = BackgroundScheduler()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(CasualFunction, 'interval', minutes=1)
    scheduler.add_job(CasualFunction, 'cron', minute=1)
    ProcessLogFunction(process_id="", log_date="", log_output_file=" ", log_data_type="job start type 1", log_process_name="Job Started 1", error="")
    scheduler.start() 
    CasualFunction()
    ProcessLogFunction(process_id="", log_date="", log_output_file=" ", log_data_type="job start type 2", log_process_name="Job Started 2", error="")