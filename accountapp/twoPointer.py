
from rest_framework.response import Response
from rest_framework import status

import json, os
from datetime import datetime, date, timedelta
from itertools import chain, combinations
import pandas as pd
import numpy as np
from time import gmtime, strftime
import uuid
import random
import time
from FunctionFolder.UserConfig import *
from accountapp.PointerValueCalculation import *




def generate_unique_random_number():
    # Get the current time in seconds since the Epoch
    current_time = int(time.time() * 1000)  # Multiply by 1000 to include milliseconds
    
    # Generate a random number
    random_number = random.randint(0, 99999)
    
    # Combine the current time with the random number to ensure uniqueness
    unique_random_number = int(f"{current_time}{random_number}")
    
    return unique_random_number




def combination(stuff):
    DataList=[]
    for i, combo in enumerate((combinations(stuff, 3)), 1):
        DataList.append(combo)
    return DataList   

def UniqueCombination(day1, day2):
    Datalist=[]
    for m in day1:
        for j in day2:
            Datalist.append((m,  j))
    return Datalist




def XAxisFunc(day, starting_point, starting_value, rule_data, daygap, value_range_list2):
   
    output_value = ""
    sum_value = 0.0
    diff_value_actual=0
    DataList = []
    DataListOutput = []
    Section = {}
  
    starting_point = starting_point
    x_starting_point_value = 0
    starting_point_loop = starting_point
    starting_value=starting_value
    starting_value1=starting_value


    sum_value = 0.0
    i=1

    if day == 1:
       
        
        # for diff_value in reversed(range(starting_point_loop-100, starting_point_loop, 5)):
        for diff_value in reversed(range(value_range_list2[1], starting_point_loop, 5)):
            diff_value_actual+=diff_value
            starting_point=diff_value
            Section['starting_point']=starting_point
            if i==1: 
                output_value= starting_value+rule_data['x01']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5  
            if i==2: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value  
                x_starting_point_value-=5  
            if i==3: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value  
                x_starting_point_value-=5    
            if i==4: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5     
            if i==5: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5 
            if i==6: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']+rule_data['x56']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==7: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']+rule_data['x56']+rule_data['x67']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==8: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']+rule_data['x56']+rule_data['x67']+rule_data['x78']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==9: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']+rule_data['x56']+rule_data['x67']+rule_data['x78']+rule_data['x89']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5       
            if i>9: 
                output_value= output_value1+5
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5    
            
        
            Section['starting_point_value']=x_starting_point_value
            Section['starting_value']=starting_value
            Section['output_value']=output_value  
            Section['sum_value']=sum_value 
            if len(Section) !=0:
                DataList.append(Section)  
                Section={}  
                output_value1=starting_value1
                i+=1 
                DataListOutput.append(starting_point)

    if day == 2:
        starting_value=starting_value+starting_value*daygap
        
        # for diff_value in reversed(range(starting_point_loop-100, starting_point_loop, 5)):
        for diff_value in reversed(range(value_range_list2[1], starting_point_loop, 5)):
            diff_value_actual+=diff_value
            starting_point=diff_value
            Section['starting_point']=starting_point
            if i==1: 
                output_value= starting_value+rule_data['x01']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5  
            if i==2: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value  
                x_starting_point_value-=5  
            if i==3: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value  
                x_starting_point_value-=5    
            if i==4: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5     
            if i==5: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==6: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']+rule_data['x56']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==7: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']+rule_data['x56']+rule_data['x67']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==8: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']+rule_data['x56']+rule_data['x67']+rule_data['x78']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==9: 
                output_value= starting_value+rule_data['x01']+rule_data['x12']+rule_data['x23']+rule_data['x34']+rule_data['x45']+rule_data['x56']+rule_data['x67']+rule_data['x78']+rule_data['x89']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i>9: 
                output_value= output_value1+5
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5    
            
        
            Section['starting_point_value']=x_starting_point_value
            Section['starting_value']=starting_value
            Section['output_value']=output_value  
            Section['sum_value']=sum_value 
            if len(Section) !=0:
                DataList.append(Section)  
                Section={}  
                output_value1=starting_value1
                i+=1  
                DataListOutput.append(starting_point)

    return DataList, DataListOutput


