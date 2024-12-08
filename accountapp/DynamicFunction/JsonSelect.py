
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
import requests

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response

#import model
from courseapp.models import *



# for model json  query start

# model OperatorCheck def

def OperatorCheck(op):
    op_list = ['==', '!=', '>', '<', '>=', '<=', '=', 'and', 'or', 'not', 'is', '&&']
    for i in range(len(op_list)):
        if i<len(op_list):
            if op_list[i]==op:
                return True
        else:
            return False    

# model validate def
def Validate(data, sl, list_name):
    validate_data = data.split(".")
    try:
        if len(validate_data)==2:
            T_Validate = Table_info_dtl.objects.get(table_name=validate_data[0])
            Table_col_info.objects.get(table_id=T_Validate.table_id, column_name=validate_data[1])
        else:
           Table_info_dtl.objects.get(table_name=validate_data[0])    
        return True
    except Exception as err:
        op_result = OperatorCheck(validate_data[0])
        if op_result is not True:
            if list_name == 'clist' and sl == 2:
                return True
            else:
                return False
        else:
            return True 
        
        
#ColumnList
def ColumnListModelFunction(query_list, select_list, from_list, TableList):
    try:
        # column information
        TableName=[]
        ColumnName = []
        TableId = []
        TableColId = []

        for p in range(select_list, from_list, 1):
            TableColumn = query_list[p].split('.')
            if len(TableColumn) == 1:
                for t in range(len(TableList)):
                    TableData = Table_info_dtl.objects.get(table_name=TableList[t])
                    for tc in range(len(TableColumn)): 
                        TableColumnData = Table_col_info.objects.filter(table_id=TableData.table_id).filter(column_name=TableColumn[tc].replace(',', '')) 
                        for tcolumn in TableColumnData:
                            if TableColumn[tc].replace(',', '') == tcolumn.column_name:
                                TableName.append(TableData.table_name)
                                TableId.append(tcolumn.table_id)
                                ColumnName.append(tcolumn.column_name)
                                TableColId.append(tcolumn.table_col_id)
                                
            if len(TableColumn) == 2:
                for tc in range(len(TableColumn)): 
                    if tc == 0:
                        TableName.append(TableColumn[tc])
                        TableData = Table_info_dtl.objects.get(table_name=TableColumn[tc])
                        TableId.append(TableData.table_id)
                    if tc == 1:    
                        ColumnName.append(TableColumn[tc].replace(',', ''))
                        TableColumnData = Table_col_info.objects.filter(table_id=TableData.table_id).filter(column_name=TableColumn[tc].replace(',', '')) 
                        for tcolumn in TableColumnData:
                            if TableColumn[tc].replace(',', '') == tcolumn.column_name:
                                TableColId.append(tcolumn.table_col_id)
   
        return TableName, TableId, ColumnName, TableColId   
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)



# Model Joining Data
def ModelJoiningData(T1, C1, T2, C2):
    try:
        T1_Data = Table_data_info.objects.filter(table_id=T1).filter(table_col_id=C1)
        T2_Data = Table_data_info.objects.filter(table_id=T2).filter(table_col_id=C2)


        t2Data = []
        for tdata in T2_Data:
            t2Data.append(tdata.column_data)
        j1data = T1_Data.filter(column_data__in=t2Data)

        t1Data = []
        for tdata in T1_Data:
            t1Data.append(tdata.column_data)
        j2data = T2_Data.filter(column_data__in=t1Data)
        jlist = []
        for j1 in j1data:
            t1 = Table_data_info.objects.filter(table_id=j1.table_id).filter(table_ref_id=j1.table_ref_id)
            jlist.append(t1)
        
        for j2 in j2data:
            t2 = Table_data_info.objects.filter(table_id=j2.table_id).filter(table_ref_id=j2.table_ref_id)
            jlist.append(t2)

        return jlist
    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


