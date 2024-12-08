
import json
import os
import pandas as pd
import time
from datetime import datetime, timedelta
import schedule
import requests

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response

#import model
from courseapp.models import *


def IsNotNullFunctionRuleValidate(table_name, column_name, operator, value):
    try:
        table_info = Table_info_dtl.objects.get(table_name=table_name)
        table_id = table_info.table_id
        table_col = Table_col_info.objects.get(table_id=table_id, column_name=column_name)
        table_col_id = table_col.table_col_id
        table_data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id)
        for i in table_data:
            if i.column_data == "":
                return False
         
        return True
                        

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)  




def IsUniqueFunctionRuleValidate(table_name, column_name, operator, value):
    try:
        table_info = Table_info_dtl.objects.get(table_name=table_name)
        table_id = table_info.table_id
        table_col = Table_col_info.objects.get(table_id=table_id, column_name=column_name)
        table_col_id = table_col.table_col_id
        table_data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id)
        listItem = []
        for i in table_data:
            listItem.append(i.column_data)
           
        if len(listItem) != len(set(listItem)):
            return False
        else:
            return True
                        

    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)  
    

def IsNotNullFunctionValueValidate(table_name, column_name, column_value, operator, value):
    try:
        if column_value == "" or column_value == " ":
                return False
        else: 
            return True
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)  


def IsUniqueFunctionValueValidate(table_name, column_name, column_value, operator, value):
    try:
        table_info = Table_info_dtl.objects.get(table_name=table_name)
        table_id = table_info.table_id
        table_col = Table_col_info.objects.get(table_id=table_id, column_name=column_name)
        table_col_id = table_col.table_col_id
        table_data = Table_data_info.objects.filter(table_id=table_id, table_col_id=table_col_id)
        for i in table_data:
            if i.column_data == column_value:
                return False
       
        return True
    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)  
    

def ContainsFunctionValueValidate(table_name, column_name, column_value, operator, value):
    try:

        if column_value !="" and column_value.find(value) != -1:
            return True
        else:
            return False
    
    except Exception as err:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)  
    