def YAxisFunc(day, starting_point, starting_value, rule_data, daygap, value_range_list2):

    output_value = ""
    diff_value_actual=0
    YDataList = []
    YDataListOutput = []
    YSection = {}

    starting_point = starting_point
    y_starting_point_value = 0
    starting_point_loop = starting_point
    starting_value=starting_value
    starting_value1=starting_value
    

    y_sum_value = 0.0
    yi=0
    if day == 1:

        # for diff_value in range(starting_point_loop, starting_point_loop+100, 5):
        for diff_value in range(starting_point_loop, value_range_list2[0]+5, 5):
            diff_value_actual+=diff_value
            starting_point=diff_value
            YSection['starting_point']=starting_point

            if yi==0: 
                output_value= starting_value
                y_sum_value=0  
                y_starting_point_value=0
        
            if yi==1: 
                output_value= starting_value-rule_data['y01']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value
                y_starting_point_value+=5 
            if yi==2: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5  
            if yi==3: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5     
            if yi==4: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value   
                y_starting_point_value+=5   
            if yi==5: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==6: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']-rule_data['y56']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==7: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']-rule_data['y56']-rule_data['y67']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==8: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']-rule_data['y56']-rule_data['y67']-rule_data['y78']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==9: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']-rule_data['y56']-rule_data['y67']-rule_data['y89']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi>9: 
                output_value= output_value1-5
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value  
                y_starting_point_value+=5   

            YSection['starting_point_value']=y_starting_point_value
            YSection['starting_value']=starting_value
            if output_value <=-1:
                YSection['output_value']=0 
            else:     
                YSection['output_value']=output_value
            YSection['sum_value']=y_sum_value 
            if len(YSection) !=0:
                YDataList.append(YSection)  
                YSection={}  
                output_value1=starting_value1
                yi+=1  
                YDataListOutput.append(starting_point) 

    if day == 2:
        starting_value=starting_value+starting_value*daygap

        # for diff_value in range(starting_point_loop, starting_point_loop+100, 5):
        for diff_value in range(starting_point_loop, value_range_list2[0]+5, 5):
            diff_value_actual+=diff_value
            starting_point=diff_value
            YSection['starting_point']=starting_point
        
            if yi==0: 
                output_value= starting_value
                y_sum_value=0  
                y_starting_point_value=0

            if yi==1: 
                output_value= starting_value-rule_data['y01']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value
                y_starting_point_value+=5 
            if yi==2: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5  
            if yi==3: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5     
            if yi==4: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value   
                y_starting_point_value+=5   
            if yi==5: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5  
            if yi==6: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']-rule_data['y56']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==7: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']-rule_data['y56']-rule_data['y67']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==8: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']-rule_data['y56']-rule_data['y67']-rule_data['y78']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==9: 
                output_value= starting_value-rule_data['y01']-rule_data['y12']-rule_data['y23']-rule_data['y34']-rule_data['y45']-rule_data['y56']-rule_data['y67']-rule_data['y89']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5      
            if yi>9: 
                output_value= output_value1-5
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value  
                y_starting_point_value+=5   

            YSection['starting_point_value']=y_starting_point_value
            YSection['starting_value']=starting_value
            if output_value <=-1:
                YSection['output_value']=0 
            else:     
                YSection['output_value']=output_value  
            YSection['sum_value']=y_sum_value 
            if len(YSection) !=0:
                YDataList.append(YSection)  
                YSection={}  
                output_value1=starting_value1
                yi+=1 
                YDataListOutput.append(starting_point)  


    return YDataList, YDataListOutput

def write_json(fileName, XDataList1, XDataList2, YDataList1, YDataList2):
    with open(fileName, 'r+') as file:
            file_data = json.load(file)
            file_data.update({
                "day1":{'x':XDataList1, 'y':YDataList1},
                "day2":{'x':XDataList2, 'y':YDataList1},
            })
            file.seek(0)
            json.dump(file_data, file, indent=4)

def write_json1(fileName, setup_value):
    with open(fileName, 'r+') as file:
            file_data = json.load(file)
            file_data.update({
                "setup_value": setup_value
            })
            file.seek(0)
            json.dump(file_data, file, indent=4)



def CombinationValue(value0, value1, DataListXY1, DataListXY2):
    dfList=[]
    new_row={}

    data_day1 = [x for x in DataListXY1 if x['starting_point'] == value0]
    # x_data_day1 = [x for x in DataListXY1 if x['starting_point'] == value0]
    # y_data_day1 = [x for x in YDataList1 if x['starting_point'] == value0]

    data1=0
    data2=0

    if len(data_day1)!=0:
        data1=round(data_day1[0]['output_value'], 2)
    # if len(x_data_day1)!=0:
    #     data1=round(x_data_day1[0]['output_value'], 2)
    # if len(y_data_day1)!=0:
    #     data1=round(y_data_day1[0]['output_value'], 2)

       
    data_day2 = [x for x in DataListXY2 if x['starting_point'] == value1]
    # x_data_day2 = [x for x in DataListXY2 if x['starting_point'] == value1]
    # y_data_day2 = [x for x in YDataList2 if x['starting_point'] == value1]
               
               
    if len(data_day2)!=0:
        data2=round(data_day2[0]['output_value'], 2)
    # if len(x_data_day2)!=0:
    #     data2=round(x_data_day2[0]['output_value'], 2)
    # if len(y_data_day2)!=0:
    #     data2=round(y_data_day2[0]['output_value'], 2)


    new_row={
        "data1":data1, 
        "data2":data2
    }
    if len(new_row)!=0:
        dfList.append(new_row)
        new_row={}
    return dfList