# Model Condition Data
def ModelConditionData(jdata, T1, C1, O, V):
    try:
        cdata = []
        section={}
        for m in range(len(jdata)):
            T1_Data = jdata[m].filter(table_id=T1).filter(table_col_id=C1)
            if len(T1_Data) != 0:
                if O == '>':
                    t1filterData = T1_Data.filter(table_col_id__gt=V)
                    for i in t1filterData:
                        t1 = Table_data_info.objects.filter(table_id=i.table_id).filter(table_ref_id=i.table_ref_id)
                        cdata.append(t1)
                if O == '>=':
                    t1filterData = T1_Data.filter(table_col_id__gte=V)
                    for i in t1filterData:
                        t1 = Table_data_info.objects.filter(table_id=i.table_id).filter(table_ref_id=i.table_ref_id)
                        cdata.append(t1)
                if O == '<':
                    t1filterData = T1_Data.filter(table_col_id__lt=V)
                    for i in t1filterData:
                        t1 = Table_data_info.objects.filter(table_id=i.table_id).filter(table_ref_id=i.table_ref_id)
                        cdata.append(t1)   
                if O == '<=':
                    t1filterData = T1_Data.filter(table_col_id__lt=V)
                    for i in t1filterData:
                        t1 = Table_data_info.objects.filter(table_id=i.table_id).filter(table_ref_id=i.table_ref_id)
                        cdata.append(t1)   
                if O == '==':
                    t1filterData = T1_Data.filter(column_data=V)
                    for i in t1filterData:
                        t1 = Table_data_info.objects.filter(table_id=i.table_id).filter(table_ref_id=i.table_ref_id)
                        cdata.append(t1)  
                       
        return cdata 
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


# Model OrderBy

def OrderByData(v_cdata, orderby):
    try:
        item=[]
        for m in range(len(v_cdata)):
            item.append(v_cdata[m].order_by(orderby)) 
        return item
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


#Model ColumnList
def SelectData(cdata, df):
    try:
        Select_Item = []

        for index, row in df.iterrows():
            for m in range(len(cdata)):
                item = cdata[m].filter(table_id=row['TableId']).filter(table_col_id=row['TableColId'])
                if len(item) != 0:
                    Select_Item.append(item)
                
        return Select_Item
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


#Model ColumnList
def SelectColumnData(TableId, TableColId):
    try:
        Select_Item = []

        item = Table_data_info.objects.filter(table_id=TableId).filter(table_col_id=TableColId)
        for i in item:
            t1 = Table_data_info.objects.filter(table_id=i.table_id).filter(table_ref_id=i.table_ref_id)
            Select_Item.append(t1) 
       
                
        return Select_Item
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)




# json convert
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
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)



