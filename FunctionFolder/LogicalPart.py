import json
import os
import csv
import pandas as pd
import numpy as np
import requests
import yfinance as yf
from pandas_datareader import data as pdr

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.views import *

from courseapp.models import *

import asyncio
import random

from courseapp.helpers import *
from FunctionFolder.UserConfig import *

# global function
from FunctionFolder.WrapperFunc import *

from accountapp.threePointerd3Minp import *
from accountapp.MainPointerCalculation import *

def generate_unique_random_number():
    # Get the current time in seconds since the Epoch
    current_time = int(time.time() * 1000)  # Multiply by 1000 to include milliseconds
    
    # Generate a random number
    random_number = random.randint(0, 99999)
    
    # Combine the current time with the random number to ensure uniqueness
    unique_random_number = int(f"{current_time}{random_number}")
    
    return unique_random_number

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(8) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP 

def CurrentTimeStand():
    ct = datetime.now()
    return ct     

def write_json(new_data, filename, key):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data[key].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def DynamicTableData(data):
    try: 
        # print("54 data", data)
        sections = {}
        items = []
        refId = []

        for k in data:
            refId.append(k.table_ref_id)                       
        refId = list(set(refId))
        for m in refId:
            for i in data:
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
                refId=[] 

        return items      
    except Exception as error:
        return []
    
def DynamicColumnData(data):
    try:
        ColumnKey = []
        for key, value in data.items():
            if key=='table_id' or key =='table_ref_id' or key == 'id' or key =='tab_rel_id':
                pass
            elif key=='Status':
                ColumnKey.append({
                    'key': key,
                    'name': key,
                })
            else:
                ColumnKey.append({
                    'key': key,
                    'name': key,
                })
        ColumnKey.append({
            'key': 'Action',
            'name': 'Action',
        })        
        return ColumnKey
    
    except Exception as err:
        return []
    
def DatabaseSetUpFunction(userId):
    try:
        db=1
        db_set_up_data = Table_data_info.objects.filter(table_id=620, user_id=userId)
        main_data = DynamicTableData(db_set_up_data)
        for item in main_data:
            if item['ConfKey'] == "DB":
                db=int(item['ConfValue'])
        return db
    except Exception as error:
        return 1
    
def DynamicTableInsertFunction(data, user_id):
    try:
        db = DatabaseSetUpFunction(user_id)
        table_data=[]
        if db == 2: 
            for item in data:
                if item['user_id'] != "0":
                    table_data_list = Table_data_info2.objects.create(table_id=item['table_id'], table_col_id=item['table_col_id'], column_data=item['column_data'], column_name=item['column_name'], table_ref_id=item['table_ref_id'], tab_rel_id=item['tab_rel_id'], user_id=item['user_id']) 
                    table_data.append(table_data_list)
                else:
                    table_data_list = Table_data_info2.objects.create(table_id=item['table_id'], table_col_id=item['table_col_id'], column_data=item['column_data'], column_name=item['column_name'], table_ref_id=item['table_ref_id'], tab_rel_id=item['tab_rel_id']) 
                    table_data.append(table_data_list)

        else:
            for item in data:
                if item['user_id'] != "0":
                    table_data_list = Table_data_info2.objects.create(table_id=item['table_id'], table_col_id=item['table_col_id'], column_data=item['column_data'], column_name=item['column_name'], table_ref_id=item['table_ref_id'], tab_rel_id=item['tab_rel_id'], user_id=item['user_id']) 
                    table_data.append(table_data_list)
                else:
                    table_data_list = Table_data_info2.objects.create(table_id=item['table_id'], table_col_id=item['table_col_id'], column_data=item['column_data'], column_name=item['column_name'], table_ref_id=item['table_ref_id'], tab_rel_id=item['tab_rel_id']) 
                    table_data.append(table_data_list)

        return table_data
    
    except Exception as error:
        return [] 

def DynamicTableDeleteByRefIdFunction(table_id, user_id, table_ref_id):
    try:
        db = DatabaseSetUpFunction(user_id)
        if db == 2: 
            if user_id != "0":
                table_data = Table_data_info2.objects.filter(table_id=table_id, table_ref_id=table_ref_id, user_id=user_id) 
                for td in table_data:
                    record = Table_data_info2.objects.get(table_data_id=td.table_data_id, user_id=user_id)
                    record.delete()
                return True, "Delete Data Successfully."
            else:
                table_data = Table_data_info2.objects.filter(table_id=table_id, table_ref_id=table_ref_id)
                for td in table_data:
                    record = Table_data_info2.objects.get(table_data_id=td.table_data_id, user_id=user_id)
                    record.delete()
                return True, "Delete Data Successfully."

        else:
            if user_id != "0":
                table_data = Table_data_info2.objects.filter(table_id=table_id, table_ref_id=table_ref_id, user_id=user_id)
                for td in table_data:
                    record = Table_data_info2.objects.get(table_data_id=td.table_data_id, user_id=user_id)
                    record.delete()
                return True, "Delete Data Successfully."
            else:
                table_data = Table_data_info2.objects.filter(table_id=table_id, table_ref_id=table_ref_id)
                for td in table_data:
                    record = Table_data_info2.objects.get(table_data_id=td.table_data_id, user_id=user_id)
                    record.delete()
                return True, "Delete Data Successfully."

    except Exception as error:
        return False, "Something Problem, Can't Delete Data Problem."  
       


  
def ExistColumnDeleteRefIdBaseData(table_id, table_col_id, column_data, user_id):
    try:
        table_col_data_exist =Table_data_info2.objects.filter(table_id=table_id, table_col_id=table_col_id, user_id=user_id) 
        if len(table_col_data_exist)!=0:
            for tcd in table_col_data_exist:
                if tcd.column_data == column_data:
                    result, message = DynamicTableDeleteByRefIdFunction(tcd.table_id, tcd.user_id, tcd.table_ref_id)
                    return result, message
        else:
            False, "Table Col Id Data Not Found"        
    except Exception as error:
        return False, error
    
def ExistColumnCheck(table_id, table_col_id, column_data, user_id):
    try:
        table_col_data_exist =Table_data_info2.objects.filter(table_id=table_id, table_col_id=table_col_id, user_id=user_id) 
        if len(table_col_data_exist)!=0:
            count=0
            for tcd in table_col_data_exist:
                if tcd.column_data == column_data:
                    count+=1
            if count > 0:        
                return True, f"{tcd.column_name} {column_data} is already exists. Please try again another {tcd.column_name}"
            else:
                return False, f"Data is not found" 
        else:
            return False, f"Data is not found"        
    except Exception as error:
        return False, error