def ExcelFileWrite(file_name, df):
    df_data = pd.read_excel(file_name)
    df_data = pd.concat([df_data, df], ignore_index=True)
    df_data.to_excel(file_name, index=False)


def PointerValueRangeFunc(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value0, value1, daygap, value_range_list2):
    # XDataList1, XDataListOutput1=XAxisFunc(day=1, starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
    # XDataList2, XDataListOutput2=XAxisFunc(day=2, starting_point=starting_point, starting_value=starting_value, rule_data=rule_data,  daygap=daygap, value_range_list2=value_range_list2)
    
    DataListXY1, DataListOutputXY1 = LeftXYAxisFunc(day=1, starting_point=starting_point, starting_value=starting_value, rule_data_x=rule_data_x, rule_data_y=rule_data_y, daygap=daygap, value_range_list2=value_range_list2)


    # YDataList1, YDataListOutput1=YAxisFunc(day=1, starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
    # YDataList2, YDataListOutput2=YAxisFunc(day=2, starting_point=starting_point, starting_value=starting_value, rule_data=rule_data,  daygap=daygap, value_range_list2=value_range_list2)
    
    DataListXY2, DataListOutputXY2 = LeftXYAxisFunc(day=2, starting_point=starting_point, starting_value=starting_value, rule_data_x=rule_data_x, rule_data_y=rule_data_y, daygap=daygap, value_range_list2=value_range_list2)


    return CombinationValue(value0, value1, DataListXY1, DataListXY2)


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
        # return Response({'status': status.HTTP_400_BAD_REQUEST, 'message':f'{err}'}, status=status.HTTP_400_BAD_REQUEST)


def SortedListFunc(l):
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            if l[i] > l[j]:
                l[i], l[j] = l[j], l[i]

    return l   