#ModelSelectQueryFunction start
def ModelSelectQueryFunction(ColumnName, df, df1, orderby):
    try:
        
        joinDataFrame = pd.DataFrame()
        sections={}
        items = []
        refId = []
        jdata = []
        cdata = []
        c_data = []
        section={}
        cdf = pd.DataFrame()
        orderdata = []
        sData = []
        count = 0

        if len(ColumnName)!=0 and len(df)!=0 and len(df1)!=0 and len(orderby)!=0: 
            for index, row in df1.iterrows(): 
                if pd.isna(row['T1'])==False and pd.isna(row['C1'])==False and pd.isna((row['T2']))==False and pd.isna((row['C2']))==False:
                    try:
                        jdata1 = ModelJoiningData(int(row['T1']),int(row['C1']), int(row['T2']), int(row['C2']))
                        for m in range(len(jdata1)):
                            jdata.append(jdata1[m])
                    except Exception as err:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)    
              
                if pd.isna(row['T1'])==False and pd.isna(row['C1'])==False and pd.isna((row['O']))==False and pd.isna((row['V']))==False and len(jdata)!=0 and len(cdata)==0:
                    try:
                        cdata1 = ModelConditionData(jdata, row['T1'], row['C1'], row['O'], row['V'])
                        for m in range(len(cdata1)):
                            cdata.append(cdata1[m])

                    except Exception as err:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)
                
                if pd.isna(row['T1'])==False and pd.isna(row['C1'])==False and pd.isna((row['O']))==False and pd.isna((row['V']))==False and len(cdata)!=0:
                    try:
                        cdata1 = ModelConditionData(cdata, row['T1'], row['C1'], row['O'], row['V'])
                        cdata = [] 
                        for m in range(len(cdata1)):
                            cdata.append(cdata1[m])
                       
                    except Exception as err:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)
            

            
            for j in range(len(cdata)):
                for m in range(len(cdata[j])):
                    section[cdata[j][m].column_name]= cdata[j][m].column_data
                if len(section)!=0:      
                    c_data.append(section) 
                    section={}
            cdf = cdf.append(c_data)   
            source = cdf.sort_values(by=orderby[0], ascending=False)
          
            try:
                result_df = source[ColumnName]
                if len(result_df)!=0:
                    result_df = result_df.fillna(0) 
                    # return result_df.to_csv(index=False)
                    data = JsonConvertData(result_df)
                    return data
            except Exception as err:
                source = source.fillna(0) 
                # return source.to_csv(index=False)
                data = JsonConvertData(source)
                return data
               
           
        if len(ColumnName)!=0 and len(df)!=0 and len(df1)!=0 and len(orderby)==0: 
            for index, row in df1.iterrows(): 
                if pd.isna(row['T1'])==False and pd.isna(row['C1'])==False and pd.isna((row['T2']))==False and pd.isna((row['C2']))==False:
                    try:
                        jdata1 = ModelJoiningData(int(row['T1']),int(row['C1']), int(row['T2']), int(row['C2']))
                        for m in range(len(jdata1)):
                            jdata.append(jdata1[m])
                    except Exception as err:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)    
              
                if pd.isna(row['T1'])==False and pd.isna(row['C1'])==False and pd.isna((row['O']))==False and pd.isna((row['V']))==False and len(jdata)!=0 and len(cdata)==0:
                    try:
                        cdata1 = ModelConditionData(jdata, row['T1'], row['C1'], row['O'], row['V'])
                        for m in range(len(cdata1)):
                            cdata.append(cdata1[m])

                    except Exception as err:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)
                
                if pd.isna(row['T1'])==False and pd.isna(row['C1'])==False and pd.isna((row['O']))==False and pd.isna((row['V']))==False and len(cdata)!=0:
                    try:
                        cdata1 = ModelConditionData(cdata, row['T1'], row['C1'], row['O'], row['V'])
                        cdata = [] 
                        for m in range(len(cdata1)):
                            cdata.append(cdata1[m])
                       
                    except Exception as err:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            for j in range(len(cdata)):
                for m in range(len(cdata[j])):
                    section[cdata[j][m].column_name]= cdata[j][m].column_data
                if len(section)!=0:      
                    c_data.append(section) 
                    section={}
            cdf = cdf.append(c_data)  
            try:
                result_df = cdf[ColumnName]
                if len(result_df)!=0:
                    result_df = result_df.fillna(0)
                    data = JsonConvertData(result_df)
                    return data
            except Exception as err:
                cdf = cdf.fillna(0)
                data = JsonConvertData(cdf)
                return data

           
        if len(ColumnName)!=0 and len(df)!=0 and len(df1)==0 and len(orderby)!=0: 
            for index, row in df.iterrows(): 
                if pd.isna(row['TableId'])==False and pd.isna(row['TableColId'])==False:
                    try:
                        sdata = SelectColumnData(int(row['TableId']),int(row['TableColId']))
                        for m in range(len(sdata)):
                            sData.append(sdata[m])
                    except Exception as err:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)    
              
                
            for j in range(len(sData)):
                for m in range(len(sData[j])):
                    section[sData[j][m].column_name]= sData[j][m].column_data
                if len(section)!=0:      
                    c_data.append(section) 
                    section={}
            cdf = cdf.append(c_data)
            source = cdf.sort_values(by=orderby[0], ascending=False)
            try:
                result_df = source[ColumnName]
                if len(result_df)!=0:
                    result_df=result_df.fillna(0) 
                    result_df = result_df.drop_duplicates()
                    data = JsonConvertData(result_df)
                    return data
            except Exception as err:
                cdf = source.fillna(0) 
                source = source.drop_duplicates()
                data = JsonConvertData(cdf)
                return data
                
        
        if len(ColumnName)!=0 and len(df)!=0 and len(df1)==0 and len(orderby)==0: 
            for index, row in df.iterrows(): 
                if pd.isna(row['TableId'])==False and pd.isna(row['TableColId'])==False:
                    try:
                        sdata = SelectColumnData(int(row['TableId']),int(row['TableColId']))
                        for m in range(len(sdata)):
                            sData.append(sdata[m])
                    except Exception as err:
                        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)    
              
                
            for j in range(len(sData)):
                for m in range(len(sData[j])):
                    section[sData[j][m].column_name]= sData[j][m].column_data
                if len(section)!=0:      
                    c_data.append(section) 
                    section={}
            cdf = cdf.append(c_data)  
            
            
            try:
                result_df = cdf[ColumnName]
                if len(result_df)!=0:
                    result_df = result_df.fillna(0) 
                    result_df = result_df.drop_duplicates()
                    data = JsonConvertData(result_df)
                    return data
            except Exception as err:
                cdf = cdf.fillna(0)
                cdf = cdf.drop_duplicates()
                data = JsonConvertData(cdf)
                return data
                
        

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)


#ModelSelectQueryFunction end    


# for model json  query end