def JsonTableDataFetchFunction(userId):
    try:
        db = DatabaseSetUpFunction(userId)
        # print("94 db", db, type(db))
        if db == 1:
            tableItem = []
            tableSections = {}
            columnItem = []
            columnSections = {}

            TableInfoDtlfileName = main_media_url+f'/media/upload_file/user_data/table_info_dtl.json'
            TableColInfofileName = main_media_url+f'/media/upload_file/user_data/table_col_info.json'

            if os.path.isfile(TableInfoDtlfileName) and os.path.isfile(TableColInfofileName):
                f = open(TableInfoDtlfileName)
                json_data = json.load(f)
                table_info_dtl_data = json_data['table_info_dtl']  

                f1 = open(TableColInfofileName)
                json_data1 = json.load(f1)
                table_col_info_data = json_data1['table_col_info']    

                for tid in table_info_dtl_data:
                    if tid['user_id'] == userId:
                        tableSections['table']=tid['table_name']
                        tableSections['id']=tid['table_id']
                        tableSections['type']=tid['table_type']

                        table_col_info_data_filter = [x for x in table_col_info_data if x['table_id'] == tid['table_id'] and tid['user_id'] == userId]
                        for cdf in table_col_info_data_filter:
                            columnSections['no']=cdf['table_col_id']
                            columnSections['name']=cdf['column_name']
                            if len(columnSections)!=0:
                                columnItem.append(columnSections)
                                columnSections={}
                        tableSections['column']=columnItem       
                        if len(tableSections)!=0:
                            tableItem.append(tableSections)
                            tableSections={}
                            columnItem=[]
                return tableItem 
            return tableItem 
           
        elif db == 2:
            tableItem = []
            tableSections = {}
            columnItem = []
            columnSections = {}

            TableInfoDtlfileName = main_media_url+f'/media/upload_file/user_data/table_info_dtl2.json'
            TableColInfofileName = main_media_url+f'/media/upload_file/user_data/table_col_info2.json'

            if os.path.isfile(TableInfoDtlfileName) and os.path.isfile(TableColInfofileName):
                f = open(TableInfoDtlfileName)
                json_data = json.load(f)
                table_info_dtl_data = json_data['table_info_dtl2']  

                f1 = open(TableColInfofileName)
                json_data1 = json.load(f1)
                table_col_info_data = json_data1['table_col_info2']    

                for tid in table_info_dtl_data:
                    if tid['user_id'] == userId:
                        tableSections['table']=tid['table_name']
                        tableSections['id']=tid['table_id']
                        tableSections['type']=tid['table_type']

                        table_col_info_data_filter = [x for x in table_col_info_data if x['table_id'] == tid['table_id'] and tid['user_id'] == userId]
                        for cdf in table_col_info_data_filter:
                            columnSections['no']=cdf['table_col_id']
                            columnSections['name']=cdf['column_name']
                            if len(columnSections)!=0:
                                columnItem.append(columnSections)
                                columnSections={}
                        tableSections['column']=columnItem       
                        if len(tableSections)!=0:
                            tableItem.append(tableSections)
                            tableSections={}
                            columnItem=[]
                return tableItem 
            return tableItem    
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def ReferenceJsonTableDataFetchFunction(userId):
    try:
        db = DatabaseSetUpFunction(userId)
        fileName = main_media_url+'/media/upload_file/yahoo_finance_hist'
        dir_list = os.listdir(fileName)
        # print("181 dir_list", dir_list)
        tableItem = []
        tableSections = {}
        columnItem = []
        columnSections = {}

        for m in dir_list:
            # print("183 m", m)
            tableSections['table']=m
            tableSections['type']='reference_json_data'
            fileNameMain = main_media_url+'/media/upload_file/yahoo_finance_hist/'+m
            # print("185 fileNameMain", fileNameMain)
            if os.path.isfile(fileNameMain):
                f = open(fileNameMain)
                json_data = json.load(f)
                reference_json_data = json_data['data']  
                # print("189 reference_json_data", reference_json_data[0])
                count=0
                if len(reference_json_data) !=0:
                    for key, value in reference_json_data[0].items():
                        count+=1
                        # print(f"Key: {key}, Value: {value}, count: {count}")
                        columnSections['no']=count
                        columnSections['name']=key
                        if len(columnSections)!=0:
                            columnItem.append(columnSections)
                            columnSections={}

                    tableSections['column']=columnItem       
                    if len(tableSections)!=0:
                        tableItem.append(tableSections)
                        tableSections={}
                        columnItem=[]  
        # print("213 tableItem", tableItem)            
        return tableItem                 
         
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def TableDataFetchFunction(userId):
    try:
        db = DatabaseSetUpFunction(userId)
        if db == 1:
            tableItem = []
            tableSections = {}
            columnItem = []
            columnSections = {}
            table_info = Table_info_dtl.objects.filter(user_id=userId).order_by('-table_id')
            for t in table_info:
                tableSections['table']=t.table_name
                tableSections['id']=t.table_id
                tableSections['type']=t.table_type

                table_col_info = Table_col_info.objects.filter(table_id=t.table_id, user_id=userId)
                for c in table_col_info:
                    columnSections['no']=c.table_col_id
                    columnSections['name']=c.column_name
                    if len(columnSections)!=0:
                        columnItem.append(columnSections)
                        columnSections={}
                tableSections['column']=columnItem       
                if len(tableSections)!=0:
                    tableItem.append(tableSections)
                    tableSections={}
                    columnItem=[]
            return tableItem 
           
        elif db == 2:
            tableItem = []
            tableSections = {}
            columnItem = []
            columnSections = {}
            table_info = Table_info_dtl2.objects.filter(user_id=userId).order_by('-table_id')
            for t in table_info:
                tableSections['table']=t.table_name
                tableSections['id']=t.table_id
                tableSections['type']=t.table_type

                table_col_info = Table_col_info2.objects.filter(table_id=t.table_id, user_id=userId)
                for c in table_col_info:
                    columnSections['no']=c.table_col_id
                    columnSections['name']=c.column_name
                    if len(columnSections)!=0:
                        columnItem.append(columnSections)
                        columnSections={}
                tableSections['column']=columnItem       
                if len(tableSections)!=0:
                    tableItem.append(tableSections)
                    tableSections={}
                    columnItem=[]
            return tableItem 
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def FlowChartDataFetchFunction(userId):
    try:
        db = DatabaseSetUpFunction(userId)
        if db == 1:
            table_data = Table_data_info.objects.filter(table_id=471, user_id=userId).order_by('-table_ref_id')
            tableItem=DynamicTableData(table_data)
            # print("283 tableItem", tableItem)
            return tableItem 
           
        elif db == 2:
            table_data = Table_data_info2.objects.filter(table_id=471, user_id=userId).order_by('-table_ref_id')
            tableItem=DynamicTableData(table_data)
            # print("283 tableItem", tableItem)
            return tableItem 
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def AllTableDataFetchFunction(userId):
    try:
        db = DatabaseSetUpFunction(userId)
        if db == 1:
            tableItem = []
            tableSections = {}
            columnItem = []
            columnSections = {}
            table_info = Table_info_dtl.objects.filter(user_id=userId).order_by('-table_id')
            for t in table_info:
                tableSections['table']=t.table_name
                tableSections['id']=t.table_id
                tableSections['type']=t.table_type

                table_col_info = Table_col_info.objects.filter(table_id=t.table_id, user_id=userId)
                for c in table_col_info:
                    columnSections['no']=c.table_col_id
                    columnSections['name']=c.column_name
                    if len(columnSections)!=0:
                        columnItem.append(columnSections)
                        columnSections={}
                tableSections['column']=columnItem       
                if len(tableSections)!=0:
                    tableItem.append(tableSections)
                    tableSections={}
                    columnItem=[]

            TableInfoDtlfileName = main_media_url+f'/media/upload_file/user_data/table_info_dtl.json'
            TableColInfofileName = main_media_url+f'/media/upload_file/user_data/table_col_info.json'

            if os.path.isfile(TableInfoDtlfileName) and os.path.isfile(TableColInfofileName):
                f = open(TableInfoDtlfileName)
                json_data = json.load(f)
                table_info_dtl_data = json_data['table_info_dtl']  

                f1 = open(TableColInfofileName)
                json_data1 = json.load(f1)
                table_col_info_data = json_data1['table_col_info']    

                for tid in table_info_dtl_data:
                    if tid['user_id'] == userId:
                        tableSections['table']=tid['table_name']
                        tableSections['id']=tid['table_id']
                        tableSections['type']=tid['table_type']

                        table_col_info_data_filter = [x for x in table_col_info_data if x['table_id'] == tid['table_id'] and tid['user_id'] == userId]
                        for cdf in table_col_info_data_filter:
                            columnSections['no']=cdf['table_col_id']
                            columnSections['name']=cdf['column_name']
                            if len(columnSections)!=0:
                                columnItem.append(columnSections)
                                columnSections={}
                        tableSections['column']=columnItem       
                        if len(tableSections)!=0:
                            tableItem.append(tableSections)
                            tableSections={}
                            columnItem=[]
            
            return tableItem
        
        elif db == 2:
            tableItem = []
            tableSections = {}
            columnItem = []
            columnSections = {}
            table_info = Table_info_dtl2.objects.filter(user_id=userId).order_by('-table_id')
            for t in table_info:
                tableSections['table']=t.table_name
                tableSections['id']=t.table_id
                tableSections['type']=t.table_type

                table_col_info = Table_col_info2.objects.filter(table_id=t.table_id, user_id=userId)
                for c in table_col_info:
                    columnSections['no']=c.table_col_id
                    columnSections['name']=c.column_name
                    if len(columnSections)!=0:
                        columnItem.append(columnSections)
                        columnSections={}
                tableSections['column']=columnItem       
                if len(tableSections)!=0:
                    tableItem.append(tableSections)
                    tableSections={}
                    columnItem=[]
            
            TableInfoDtlfileName = main_media_url+f'/media/upload_file/user_data/table_info_dtl2.json'
            TableColInfofileName = main_media_url+f'/media/upload_file/user_data/table_col_info2.json'

            if os.path.isfile(TableInfoDtlfileName) and os.path.isfile(TableColInfofileName):
                f = open(TableInfoDtlfileName)
                json_data = json.load(f)
                table_info_dtl_data = json_data['table_info_dtl2']  

                f1 = open(TableColInfofileName)
                json_data1 = json.load(f1)
                table_col_info_data = json_data1['table_col_info2']    

                for tid in table_info_dtl_data:
                    if tid['user_id'] == userId:
                        tableSections['table']=tid['table_name']
                        tableSections['id']=tid['table_id']
                        tableSections['type']=tid['table_type']

                        table_col_info_data_filter = [x for x in table_col_info_data if x['table_id'] == tid['table_id'] and tid['user_id'] == userId]
                        for cdf in table_col_info_data_filter:
                            columnSections['no']=cdf['table_col_id']
                            columnSections['name']=cdf['column_name']
                            if len(columnSections)!=0:
                                columnItem.append(columnSections)
                                columnSections={}
                        tableSections['column']=columnItem       
                        if len(tableSections)!=0:
                            tableItem.append(tableSections)
                            tableSections={}
                            columnItem=[]

            return tableItem

    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def GetTableDataRelIdInfoByUserFunction(userId, tableId, tableColId, tabRelId):
    try:
        db = DatabaseSetUpFunction(userId)
        user_id=userId
        table_id= tableId
        table_col_id=tableColId
        tab_rel_id=tabRelId
        if db == 1:
            if user_id != "0":
                startTime = CurrentTimeFunc()
                APICALLFUNCTION('get_table_data_rel_id_info', 'null')
                if table_col_id==0 and tab_rel_id=="":
                    data_t = Table_data_info.objects.filter(table_id=table_id, user_id=user_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))	
                    return data
                elif tab_rel_id=="":
                    data_t = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id, user_id=user_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))
                    return data
                elif table_col_id==0:
                    data_t = Table_data_info.objects.filter(table_id=table_id, tab_rel_id=tab_rel_id, user_id=user_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))
                    return data
                        
                data_t = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id, tab_rel_id=tab_rel_id, user_id=user_id)
                data = DynamicTableData(data_t)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))    
                return data
            
            else:
                startTime = CurrentTimeFunc()
                APICALLFUNCTION('get_table_data_rel_id_info', 'null')
                if table_col_id==0 and tab_rel_id=="":
                    data_t = Table_data_info.objects.filter(table_id=table_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))	
                    return data
                elif tab_rel_id=="":
                    data_t = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))
                    return data
                elif table_col_id==0:
                    data_t = Table_data_info.objects.filter(table_id=table_id, tab_rel_id=tab_rel_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))
                    return data
                        
                data_t = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id, tab_rel_id=tab_rel_id)
                data = DynamicTableData(data_t)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_rel_id_info", "model data", value_count, round(loadTime, 6))    
                return data
        
        elif db == 2:
            if user_id != "0":
                startTime = CurrentTimeFunc()
                APICALLFUNCTION('get_table_data_rel_id_info2', 'null')
                if table_col_id==0 and tab_rel_id=="":
                    data_t = Table_data_info2.objects.filter(table_id=table_id, user_id=user_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info2", "model data", value_count, round(loadTime, 6))	
                    return data
                elif tab_rel_id=="":
                    data_t = Table_data_info2.objects.filter(table_id=table_id, table_col_id=table_col_id, user_id=user_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info2", "model data", value_count, round(loadTime, 6))
                    return data
                elif table_col_id==0:
                    data_t = Table_data_info2.objects.filter(table_id=table_id, tab_rel_id=tab_rel_id, user_id=user_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info2", "model data", value_count, round(loadTime, 6))
                    return data
                        
                data_t = Table_data_info2.objects.filter(table_id=table_id, table_col_id=table_col_id, tab_rel_id=tab_rel_id, user_id=user_id)
                data = DynamicTableData(data_t)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_rel_id_info2", "model data", value_count, round(loadTime, 6))    
                return data
            
            else:
                startTime = CurrentTimeFunc()
                APICALLFUNCTION('get_table_data_rel_id_info2', 'null')
                if table_col_id==0 and tab_rel_id=="":
                    data = Table_data_info2.objects.filter(table_id=table_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info2", "model data", value_count, round(loadTime, 6))	
                    return data
                elif tab_rel_id=="":
                    data_t = Table_data_info2.objects.filter(table_id=table_id, table_col_id=table_col_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info2", "model data", value_count, round(loadTime, 6))
                    return data
                elif table_col_id==0:
                    data_t = Table_data_info2.objects.filter(table_id=table_id, tab_rel_id=tab_rel_id)
                    data = DynamicTableData(data_t)
                    endTime = CurrentTimeFunc()
                    loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                    value_count = ValueCountFunc(data)
                    DataFetch_Static("get_table_data_rel_id_info2", "model data", value_count, round(loadTime, 6))
                    return data
                        
                data_t = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id, tab_rel_id=tab_rel_id)
                data = DynamicTableData(data_t)
                endTime = CurrentTimeFunc()
                loadTime = (datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')).total_seconds() / 60
                value_count = ValueCountFunc(data)
                DataFetch_Static("get_table_data_rel_id_info2", "model data", value_count, round(loadTime, 6))    
                return data
        

    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def TableDataColumnUpdateFunction(user_id, table_id, table_ref_id, column_name, column_data):
    try:
        db = DatabaseSetUpFunction(user_id)
        if db == 1:
            if user_id != "0":      
                update_column_data = Table_data_info.objects.get(table_id=table_id, table_ref_id=table_ref_id, column_name=column_name, user_id=user_id)
                update_column_data.column_data=column_data
                update_column_data.save()
                return True
            else:
                update_column_data = Table_data_info.objects.get(table_id=table_id, table_ref_id=table_ref_id, column_name=column_name)
                update_column_data.column_data=column_data
                update_column_data.save()
                return True

        
        elif db == 2:
            if user_id != "0":
                update_column_data = Table_data_info2.objects.get(table_id=table_id, table_ref_id=table_ref_id, column_name=column_name, user_id=user_id)
                # print("595 update_column_data", update_column_data)
                update_column_data.column_data=column_data
                update_column_data.save()
                return True
            else:
                update_column_data = Table_data_info2.objects.get(table_id=table_id, table_ref_id=table_ref_id, column_name=column_name)
                update_column_data.column_data=column_data
                update_column_data.save()
                return True

    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def DynamicTableCreateFunction(data):
    try:
        print("696 data", data)
        db = DatabaseSetUpFunction(data['user_id'])
        print("698 db", db)
        table_data = []
        if db == 2: 
            if data['table_id'] == 39:
                if data['mode'].lower() == 'create':
                    result, message = ExistColumnCheck(39, 3, data['data'][2]['column_data'], data['user_id'])
                    result1, message1 = ExistColumnCheck(39, 4, data['data'][3]['column_data'], data['user_id'])
                    if result == True:
                        return [], False, message 
                    if result1 == True:
                        return [], False, message1 
                    
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully." 
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(39, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
                
            if data['table_id'] == 40:
                if data['mode'].lower() == 'create':
                    # result, message = ExistColumnCheck(39, 3, data['data'][2]['column_data'], data['user_id'])
                    # result1, message1 = ExistColumnCheck(39, 4, data['data'][3]['column_data'], data['user_id'])
                    # if result == True:
                    #     return [], False, message 
                    # if result1 == True:
                    #     return [], False, message1 
                    
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully." 
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(40, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
                
            if data['table_id'] == 41:
                if data['mode'].lower() == 'create':
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully." 
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(41, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
            
            if data['table_id'] == 42:
                if data['mode'].lower() == 'create':
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully." 
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(42, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
            
            if data['table_id'] == 43:
                if data['mode'].lower() == 'create':
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully." 
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(43, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
                
            if data['table_id'] == 46:
                if data['mode'].lower() == 'create':
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully." 
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(46, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
                   
        else:
            if data['table_id'] == 39:
                if data['mode'].lower() == 'create':
                    result, message = ExistColumnCheck(39, 3, data['data'][2]['column_data'], data['user_id'])
                    result1, message1 = ExistColumnCheck(39, 4, data['data'][3]['column_data'], data['user_id'])
                    if result == True:
                        return [], False, message 
                    if result1 == True:
                        return [], False, message1

                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully."
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(39, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
                
            if data['table_id'] == 40:
                if data['mode'].lower() == 'create':
                    # result, message = ExistColumnCheck(39, 3, data['data'][2]['column_data'], data['user_id'])
                    # result1, message1 = ExistColumnCheck(39, 4, data['data'][3]['column_data'], data['user_id'])
                    # if result == True:
                    #     return [], False, message 
                    # if result1 == True:
                    #     return [], False, message1

                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully."
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(40, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
                
            if data['table_id'] == 41:
                if data['mode'].lower() == 'create':
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully."
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(41, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
                
            if data['table_id'] == 42:
                if data['mode'].lower() == 'create':
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully."
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(42, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
                

            if data['table_id'] == 43:
                if data['mode'].lower() == 'create':
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully."
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(43, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 
            
            if data['table_id'] == 46:
                if data['mode'].lower() == 'create':
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Created Successfully."
                   
                if data['mode'].lower() == 'update':
                    result, message = DynamicTableDeleteByRefIdFunction(46, data['user_id'], data['table_ref_id'])
                    if result == False:
                        return [], False, message 
                 
                    table_data = DynamicTableInsertFunction(data['data'], data['user_id'])
                    d_data = DynamicTableData(table_data)
                    return d_data, True, "Table Data Updated Successfully." 

    except Exception as error:
        return [], False, f"Something errors or {error}"

def DynamicTableGetFunction(data):
    try:
       
        db = DatabaseSetUpFunction(data['user_id'])
        table_data = []
        if db == 2: 
            if data['user_id'] != "0":
                if data['table_id'] != 0 and data['table_ref_id'] != "":
                    table_data = Table_data_info2.objects.filter(table_id=data['table_id'], table_ref_id=data['table_ref_id'], user_id=data['user_id']) 
                else:
                    table_data = Table_data_info2.objects.filter(table_id=data['table_id'], user_id=data['user_id']) 
            else:
                if data['table_id'] != 0 and data['table_ref_id'] != "":
                    table_data = Table_data_info2.objects.filter(table_id=data['table_id'], table_ref_id=data['table_ref_id']) 
                else:
                    table_data = Table_data_info2.objects.filter(table_id=data['table_id']) 

        else:
            if data['user_id'] != "0":
                if data['table_id'] != 0 and data['table_ref_id'] != "":
                    table_data = Table_data_info2.objects.filter(table_id=data['table_id'], table_ref_id=data['table_ref_id'], user_id=data['user_id']) 
                else:
                    table_data = Table_data_info2.objects.filter(table_id=data['table_id'], user_id=data['user_id']) 
            else:
                if data['table_id'] != 0 and data['table_ref_id'] != "":
                    table_data = Table_data_info2.objects.filter(table_id=data['table_id'], table_ref_id=data['table_ref_id']) 
                else:
                    table_data = Table_data_info2.objects.filter(table_id=data['table_id']) 

        d_data = DynamicTableData(table_data)
        column_name = DynamicColumnData(d_data[0])
        return d_data, column_name, True, "Dynamic Data Fetch Successfully."
    
    except Exception as error:
        return [], [], False, f"Something errors or {error}"

def DynamicTableGetByRefIdFunction(table_id, user_id, table_ref_id):
    try:
        db = DatabaseSetUpFunction(user_id)
        table_data = []
        if db == 2: 
            if user_id != "0":
                table_data = Table_data_info2.objects.filter(table_id=table_id, table_ref_id=table_ref_id, user_id=user_id) 
            else:
                table_data = Table_data_info2.objects.filter(table_id=table_id, table_ref_id=table_ref_id) 

        else:
            if user_id != "0":
                table_data = Table_data_info2.objects.filter(table_id=table_id, table_ref_id=table_ref_id, user_id=user_id) 
            else:
                table_data = Table_data_info2.objects.filter(table_id=table_id, table_ref_id=table_ref_id) 

        d_data = DynamicTableData(table_data)
        return d_data
    
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def CouponCheckFunction(data):
    try:
        db = DatabaseSetUpFunction(data['user_id'])
        table_data = []
        if db == 2: 
            try:
                data = Table_data_info2.objects.filter(table_id=data['table_id'], column_data=data['coupon_code']) 
                for d in data:
                    table_data += Table_data_info2.objects.filter(table_id=d.table_id, table_ref_id=d.table_ref_id) 

                d_data = DynamicTableData(table_data)
                # Convert strings to datetime objects
                start_dt = datetime.strptime(d_data[0]['coupon_start_date'], "%Y-%m-%d %H:%M:%S")
                end_dt = datetime.strptime(d_data[0]['coupon_ending_date'], "%Y-%m-%d %H:%M:%S")

                # Calculate the difference
                difference = end_dt - datetime.now()  
                
                if difference.days < 0:
                    return [], False, "Coupon Code time is expired." 
                return d_data, True, "Valid Coupon Code Found Successfully." 
            except:
                return [], False, "Coupon Code is not Valid. Please Valid Coupon Code." 
                     
        else:
            try:
                data = Table_data_info2.objects.filter(table_id=data['table_id'], column_data=data['coupon_code']) 
                for d in data:
                    table_data += Table_data_info2.objects.filter(table_id=d.table_id, table_ref_id=d.table_ref_id) 

                d_data = DynamicTableData(table_data)
                # Convert strings to datetime objects
                start_dt = datetime.strptime(d_data[0]['coupon_start_date'], "%Y-%m-%d %H:%M:%S")
                end_dt = datetime.strptime(d_data[0]['coupon_ending_date'], "%Y-%m-%d %H:%M:%S")

                # Calculate the difference
                difference = end_dt - datetime.now()  

                if difference.days < 0:
                    return [], False, "Coupon Code time is expired." 
                return d_data, True, "Valid Coupon Code Found Successfully." 
            except:
                return [], False, "Coupon Code is not Valid. Please Valid Coupon Code." 
                
    except Exception as error:
        return [], False, f"Something errors or {error}"
    
    
def UserRoleBaseRegisterFunction(data):
    try:
        uniqueKey = generate_unique_random_number()
        user_count = Table_data_info2.objects.filter(table_id=47).count()
        user_count_number = Table_data_info2.objects.filter(column_name="user_id", table_id=47).count()
        if data['create_by'].lower() == 'admin':
            if data['required']['email'] != "":
                if data['email'] != "": 
                    if Table_data_info2.objects.filter(column_data=data['email'], table_id=47).exists():
                        raise Exception("Email already exists. Please try again another email.")
                    userEmail = Table_data_info2(table_id=47, table_col_id=1, user_id=user_count_number+1, column_data=data['email'], table_ref_id=uniqueKey, col_data_type="String", column_name='email') 
                    userEmail.save()
                else: 
                    raise Exception("Email is required.")
            else:
                userEmail = Table_data_info2(table_id=47, table_col_id=1, user_id=user_count_number+1, column_data=data['email'], table_ref_id=uniqueKey, col_data_type="String", column_name='email') 
                userEmail.save()
                
            if data['required']['username'] != "":
                if data['username'] != "": 
                    if Table_data_info2.objects.filter(column_data=data['username'], table_id=47).exists():
                        raise Exception("Username already exists. Please try again another username.")
                    username = Table_data_info2(table_id=47, table_col_id=2, user_id=user_count_number+1, column_data=data['username'], table_ref_id=uniqueKey, col_data_type="String", column_name='username') 
                    username.save()
                else: 
                    raise Exception("Username is required.")
            else:
                username = Table_data_info2(table_id=47, table_col_id=2, user_id=user_count_number+1, column_data=data['username'], table_ref_id=uniqueKey, col_data_type="String", column_name='username') 
                username.save()

            if data['required']['phone_number'] != "":
                if data['phone_number'] != "": 
                    if Table_data_info2.objects.filter(column_data=data['phone_number'], table_id=47).exists():
                        raise Exception("Phone Number already exists. Please try again another Phone Number.")
                    phone_number = Table_data_info2(table_id=47, table_col_id=3, user_id=user_count_number+1, column_data=data['phone_number'], table_ref_id=uniqueKey, col_data_type="string", column_name='phone_number') 
                    phone_number.save()
                else: 
                    raise Exception("Phone Number is required.")
            else:
                phone_number = Table_data_info2(table_id=47, table_col_id=3, user_id=user_count_number+1, column_data=data['phone_number'], table_ref_id=uniqueKey, col_data_type="String", column_name='phone_number') 
                phone_number.save()

            firstName = Table_data_info2(table_id=47, table_col_id=4, user_id=user_count_number+1, column_data=data['first_name'], table_ref_id=uniqueKey, col_data_type="String", column_name='first_name') 
            firstName.save()

            LastName = Table_data_info2(table_id=47, table_col_id=5, user_id=user_count_number+1, column_data=data['last_name'], table_ref_id=uniqueKey, col_data_type="String", column_name='last_name') 
            LastName.save() 
            
            middle_name = Table_data_info2(table_id=47, table_col_id=6, user_id=user_count_number+1, column_data="M", table_ref_id=uniqueKey, col_data_type="String", column_name='middle_name') 
            middle_name.save()   

            Password = Table_data_info2(table_id=47, table_col_id=7, user_id=user_count_number+1, column_data=data['password'], table_ref_id=uniqueKey, col_data_type="String", column_name='password') 
            Password.save()

            userRole = Table_data_info2(table_id=47, table_col_id=8, user_id=user_count_number+1, column_data=data['user_role_type'].lower(), table_ref_id=uniqueKey, col_data_type="String", column_name='user_role_type') 
            userRole.save()
            if data['user_role_type'].lower() == 'admin':
                userIsActive = Table_data_info2(table_id=47, table_col_id=9, user_id=user_count_number+1, column_data="True", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_active') 
                userIsActive.save()
                userIsSuperuser = Table_data_info2(table_id=47, table_col_id=10, user_id=user_count_number+1, column_data="True", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_superuser') 
                userIsSuperuser.save()
                userEmailActivationFlag = Table_data_info2(table_id=47, table_col_id=11, user_id=user_count_number+1, column_data="True", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_email_verified') 
                userEmailActivationFlag.save()
            if data['user_role_type'].lower() != 'admin':
                userIsActive = Table_data_info2(table_id=47, table_col_id=9, user_id=user_count_number+1, column_data="True", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_active') 
                userIsActive.save()
                userIsSuperuser = Table_data_info2(table_id=47, table_col_id=10, user_id=user_count_number+1, column_data="False", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_superuser') 
                userIsSuperuser.save()
                userEmailActivationFlag = Table_data_info2(table_id=47, table_col_id=11, user_id=user_count_number+1, column_data="True", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_email_verified') 
                userEmailActivationFlag.save()
            
            
            userUserId = Table_data_info2(table_id=47, table_col_id=12, user_id=user_count_number+1, column_data=user_count_number+1, table_ref_id=uniqueKey, col_data_type="Int", column_name='user_id') 
            userUserId.save()
            gender = Table_data_info2(table_id=47, table_col_id=13, user_id=user_count_number+1, column_data="Gender", table_ref_id=uniqueKey, col_data_type="string", column_name='gender') 
            gender.save()
            dob = Table_data_info2(table_id=47, table_col_id=14, user_id=user_count_number+1, column_data="dd-mm-yyyy", table_ref_id=uniqueKey, col_data_type="datetimefield", column_name='dob') 
            dob.save()
            address = Table_data_info2(table_id=47, table_col_id=15, user_id=user_count_number+1, column_data="address", table_ref_id=uniqueKey, col_data_type="string", column_name='address') 
            address.save()
            country = Table_data_info2(table_id=47, table_col_id=16, user_id=user_count_number+1, column_data="country", table_ref_id=uniqueKey, col_data_type="string", column_name='country') 
            country.save()
            city = Table_data_info2(table_id=47, table_col_id=17, user_id=user_count_number+1, column_data="city", table_ref_id=uniqueKey, col_data_type="string", column_name='city') 
            city.save()
            state = Table_data_info2(table_id=47, table_col_id=18, user_id=user_count_number+1, column_data="state", table_ref_id=uniqueKey, col_data_type="string", column_name='state') 
            state.save()
            userZipCode = Table_data_info2(table_id=47, table_col_id=19, user_id=user_count_number+1, column_data="0", table_ref_id=uniqueKey, col_data_type="String", column_name='zipcode') 
            userZipCode.save()
            userProfilePicture = Table_data_info2(table_id=47, table_col_id=20, user_id=user_count_number+1, column_data="/media/userProfilePicture/default.jpg", table_ref_id=uniqueKey, col_data_type="String", column_name='user_profile_picture') 
            userProfilePicture.save()
        
        
        else:
            if data['required']['email'] != "":
                if data['email'] != "": 
                    if Table_data_info2.objects.filter(column_data=data['email'], table_id=47).exists():
                        raise Exception("Email already exists. Please try again another email.")
                    userEmail = Table_data_info2(table_id=47, table_col_id=1, user_id=user_count_number+1, column_data=data['email'], table_ref_id=uniqueKey, col_data_type="String", column_name='email') 
                    userEmail.save()
                else: 
                    raise Exception("Email is required.")
            else:
                userEmail = Table_data_info2(table_id=47, table_col_id=1, user_id=user_count_number+1, column_data=data['email'], table_ref_id=uniqueKey, col_data_type="String", column_name='email') 
                userEmail.save()
                
            if data['required']['username'] != "":
                if data['username'] != "": 
                    if Table_data_info2.objects.filter(column_data=data['username'], table_id=47).exists():
                        raise Exception("Username already exists. Please try again another username.")
                    username = Table_data_info2(table_id=47, table_col_id=2, user_id=user_count_number+1, column_data=data['username'], table_ref_id=uniqueKey, col_data_type="String", column_name='username') 
                    username.save()
                else: 
                    raise Exception("Username is required.")
            else:
                username = Table_data_info2(table_id=47, table_col_id=2, user_id=user_count_number+1, column_data=data['username'], table_ref_id=uniqueKey, col_data_type="String", column_name='username') 
                username.save()

            if data['required']['phone_number'] != "":
                if data['phone_number'] != "": 
                    if Table_data_info2.objects.filter(column_data=data['phone_number'], table_id=47).exists():
                        raise Exception("Phone Number already exists. Please try again another Phone Number.")
                    phone_number = Table_data_info2(table_id=47, table_col_id=3, user_id=user_count_number+1, column_data=data['phone_number'], table_ref_id=uniqueKey, col_data_type="string", column_name='phone_number') 
                    phone_number.save()
                else: 
                    raise Exception("Phone Number is required.")
            else:
                phone_number = Table_data_info2(table_id=47, table_col_id=3, user_id=user_count_number+1, column_data=data['phone_number'], table_ref_id=uniqueKey, col_data_type="String", column_name='phone_number') 
                phone_number.save()

            firstName = Table_data_info2(table_id=47, table_col_id=4, user_id=user_count_number+1, column_data=data['first_name'], table_ref_id=uniqueKey, col_data_type="String", column_name='first_name') 
            firstName.save()

            LastName = Table_data_info2(table_id=47, table_col_id=5, user_id=user_count_number+1, column_data=data['last_name'], table_ref_id=uniqueKey, col_data_type="String", column_name='last_name') 
            LastName.save() 
            
            middle_name = Table_data_info2(table_id=47, table_col_id=6, user_id=user_count_number+1, column_data="M", table_ref_id=uniqueKey, col_data_type="String", column_name='middle_name') 
            middle_name.save()   

            Password = Table_data_info2(table_id=47, table_col_id=7, user_id=user_count_number+1, column_data=data['password'], table_ref_id=uniqueKey, col_data_type="String", column_name='password') 
            Password.save()

            userRole = Table_data_info2(table_id=47, table_col_id=8, user_id=user_count_number+1, column_data=data['user_role_type'].lower(), table_ref_id=uniqueKey, col_data_type="String", column_name='user_role_type') 
            userRole.save()
            if data['user_role_type'].lower() == 'admin':
                userIsActive = Table_data_info2(table_id=47, table_col_id=9, user_id=user_count_number+1, column_data="True", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_active') 
                userIsActive.save()
                userIsSuperuser = Table_data_info2(table_id=47, table_col_id=10, user_id=user_count_number+1, column_data="True", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_superuser') 
                userIsSuperuser.save()
                userEmailActivationFlag = Table_data_info2(table_id=47, table_col_id=11, user_id=user_count_number+1, column_data="True", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_email_verified') 
                userEmailActivationFlag.save()
            if data['user_role_type'].lower() != 'admin':
                userIsActive = Table_data_info2(table_id=47, table_col_id=9, user_id=user_count_number+1, column_data="False", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_active') 
                userIsActive.save()
                userIsSuperuser = Table_data_info2(table_id=47, table_col_id=10, user_id=user_count_number+1, column_data="False", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_superuser') 
                userIsSuperuser.save()
                userEmailActivationFlag = Table_data_info2(table_id=47, table_col_id=11, user_id=user_count_number+1, column_data="False", table_ref_id=uniqueKey, col_data_type="Boolean", column_name='is_email_verified') 
                userEmailActivationFlag.save()
            
            
            userUserId = Table_data_info2(table_id=47, table_col_id=12, user_id=user_count_number+1, column_data=user_count_number+1, table_ref_id=uniqueKey, col_data_type="Int", column_name='user_id') 
            userUserId.save()
            gender = Table_data_info2(table_id=47, table_col_id=13, user_id=user_count_number+1, column_data="Gender", table_ref_id=uniqueKey, col_data_type="string", column_name='gender') 
            gender.save()
            dob = Table_data_info2(table_id=47, table_col_id=14, user_id=user_count_number+1, column_data="dd-mm-yyyy", table_ref_id=uniqueKey, col_data_type="datetimefield", column_name='dob') 
            dob.save()
            address = Table_data_info2(table_id=47, table_col_id=15, user_id=user_count_number+1, column_data="address", table_ref_id=uniqueKey, col_data_type="string", column_name='address') 
            address.save()
            country = Table_data_info2(table_id=47, table_col_id=16, user_id=user_count_number+1, column_data="country", table_ref_id=uniqueKey, col_data_type="string", column_name='country') 
            country.save()
            city = Table_data_info2(table_id=47, table_col_id=17, user_id=user_count_number+1, column_data="city", table_ref_id=uniqueKey, col_data_type="string", column_name='city') 
            city.save()
            state = Table_data_info2(table_id=47, table_col_id=18, user_id=user_count_number+1, column_data="state", table_ref_id=uniqueKey, col_data_type="string", column_name='state') 
            state.save()
            userZipCode = Table_data_info2(table_id=47, table_col_id=19, user_id=user_count_number+1, column_data="0", table_ref_id=uniqueKey, col_data_type="String", column_name='zipcode') 
            userZipCode.save()
            userProfilePicture = Table_data_info2(table_id=47, table_col_id=20, user_id=user_count_number+1, column_data="/media/userProfilePicture/default.jpg", table_ref_id=uniqueKey, col_data_type="String", column_name='user_profile_picture') 
            userProfilePicture.save()

        table_data = Table_data_info2.objects.filter(table_id=47, table_ref_id=uniqueKey)
        d_data = DynamicTableData(table_data)
        return d_data, True, "User Created Successfully."

    except Exception as error:
        return [], False, f"Something errors or {error}"


def LoginCheck(data, l_data, p_data):
    try:
        if l_data.table_ref_id==p_data.table_ref_id and l_data.user_id==p_data.user_id:
            flag_check = Table_data_info2.objects.filter(table_id=47, table_ref_id=l_data.table_ref_id, user_id=l_data.user_id)

            email_active = []
            user_active = []
            for i in flag_check:
                if i.column_name=="is_email_verified" and i.column_data=="True" and i.table_ref_id==l_data.table_ref_id and i.user_id==l_data.user_id and i.table_col_id==11:
                    email_active.append(i.column_data)
                if i.column_name=="is_active" and i.column_data=="True" and i.table_ref_id==l_data.table_ref_id and i.user_id==l_data.user_id and i.table_col_id==9:
                    user_active.append(i.column_data)
                                 
            if email_active and user_active:
                if email_active[0]=="True" and user_active[0]=="True":
                    user_otp=generateOTP()
                    cts = CurrentTimeStand()
                    if Table_data_info2.objects.filter(table_id=48, column_data=data['email_or_username_or_phone_number'], user_id=l_data.user_id).exists():
                        otp_check_email = Table_data_info2.objects.get(table_id=48, column_data=data['email_or_username_or_phone_number'], user_id=l_data.user_id)
                        otp_check = Table_data_info2.objects.filter(table_id=48, table_ref_id=otp_check_email.table_ref_id, user_id=otp_check_email.user_id)
                        count = 0
                        for i in otp_check:
                            if i.table_id==48 and i.table_col_id==2 and i.column_name=="user_otp" and i.table_ref_id==otp_check_email.table_ref_id and i.user_id==otp_check_email.user_id:
                                otp_update = Table_data_info2.objects.get(table_id=i.table_id, table_col_id=i.table_col_id, column_name=i.column_name, table_ref_id=otp_check_email.table_ref_id, user_id=otp_check_email.user_id)
                                otp_update.column_data=user_otp
                                otp_update.save()
                                count=count+1
                                
                                
                            if i.table_id==48 and i.table_col_id==4 and i.column_name=="timestamp" and i.table_ref_id==otp_check_email.table_ref_id and i.user_id==otp_check_email.user_id:
                                cts_update = Table_data_info2.objects.get(table_id=i.table_id, table_col_id=i.table_col_id, column_name=i.column_name, table_ref_id=otp_check_email.table_ref_id, user_id=otp_check_email.user_id)
                                cts_update.column_data=cts
                                cts_update.save()
                                count=count+1
                            
                            if count == 2:
                                # send_user_otp_mail(email, user_otp, cts)
                                # return UserSignIn(result=True, otp=user_otp) 
                                user_table_data1 = Table_data_info2.objects.filter(table_id=47, table_ref_id=l_data.table_ref_id)
                                user_otp_table_data1 = Table_data_info2.objects.filter(table_id=48, table_ref_id=l_data.table_ref_id)
                                user_table_data = DynamicTableData(user_table_data1) 
                                user_otp_table_data = DynamicTableData(user_otp_table_data1) 
                                return user_table_data, user_otp_table_data, True, "Data Fetch Successfully" 
                            
                    else:    
                        userPassDetailEmail = Table_data_info2(table_id=48, table_col_id=1, user_id=l_data.user_id, column_data=data['email_or_username_or_phone_number'], table_ref_id=l_data.table_ref_id, col_data_type="String", column_name='user_email') 
                        userPassDetailEmail.save()
                        userPassDetailOtp = Table_data_info2(table_id=48, table_col_id=2, user_id=l_data.user_id, column_data=user_otp, table_ref_id=l_data.table_ref_id, col_data_type="String", column_name='user_otp') 
                        userPassDetailOtp.save()
                        userPassDetailToken = Table_data_info2(table_id=48, table_col_id=3, user_id=l_data.user_id, column_data='tokenabc', table_ref_id=l_data.table_ref_id, col_data_type="String", column_name='user_token') 
                        userPassDetailToken.save()
                        userPassDetailCTS = Table_data_info2(table_id=48, table_col_id=4, user_id=l_data.user_id, column_data=cts, table_ref_id=l_data.table_ref_id, col_data_type="DateTimeField", column_name='timestamp') 
                        userPassDetailCTS.save()

                        user_table_data1 = Table_data_info2.objects.filter(table_id=47, table_ref_id=l_data.table_ref_id)
                        user_otp_table_data1 = Table_data_info2.objects.filter(table_id=48, table_ref_id=l_data.table_ref_id)
                        user_table_data = DynamicTableData(user_table_data1) 
                        user_otp_table_data = DynamicTableData(user_otp_table_data1) 
                        return user_table_data, user_otp_table_data, True, "Data Fetch Successfully" 
          
                       
                else:
                    # return UserSignIn(result=False, otp="")
                    return [], [], False, "Your account doesn't active and email verified.Please email verified."
            else:
                return [], [], False, "Your account doesn't active and email verified.Please email verified."
        else:
            return [], [], False, "Email or Password don't match. Please try again valid email and password."
    except Exception as error:
        return [], [], False, f"Something errors or {error}"



def UserLoginFunction(data):
    try:
        email_exist_check1 = Table_data_info2.objects.filter(table_id=47, table_col_id=1, column_data=data['email_or_username_or_phone_number'])
        if email_exist_check1.count()==1:
            email_exist_check = Table_data_info2.objects.get(table_id=47, table_col_id=1, column_data=data['email_or_username_or_phone_number'])
            password_detail = Table_data_info2.objects.get(table_id=47, table_ref_id=email_exist_check.table_ref_id, column_data=data['password'], user_id=email_exist_check.user_id, column_name='password')
            user_data, otp_data, result, message = LoginCheck(data, email_exist_check, password_detail)
            return user_data, otp_data, result, message
        username_exist_check1 = Table_data_info2.objects.filter(table_id=47, table_col_id=2, column_data=data['email_or_username_or_phone_number'])
        if username_exist_check1.count()==1:
            username_exist_check = Table_data_info2.objects.get(table_id=47, table_col_id=2, column_data=data['email_or_username_or_phone_number'])
            password_detail = Table_data_info2.objects.get(table_id=47, table_ref_id=username_exist_check.table_ref_id, column_data=data['password'], user_id=username_exist_check.user_id, column_name='password')
            user_data, otp_data, result, message = LoginCheck(data, email_exist_check, password_detail)
            return user_data, otp_data, result, message
        
        phone_exist_check1 = Table_data_info2.objects.filter(table_id=47, table_col_id=3, column_data=data['email_or_username_or_phone_number'])
        if phone_exist_check1.count()==1:
            phone_exist_check = Table_data_info2.objects.get(table_id=47, table_col_id=3, column_data=data['email_or_username_or_phone_number'])
            password_detail = Table_data_info2.objects.get(table_id=47, table_ref_id=phone_exist_check.table_ref_id, column_data=data['password'], user_id=phone_exist_check.user_id, column_name='password')
            user_data, otp_data, result, message = LoginCheck(data, email_exist_check, password_detail)
            return user_data, otp_data, result, message
        
        return [], [], False, "Email or Password don't match. Please try again valid email and password."
    except Exception as error:
        return [], [],False, f"Something errors or Email or Password don't match or {error}"
    

def UserOTPCheckFunction(data):
    try:
        user_email_otp = Table_data_info2.objects.get(table_id=48, table_col_id=1, column_data=data['email_or_username_or_phone_number'])
        user_otp_check = Table_data_info2.objects.get(table_id=48, table_col_id=2, table_ref_id=user_email_otp.table_ref_id, column_data=data['user_otp'], user_id=user_email_otp.user_id)
        if user_email_otp.table_ref_id==user_otp_check.table_ref_id and user_email_otp.user_id==user_otp_check.user_id and user_otp_check.column_data==data['user_otp']:
            email_detail = Table_data_info2.objects.get(table_id=47, column_data=data['email_or_username_or_phone_number'])
            login = Table_data_info2.objects.filter(table_id=47, table_ref_id=email_detail.table_ref_id, user_id=email_detail.user_id)
            # print("login", login)
            login_data = {}
            for m in login:
                # print("m", m.column_name, m.column_data)
                if m.column_name == 'user_id':
                    login_data['pk'] = m.pk
                    login_data[m.column_name] = m.column_data
                login_data[m.column_name] = m.column_data

            token = JWTTokenGenerator.generate_token(login_data)
            user_token_update = Table_data_info2.objects.get(table_id=48, table_col_id=3, column_name='user_token', user_id=email_detail.user_id)
            user_token_update.column_data=token
            user_token_update.save()
            login_data['token']=token
            return login_data, True, 'Login Successfully Done.'
        else:
            return [], False, 'Please Valid Email and OTP.'
    except Exception as error:
        return [], False, f"Something errors or Please Valid Email and OTP or {error}"



def TableColInfoCreateFunction(data):
    try:
        if data['db'] == 1:
            fileName = main_media_url+f'/media/upload_file/user_data/table_col_info.json'
            TableInfoDtlfileName = main_media_url+f'/media/upload_file/user_data/table_info_dtl.json'
            ChangeLogFunction(folder_path=f'/media/upload_file/user_data/table_col_info.json', api_url=main_url+f'/media/upload_file/user_data/table_col_info.json')
            ChangeLogFunction(folder_path=f'/media/upload_file/user_data/table_info_dtl.json', api_url=main_url+f'/media/upload_file/user_data/table_info_dtl.json')

            if os.path.isfile(fileName) and os.path.isfile(TableInfoDtlfileName):
                f = open(TableInfoDtlfileName)
                json_data = json.load(f)
                table_info_dtl_data = json_data['table_info_dtl']
            
                table_data_filter = [x for x in table_info_dtl_data if x['table_name'] == data['table_name'] and x['user_id'] == data['user_id']]

                for key, value in data['items'].items():

                    f1= open(fileName)
                    json_data1 = json.load(f1)
                    table_col_info_data1 = json_data1['table_col_info']
                    if any(
                        x['table_id'] == table_data_filter[0]['table_id']
                        and x['table_col_id'] == key
                        and x['column_name'] == value
                        and x['user_id'] == data['user_id']
                        for x in table_col_info_data1
                    ):
                        return False, 'Table column name already exists.'

                    new_data = {
                        "id": len(table_col_info_data1)+1,
                        "table_id": table_data_filter[0]['table_id'],
                        "table_col_id": key,
                        "column_name": value,
                        "col_desc": value,
                        "col_data_type": "char",
                        "col_classi": "internal",
                        "col_visible": "True",
                        "user_id": data['user_id'],
                    }
                    write_json(new_data, fileName, "table_col_info")
                return True, "Json Table Column Created Successfully."
            return False, "Something Wrong!"
        
        if data['db'] == 2:
            fileName = main_media_url+f'/media/upload_file/user_data/table_col_info2.json'
            TableInfoDtlfileName = main_media_url+f'/media/upload_file/user_data/table_info_dtl2.json'
            ChangeLogFunction(folder_path=f'/media/upload_file/user_data/table_col_info2.json', api_url=main_url+f'/media/upload_file/user_data/table_col_info2.json')
            ChangeLogFunction(folder_path=f'/media/upload_file/user_data/table_info_dtl2.json', api_url=main_url+f'/media/upload_file/user_data/table_info_dtl2.json')

            if os.path.isfile(fileName) and os.path.isfile(TableInfoDtlfileName):
                f = open(TableInfoDtlfileName)
                json_data = json.load(f)
                table_info_dtl_data = json_data['table_info_dtl2']
            
                table_data_filter = [x for x in table_info_dtl_data if x['table_name'] == data['table_name'] and x['user_id'] == data['user_id']]

                for key, value in data['items'].items():

                    f1= open(fileName)
                    json_data1 = json.load(f1)
                    table_col_info_data1 = json_data1['table_col_info2']

                    if any(
                        x['table_id'] == table_data_filter[0]['table_id']
                        and x['table_col_id'] == key
                        and x['column_name'] == value
                        and x['user_id'] == data['user_id']
                        for x in table_col_info_data1
                    ):
                        return False, 'Table column name already exists.'

                    new_data = {
                        "id": len(table_col_info_data1)+1,
                        "table_id": table_data_filter[0]['table_id'],
                        "table_col_id": key,
                        "column_name": value,
                        "col_desc": value,
                        "col_data_type": "char",
                        "col_classi": "internal",
                        "col_visible": "True",
                        "user_id": data['user_id'],
                    }
                    write_json(new_data, fileName, "table_col_info2")
                return True, "Json Table Column Created Successfully."
            return False, "Something Wrong!"
        
    except Exception as error:
        # return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  
        return False, f'Something errors or {error}'

def TableInfoDtlCreateFunction(data):
    try:
        if data['db'] == 1:
            fileName = main_media_url+f'/media/upload_file/user_data/table_info_dtl.json'
            ChangeLogFunction(folder_path=f'/media/upload_file/user_data/table_info_dtl.json', api_url=main_url+f'/media/upload_file/user_data/table_info_dtl.json')

            if os.path.isfile(fileName):
                f = open(fileName)
                json_data = json.load(f)
                table_info_dtl_data = json_data['table_info_dtl']
                if any(
                    x['table_name'] == data['table_name']
                    and x['user_id'] == data['user_id']
                    for x in table_info_dtl_data
                ):
                    return False,  f'Table Name already existed.'
                # if [x for x in table_info_dtl_data if x['table_name'] == data['table_name'] ]:
                #     return False, f'Table Name already existed.'

                new_data = {
                    "table_id": len(table_info_dtl_data)+1,
                    "table_name": data['table_name'],
                    "table_description": data['table_description'],
                    "table_type": data['table_type'],
                    "user_id": data['user_id'],
                }

                write_json(new_data, fileName, "table_info_dtl")
                return True, f'Json Table Created Successfully.'
            return False, f'Something Wrong.'
        
        if data['db'] == 2:
            fileName = main_media_url+f'/media/upload_file/user_data/table_info_dtl2.json'
            ChangeLogFunction(folder_path=f'/media/upload_file/user_data/table_info_dtl2.json', api_url=main_url+f'/media/upload_file/user_data/table_info_dtl2.json')

            if os.path.isfile(fileName):
                f = open(fileName)
                json_data = json.load(f)
                table_info_dtl_data = json_data['table_info_dtl2']
                if any(
                    x['table_name'] == data['table_name']
                    and x['user_id'] == data['user_id']
                    for x in table_info_dtl_data
                ):
                    return False,  f'Table Name already existed.'
                # if [x for x in table_info_dtl_data if x['table_name'] == data['table_name']]:
                #     return False, f'Table Name already existed.'

                new_data = {
                    "table_id": len(table_info_dtl_data)+1,
                    "table_name": data['table_name'],
                    "table_description": data['table_description'],
                    "table_type": data['table_type'],
                    "user_id": data['user_id'],
                }

                write_json(new_data, fileName, "table_info_dtl2")
                return True, f'Json Table Created Successfully.'
            return False, f'Something Wrong.'
        

    except Exception as error:
        # return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  
        return False, f'Something errors or {error}'

def PageDeleteAPIFunction(table_id, table_col_id, page_name):
    try:
        page_data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id, column_data=page_name)
        # print("page_data", page_data)
        if len(page_data) != 0:
            for ap in page_data:
                # print("columname columndata", ap.column_name, ap.column_data)
                try:
                    page = Table_data_info.objects.filter(table_id=642, table_col_id=5, column_data=ap.column_data)
                    for p in page:
                        page_dk = Table_data_info.objects.filter(table_id=642, table_ref_id=p.table_ref_id)
                        if len(page_dk)!=0:
                            for pdk in page_dk:
                                pdk.delete()
                except:
                    print("except")
                else:
                    page_d = Table_data_info.objects.filter(table_id=table_id, table_ref_id=ap.table_ref_id)   
                    if len(page_d)!=0:
                        for pd in page_d:
                            pd.delete()
            return True 
        return False               
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def PageDataClearAPIFunction(table_id, table_col_id):
    try:
        sections = {}
        items = []
        refId = []

        page_data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id)
        # print("page_data", page_data)
        for ap in page_data:
            # print("columname columndata", ap.column_name, ap.column_data)
            if ap.column_data.lower() == "true":
                data_update = Table_data_info.objects.get(table_data_id=ap.table_data_id)
                data_update.column_data = "false"
                data_update.save()
        return True 
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  


def PageWiseDataShowAPIFunction(page_name):
    try:
        sections = {}
        items = []
        refId = []

        page_data = Table_data_info.objects.filter(table_id=642, column_data=page_name)[0]
        all_page = Table_data_info.objects.filter(table_ref_id=page_data.table_ref_id)
        # print("all_page", all_page)
        for ap in all_page:
            # print("columname columndata", ap.column_name, ap.column_data)
            if ap.column_name == 'card_id':
                card_data = Table_data_info.objects.get(table_id=534, column_data=ap.column_data)
                card_data_filter = Table_data_info.objects.filter(table_ref_id=card_data.table_ref_id)
                # print("card_data_filter", card_data_filter)
                items = DynamicTableData(card_data_filter)
                # for k in card_data_filter:
                #     refId.append(k.table_ref_id)
                            
                # refId = list(set(refId))
                # for m in refId:
                #     for i in card_data_filter:
                #         if i.table_ref_id==m:
                #             sections[i.column_name]=i.column_data
                #             sections['table_ref_id']=i.table_ref_id
                #             sections['table_id']=i.table_id
                #             sections['id']=i.table_data_id
                #             sections['tab_rel_id']=i.tab_rel_id
                #             sections['user_id']=i.user_id
                #     if sections != "":
                #         items.append(sections)   
                #         sections = {}
                #         refId=[]
        return items
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  

def GETDYNAMICJSONTABLEDATAINFOPIFunction(table_id, user_id):
    try:
        items = []
        UserTableDatafileName = main_media_url+f'/media/upload_file/user_data/user_table_data.json'
        if os.path.isfile(UserTableDatafileName):
            f = open(UserTableDatafileName)
            json_data = json.load(f)
            # print("10175 json_data", json_data)
            # print("10176 json_data[str(user_id)][str(table_id)]", json_data[str(user_id)][str(table_id)])
            items = json_data[str(user_id)][str(table_id)]
        return items    
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

def UPDATEDYNAMICTABLEDATAINFOPIFunction(table_data):
    try:
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
        return True
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  



def GETDYNAMICTABLEDATAINFOPI2Function(table_id):
    try:
        sections = {}
        items = []
        refId = []
        api_name_value = Table_data_info2.objects.filter(table_id=table_id)
        items = DynamicTableData(api_name_value)
        return items
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  

def GETDYNAMICTABLEDATAINFOPIFunction(table_id):
    try:
        sections = {}
        items = []
        refId = []
        api_name_value = Table_data_info.objects.filter(table_id=table_id)
        items = DynamicTableData(api_name_value)
        return items
    except Exception as error:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {error}'}, status=status.HTTP_400_BAD_REQUEST)  

#two layer dynamic data insert json
def insert_data(data, key1, key2, new_entry):
    """
    Inserts new_entry into the nested dictionary structure.
    If data is empty, it initializes it with the provided key structure.
    """
    
    if not data:  # If data is empty, initialize with the given structure
        data[key1] = {key2: [new_entry]}
    else:
        try:
            data[key1][key2].append(new_entry)
        except:
            if key1 not in data:
                data[key1] = {}
            if key2 not in data[key1]:
                data[key1][key2] = []
            
            data[key1][key2].append(new_entry)
    
    return data

def FormBuilderDataSaveAPIFunction(form_data, type_data, dataSourceId, UserId):
    try:
        unique_table_ref_id = generate_unique_random_number()

        if type_data == 'Normal Type' and str(dataSourceId) == "1":
            f_data = Table_col_info.objects.filter(table_id=form_data['tableId'])
            for fd in f_data: 
                if fd.column_name in form_data.keys():
                    Table_data_info.objects.create(table_id=fd.table_id, table_col_id=fd.table_col_id, column_name=fd.column_name, column_data=form_data[fd.column_name], table_ref_id=unique_table_ref_id)
            
        if type_data == 'Normal Type' and str(dataSourceId) == "2":
            f_data = Table_col_info2.objects.filter(table_id=form_data['tableId'])
            for fd in f_data: 
                if fd.column_name in form_data.keys():
                    Table_data_info2.objects.create(table_id=fd.table_id, table_col_id=fd.table_col_id, column_name=fd.column_name, column_data=form_data[fd.column_name], table_ref_id=unique_table_ref_id)
            
        if type_data == 'Normal Type' and str(dataSourceId) == "json data":
            UserTableDatafileName = main_media_url+f'/media/upload_file/user_data/user_table_data.json'
            tableId = form_data['tableId']
            exclude_keys = {'tableId'}
            form_data_exlcude_table_id = {k: v for k, v in form_data.items() if k not in exclude_keys}
            if os.path.isfile(UserTableDatafileName):
                f = open(UserTableDatafileName)
                json_data = json.load(f)
                # print("json_data", json_data)
                updated_data = insert_data(json_data, UserId, str(tableId), form_data_exlcude_table_id)
                # print(json.dumps(updated_data, indent=4))
                def write_json(new_data, filename=UserTableDatafileName):
                    with open(filename, 'r+') as file:
                        json.dump(new_data, file, indent=4)
                write_json(updated_data)  
        return True              
    except Exception as error:
        return False


def ALLStartingPointAPIFunction(scalList, resultList):
    try:
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
        return DataList              
    except Exception as error:
        return []
    

def GETBalanceSimulationByNameAPIFunction(name, user_email):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/balance_simulation.json'
        f = open(fileName)
        data = json.load(f)
        array_data = data['data']
        compareData = [x for x in array_data if x['name'] == name and x['user_email'] == user_email ]
        return compareData              
    except Exception as error:
        return []
    
def GETBalanceSimulationAPIFunction():
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
        return Datalist              
    except Exception as error:
        return []


def BalanceSimulationJsonFunction(name, starting_point, starting_vlaue, left_side, right_side, all_starting_tabular_data, user_email):
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
                new_data = {
                    "user_email": user_email,
                    "name": name,
                    "starting_point": starting_point,
                    "starting_vlaue": starting_vlaue,
                    "left_side": left_side,
                    "right_side": right_side,
                    "all_starting_tabular_data": all_starting_tabular_data,
                    "time": curdatetime,
                }
                write_json(new_data, fileName, "data")
        return True
    except Exception as err:
        return False


def SendInboundMessageFunction(message_id, email, subject, message):
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
        return True

    except Exception as err:
        return False

def SendOutboundMessageFunction(message_id, email, message):
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
                                
        return True
    except Exception as err:
        return False
    

def UpdateMessageAPIFunction(message_id):
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
                                
        return True
    except Exception as err:
        return False
    
def GetMessageAPIFunction(email):
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
        return unread_data
    except Exception as err:
        return []

def SendMessageFunction(email, subject, message):
    try:
        fileName = main_media_url+f'/media/upload_file/investing/json/message.json'
        # ChangeLogFunction(folder_path=f'/media/upload_file/investing/json/message.json', api_url=main_url+f'/media/upload_file/investing/json/message.json')
        curdate, curdatestamp, curdatetime, curdatetimestamp, curdate5, curtimestamp5, curdate_5, curtimestamp_5 = dtm()
        if os.path.isfile(fileName):
           
            new_data = {
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
            write_json(new_data, fileName, "data")
        return True
    except Exception as err:
        return False
    
def GETDAPIFunction():
    try:
        api_name_value = Table_data_info.objects.filter(table_id=1)
        items = DynamicTableData(api_name_value)
        return items
    except Exception as err:
        return []
    

def ThreePointerD3MinpCalculationAPIFunction(starting_point, starting_value, daygap, first_run, value_range_list2, input_p, d1_point0, d1_point1, d2_point2):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'
        if os.path.isfile(fileNameRule):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            dfList = []
            SumList=[]
            count=0

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
            return minp_data
        return []
    except Exception as err:
        return []
    
def MainPointerCalculationAPIFunction(starting_point, starting_value, daygap, value_range_list2):
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
            file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file2.xlsx'
            empty_df = pd.DataFrame()
            empty_df.to_excel(file_name1, index=False)

            main_data, summary_data, summary_data2,  range_point = MainPointerCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, SumList, daygap)
            return main_data, summary_data, summary_data2,  range_point
        return [], [], [], []
    except Exception as err:
        return [], [], [], []
    
def ThreePointerD3CalculationAPIFunction(starting_point, starting_value, daygap, first_run, value_range_list2, input_p, d1_point0, d1_point1, d2_point2, minp_value):
    try:
        fileNameRule = main_media_url+f'/media/upload_file/investing/json/rule.json'
        if os.path.isfile(fileNameRule):
            fr = open(fileNameRule)
            rule_data = json.load(fr)
            dfList = []
            SumList=[]
            count=0

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

            summary_data= PointerCalculationd3(starting_point, starting_value, rule_data, value_range_list2, dfList, count, SumList, daygap, first_run, input_p, d1_point0,  d1_point1, d2_point2, minp_value)
            return summary_data
        return []
    except Exception as err:
        return []
