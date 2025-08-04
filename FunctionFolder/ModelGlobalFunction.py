import json
import os

# from transformers import pipeline

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.views import *

from courseapp.models import *


# from accountapp.DynamicFunction.Process_Log import ProcessLogFunction


# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import pandas as pd
# import numpy as np

import time
from datetime import datetime, date

import threading

gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
currenttimestamp = datetime.strptime(
                gm, "%a, %d %b %Y %X").timestamp()
currenttimedate = datetime.fromtimestamp(
                currenttimestamp).strftime('%d-%m-%Y %H:%M:%S')
                
                
from accountapp.DynamicFunction.LinkedList import *
from accountapp.DynamicFunction.JsonSelect import *                
from FunctionFolder.ModelGlobalFunction import *                
                
                
def CurrentTimeFunc():
    date_mili = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

    return date_mili


def ValueCountFunc(data):
    if type(data) is int:
        return 1
    if type(data) is str:
        return 1
    if type(data) is bool:
        return 1    
    if type(data) is list:
        return len(data)
    if type(data) is dict:
        return len(data)    
        
        
        
def HashKeyValidateFunc(hashKey):
    try:
        table_data = Table_data_info.objects.filter(table_id=587)
        if len(table_data) !=0:
            for m in table_data:
                if m.table_col_id == 1:
                    if m.column_data == hashKey:
                        return True
            return False
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
    
        
                
                
                
def APICALLFUNCTION(api_name, ip_address):
    try:
        fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/api_call_data.json'
        if os.path.isfile(fileName):
        
            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4, skipkeys=False)

            y = {
                "api_name": api_name,
                "user_id": "1",
                "date_time": currenttimedate,
                "ip_address": ip_address
                }

            p1 = threading.Thread(target=write_json,args=(y,))
            p1.start()
            p1.join()

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 
        

def APICALLLOGFUNCTION(api_name, ip_address):
    try:
        fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/api_call_log.json'
        if os.path.isfile(fileName):
        
            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4, skipkeys=False)

            y = {
                "api_name": api_name,
                "user_id": "1",
                "date_time": currenttimedate,
                "ip_address": ip_address
                }

            p1 = threading.Thread(target=write_json,args=(y,))
            p1.start()
            p1.join()

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)
        
        
def APICALLSTATUSFUNCTION(api_name, ip_address):
    try:
        fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/json/api_call_status.json'
        if os.path.isfile(fileName):
        
            def write_json(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4, skipkeys=False)

            y = {
                "api_name": api_name,
                "user_id": "1",
                "date_time": currenttimedate,
                "ip_address": ip_address
                }

            p1 = threading.Thread(target=write_json,args=(y,))
            p1.start()
            p1.join()

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
                    
            
        
    
                



# def Summarization(text):
#     summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
#     # print(summarizer(text, max_length=130, min_length=30, do_sample=False))
#     return summarizer(text, max_length=130, min_length=30, do_sample=False)
# # text = """
# # Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
# # Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
# # when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
# # It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. 
# # It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
# # and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

# # """
# # print(Summarization(text))

# def SearchNews(string):
#     try:
#         model_data = Table_data_info.objects.get(table_id=585)
#         string_list = []
#         for m in eval(model_data.column_data):
#             fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/news_json/{m}.json'
#             if os.path.isfile(fileName):
#                 f = open(fileName)
#                 data = json.load(f)
#                 array_data = data['data']
#                 for adata in array_data:
#                     string_list.append(adata['headline'])

#         tfidf_vectorizer = TfidfVectorizer(analyzer="char")

#         sparse_matrix = tfidf_vectorizer.fit_transform([string]+string_list)
#         cosine = cosine_similarity(sparse_matrix[0,:],sparse_matrix[1:,:])
#         pdg =pd.DataFrame({'cosine':cosine[0],'strings':string_list}).sort_values('cosine',ascending=False)
#         maxClm = pdg['cosine'].max()
#         SearchData = []
#         for index, row in pdg.iterrows():
#             if int(row['cosine']*100) >= int(maxClm*100):
#                 SearchData.append(row['strings'])  

#         return SearchData                

#     except Exception as err:
#         return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
    



def DataFetch_Static(title, name, value_count, loadtime):
    try:
        gm = time.strftime("%a, %d %b %Y %X",
                   time.gmtime())
        currenttimestamp = datetime.strptime(
                        gm, "%a, %d %b %Y %X").timestamp()
        currenttimedate = datetime.fromtimestamp(
                        currenttimestamp).strftime('%d-%m-%Y %H:%M:%S')

        currentdatetime = datetime.fromtimestamp(
                        currenttimestamp).strftime('%Y-%m-%d')
        
        fileName = main_media_url+f'/media/upload_file/json/datafetch_stat.json'
        if os.path.isfile(fileName):
        
            def write_json1(new_data, filename=fileName):
                with open(filename, 'r+') as file:
                    file_data = json.load(file)
                    file_data["data"].append(new_data)
                    file.seek(0)
                    json.dump(file_data, file, indent=4, skipkeys=False)

            y1 = {
                "title": title,
                "name": name,
                "value_count": value_count,
                "loadtime": loadtime,
                "date_time": currenttimedate
                }
            
            p1 = threading.Thread(target=write_json1,args=(y1,))
            p1.start()
            p1.join()


    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST)  
        
        
def CodeWriting(code, user, api_name, paramList):
    code_v = "    if user == "+ "'"+ user +"'" +" and api_name == "+ "'"+ api_name +"'"+" and "+" paramList"+":"
    code_v1 = "        a=''"
    code_v2 = "        b=''"
    code_v3 = "        for key, values in paramList.items():"
    code_v4 = "            if key == 'a':"
    code_v5 = "                a = values"
    code_v6 = "            if key == 'b':"
    code_v7 = "                b = values"
       
        
     

    fileName = f'/home/itbusaah/idriver_education_djangoproject/media/upload_file/dynamic_rest/Custom.py'
       
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
    
    
    
    

## Execute Sql start 



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

def Execute_sql(query):
    try:
        
        # table information
        TableList = []
        TableName=[]
        TableId = []
        # column information
        ColumnName = []
        TableColId = []

        ModelSelectQueryData = []
   

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
        
        
        print("ModelSelectQueryData", ModelSelectQueryData)
        return ModelSelectQueryData
        
            
       
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'Something errors or {err}'}, status=status.HTTP_400_BAD_REQUEST) 




## Execute Sql end    