def PointerCalculation(starting_point, starting_value, rule_data, rule_data_x, rule_data_y, value_range_list2, dfList, count, SumList, daygap, first_run):
    
    DataList=[]
    DataList1=[]
    DataList2=[]
    DataList3=[]

    # X axis day1 and day2 XDataList and Length of range
    DataListXY1, DataListOutputXY1 = LeftXYAxisFunc(day=1, starting_point=starting_point, starting_value=starting_value, rule_data_x=rule_data_x, rule_data_y=rule_data_y, daygap=daygap, value_range_list2=value_range_list2)
    print("DataListXY1, DataListOutputXY1", DataListXY1, SortedListFunc(DataListOutputXY1))
    # XDataList1, XDataListOutput1=XAxisFunc(day=1, starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
    DataListXY2, DataListOutputXY2 = LeftXYAxisFunc(day=2, starting_point=starting_point, starting_value=starting_value, rule_data_x=rule_data_x, rule_data_y=rule_data_y, daygap=daygap, value_range_list2=value_range_list2)
    # print("DataListXY2, DataListOutputXY2", DataListXY2, SortedListFunc(DataListOutputXY2))
    # XDataList1, XDataListOutput1=XAxisFunc(day=1, starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
    # XDataList2, XDataListOutput2=XAxisFunc(day=2, starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
    

    # Y axis day1 and day2 YDataList and Length of range
    # YDataList1, YDataListOutput1=YAxisFunc(day=1, starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
    # YDataList2, YDataListOutput2=YAxisFunc(day=2, starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)

    # print("XDataList1", XDataList1)
    # print("YDataList1", YDataList1)

    # day1 = XDataListOutput1[::-1]+YDataListOutput1
    # day2 = XDataListOutput2[::-1]+YDataListOutput2
    day1 = SortedListFunc(DataListOutputXY1)
    day2 =  SortedListFunc(DataListOutputXY2)

    # # day1c= combination(day1[15:26])
    # # day2c= combination(day2[15:26])

    uniqueCombination=[]
    if first_run == "YES" or first_run == "Yes" or first_run == "yes":
        # uniqueCombination= UniqueCombination(day1[15:26], day2[15:26])
        uniqueCombination= UniqueCombination(day1, day2)
   
    for i in uniqueCombination:
        # actual point value
        # DataList1 = CombinationValue(i[0], i[1], XDataList1, YDataList1, XDataList2, YDataList2)
        DataList1 = CombinationValue(i[0], i[1], DataListXY1, DataListXY2)
        # max point value
        DataList2 = PointerValueRangeFunc(value_range_list2[0], starting_value, rule_data, rule_data_x, rule_data_y, i[0],  i[1], daygap, value_range_list2)
        # min point value
        DataList3 = PointerValueRangeFunc(value_range_list2[1], starting_value, rule_data, rule_data_x, rule_data_y, i[0],  i[1], daygap, value_range_list2)
        DataList = DataList1+DataList2+DataList3
        SList=[]
        Section={}

        # print("DataList", DataList)

        if len(DataList)!=0 and len(DataList)==3:
            sum_value1 = DataList[0]['data1']+DataList[0]['data2']
            sum_value2 = DataList[1]['data1']+DataList[1]['data2']-sum_value1
            sum_value3 = DataList[2]['data1']+DataList[2]['data2']-sum_value1
           
            # combinations point
            Section['d1lp1']=i[0]
            Section['d1rp1']=0
            Section['d2lp2']=i[1]
            Section['d3lp3']=0

            Section['point_id']=str(Section['d1lp1'])+str(Section['d1rp1'])+str(Section['d2lp2'])+str(Section['d3lp3'])+str(generate_unique_random_number())

            # Point 0, 1 and 2 output value
            Section['pv0']= DataList[0]['data1']
            Section['pv1']= 0
            Section['pv2']= DataList[0]['data2']
            Section['pv3']= 0

            Section['pv_max']= round(-sum_value2, 2)
            Section['pv_min']= round(-sum_value3, 2)

            # sum of point value 0, 1, 2 
            Section['actual_value']=  round(Section['pv0']+Section['pv1']+Section['pv2']+Section['pv3'], 2)

            Section['maxv']=round(sum_value2, 2)
            Section['minv']=round(sum_value3, 2)

            if len(Section)!=0:
                SumList.append(Section)
                Section={}
                DataList=[]

    df = pd.DataFrame(SumList)
    
    # print("527 df", df)
    maxv_value = []
    minv_value = []

    # net_value = (value_range_high-starting_point)-maxv
    for d1 in df['maxv']:
        maxv_value.append(round(d1-(value_range_list2[0]-starting_point), 2))

    # minv_value = (value_range_low-starting_point)-minv    
    for d2 in df['minv']:
        if d2 < 0:
            minv_value.append(round((value_range_list2[1]-starting_point)-d2, 2))
        elif d2>0:
            minv_value.append(round((value_range_list2[1]-starting_point)+d2, 2))
   
    df.insert(9, "maxv_net", maxv_value, True)
    df.insert(10, "minv_net", minv_value, True)

    # RangeSum = sum of maxv_value and minv_value
    df['RangeSum'] = round(abs(df['maxv_net']) + abs(df['minv_net']), 2)
    if first_run == "YES" or first_run == "Yes" or first_run == "yes":
        df['ActualP'] = 100
    # if first_run == "NO" or first_run == "No" or first_run == "no": 
    #     file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
    #     output_df = pd.read_excel(file_name1)
    #     exist_data = output_df['first_run'].iloc[0]
    #     if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
    #         df['ActualP'] = (((output_df['actual_value'].iloc[0]-df['actual_value'])/output_df['actual_value'].iloc[0])*100)
    df['MaxP'] = round(((df['maxv_net']/df['RangeSum'])*100), 2)
    df['MinP'] = round(((df['minv_net']/df['RangeSum'])*100), 2)
    
  
    # if first_run == "YES" or first_run == "Yes" or first_run == "yes":
    #     df1 = df[(abs(df['MaxP']) < 100) & (abs(df['MinP']) < 100)]
    #     df1 = df[(abs(df['MaxP']) < 100)]
    #     df2 = df1[(abs(df1['MinP']) < 100)]
    #     df3 = df2['MinP'].unique()
    #     df5 = pd.DataFrame()

    #     for d3 in df3:
    #         d1_point0=0
    #         d1_point1=0
    #         d2_point2=0
    #         count=0
    #         for index, row in df2.iterrows():
    #             if d3 == row['MinP']:
    #                 count+=1
    #                 if d1_point0 < row['d1_point0']:
    #                     d1_point0=row['d1_point0']
    #                 if d1_point1 < row['d1_point1']:
    #                     d1_point1=row['d1_point1']
    #                 if count==1:
    #                     d2_point2=row['d2_point2']
    #                 if d2_point2 > row['d2_point2']:
    #                     d2_point2=row['d2_point2']

    #         df4 = df2[(df2['d1_point0'] == d1_point0) & (df2['d1_point1'] == d1_point1) & (df2['d2_point2'] == d2_point2) & (df2['MinP'] == d3)]
    #         df5 = pd.concat([df5, df4], ignore_index=True)

       
    #     ExcelFileWrite(main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx', df5)
       
    #     main_df = pd.read_excel(main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx')
        
    #     return JsonConvertData(main_df), day1

    ExcelFileWrite(main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx', df)
      
    main_df = pd.read_excel(main_media_url+'/media/upload_file/investing/xlsx/raw_data_file.xlsx')
      
    return JsonConvertData(main_df), day1

