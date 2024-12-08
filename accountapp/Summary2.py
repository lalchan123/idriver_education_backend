

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






def combination(stuff):
    DataList=[]
    for i, combo in enumerate((combinations(stuff, 3)), 1):
        DataList.append(combo)
    return DataList   

def UniqueCombination(day1, day12, day2):
    Datalist=[]
    for m in day1:
        for k in day12:
            for j in day2:
                Datalist.append((m, k, j))
    return Datalist

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


def XAxisFuncLeft(day, starting_point, starting_value, rule_data, daygap, value_range_list2):
   
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
            Section['Side']="Left" 
            Section['Day']=day 
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
            Section['Side']="Left" 
            Section['Day']=day 
            if len(Section) !=0:
                DataList.append(Section)  
                Section={}  
                output_value1=starting_value1
                i+=1  
                DataListOutput.append(starting_point)

    return DataList, DataListOutput

def XAxisFuncRight(day, starting_point, starting_value, rule_data, daygap, value_range_list2):
   
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
        for diff_value in reversed(range(value_range_list2[1], starting_point_loop, 5)):
            diff_value_actual+=diff_value
            starting_point=diff_value
            Section['starting_point']=starting_point
            if i==1: 
                output_value= starting_value-rule_data['x01']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5  
            if i==2: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value  
                x_starting_point_value-=5  
            if i==3: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value  
                x_starting_point_value-=5    
            if i==4: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5     
            if i==5: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5 
            if i==6: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']-rule_data['x56']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==7: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']-rule_data['x56']-rule_data['x67']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==8: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']-rule_data['x56']-rule_data['x67']-rule_data['x78']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==9: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']-rule_data['x56']-rule_data['x67']-rule_data['x78']-rule_data['x89']
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
            Section['Side']="Right" 
            Section['Day']=day 
            if len(Section) !=0:
                DataList.append(Section)  
                Section={}  
                output_value1=starting_value1
                i+=1 
                DataListOutput.append(starting_point)

    if day == 2:
        starting_value=starting_value+starting_value*daygap
        
        for diff_value in reversed(range(value_range_list2[1], starting_point_loop, 5)):
            diff_value_actual+=diff_value
            starting_point=diff_value
            Section['starting_point']=starting_point
            if i==1: 
                output_value= starting_value-rule_data['x01']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5  
            if i==2: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value  
                x_starting_point_value-=5  
            if i==3: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value  
                x_starting_point_value-=5    
            if i==4: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value 
                x_starting_point_value-=5     
            if i==5: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==6: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']-rule_data['x56']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==7: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']-rule_data['x56']-rule_data['x67']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==8: 
                output_value= starting_value-rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']-rule_data['x56']-rule_data['x67']-rule_data['x78']
                starting_value1=output_value
                sum_value=diff_value_actual-output_value   
                x_starting_point_value-=5  
            if i==9: 
                output_value= starting_value+rule_data['x01']-rule_data['x12']-rule_data['x23']-rule_data['x34']-rule_data['x45']-rule_data['x56']-rule_data['x67']-rule_data['x78']-rule_data['x89']
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
            Section['Side']="Right" 
            Section['Day']=day 
            if len(Section) !=0:
                DataList.append(Section)  
                Section={}  
                output_value1=starting_value1
                i+=1  
                DataListOutput.append(starting_point)

    return DataList, DataListOutput


def YAxisFuncLeft(day, starting_point, starting_value, rule_data, daygap, value_range_list2):

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
            YSection['Side']="Left" 
            YSection['Day']=day 
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
            YSection['Side']="Left" 
            YSection['Day']=day 
            if len(YSection) !=0:
                YDataList.append(YSection)  
                YSection={}  
                output_value1=starting_value1
                yi+=1 
                YDataListOutput.append(starting_point)  


    return YDataList, YDataListOutput


def YAxisFuncRight(day, starting_point, starting_value, rule_data, daygap, value_range_list2):

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

        for diff_value in range(starting_point_loop, value_range_list2[0]+5, 5):
            diff_value_actual+=diff_value
            starting_point=diff_value
            YSection['starting_point']=starting_point

            if yi==0: 
                output_value= starting_value
                y_sum_value=0  
                y_starting_point_value=0
        
            if yi==1: 
                output_value= starting_value+rule_data['y01']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value
                y_starting_point_value+=5 
            if yi==2: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5  
            if yi==3: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5     
            if yi==4: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value   
                y_starting_point_value+=5   
            if yi==5: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==6: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']+rule_data['y56']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==7: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']+rule_data['y56']+rule_data['y67']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==8: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']+rule_data['y56']+rule_data['y67']+rule_data['y78']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==9: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']+rule_data['y56']+rule_data['y67']+rule_data['y89']
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
            YSection['Side']="Right" 
            YSection['Day']=day 
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
                output_value= starting_value+rule_data['y01']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value
                y_starting_point_value+=5 
            if yi==2: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5  
            if yi==3: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5     
            if yi==4: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value   
                y_starting_point_value+=5   
            if yi==5: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5  
            if yi==6: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']+rule_data['y56']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==7: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']+rule_data['y56']+rule_data['y67']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==8: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']+rule_data['y56']+rule_data['y67']+rule_data['y78']
                starting_value1=output_value
                y_sum_value=diff_value_actual-output_value 
                y_starting_point_value+=5   
            if yi==9: 
                output_value= starting_value+rule_data['y01']+rule_data['y12']+rule_data['y23']+rule_data['y34']+rule_data['y45']+rule_data['y56']+rule_data['y67']+rule_data['y89']
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
            YSection['Side']="Right" 
            YSection['Day']=day 
            if len(YSection) !=0:
                YDataList.append(YSection)  
                YSection={}  
                output_value1=starting_value1
                yi+=1 
                YDataListOutput.append(starting_point)  


    return YDataList, YDataListOutput





def XAxisFunc(day, starting_point, starting_value, rule_data, daygap):
   
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
       
        
        for diff_value in reversed(range(starting_point_loop-100, starting_point_loop, 5)):
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
        
        for diff_value in reversed(range(starting_point_loop-100, starting_point_loop, 5)):
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

    if day == 3:
        starting_value=starting_value+starting_value*daygap+6
        
        for diff_value in reversed(range(starting_point_loop-100, starting_point_loop, 5)):
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


def YAxisFunc(day, starting_point, starting_value, rule_data, daygap):

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

        for diff_value in range(starting_point_loop, starting_point_loop+100, 5):
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

        for diff_value in range(starting_point_loop, starting_point_loop+100, 5):
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

    if day == 3:
        starting_value=starting_value+starting_value*daygap+6

        for diff_value in range(starting_point_loop, starting_point_loop+100, 5):
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



def CombinationValue(value0, value1, value2, XDataList1, YDataList1, XDataList2, YDataList2, XDataList3, YDataList3):
    dfList=[]
    new_row={}

    x_data_day1 = [x for x in XDataList1 if x['starting_point'] == value0]
    y_data_day1 = [x for x in YDataList1 if x['starting_point'] == value0]

    data1=0
    data12=0
    data2=0

    if len(x_data_day1)!=0:
        data1=x_data_day1[0]['output_value']
    if len(y_data_day1)!=0:
        data1=y_data_day1[0]['output_value']

    x_data_day12 = [x for x in XDataList2 if x['starting_point'] == value1]
    y_data_day12 = [x for x in YDataList2 if x['starting_point'] == value1]
        
    if len(x_data_day12)!=0:
        data12=x_data_day12[0]['output_value']
    if len(y_data_day12)!=0:
        data12=y_data_day12[0]['output_value']

       
    x_data_day2 = [x for x in XDataList3 if x['starting_point'] == value2]
    y_data_day2 = [x for x in YDataList3 if x['starting_point'] == value2]
               
               
    if len(x_data_day2)!=0:
        data2=x_data_day2[0]['output_value']
    if len(y_data_day2)!=0:
        data2=y_data_day2[0]['output_value']


    new_row={
        "data1":data1, 
        "data12":data12, 
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


def PointerValueRangeFunc(starting_point, starting_value, rule_data, ValueList, daygap, value_range_list2):
    XDataListT1=[]    
    XDataListOutputT1=[]    
    YDataListT1=[]    
    YDataListOutputT1=[] 

    for dt in ValueList:    
        if dt['v_point'] == "Left":
            XDataList1, XDataListOutput1=XAxisFuncLeft(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
            YDataList1, YDataListOutput1=YAxisFuncLeft(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)

            XDataListT1= XDataListT1+XDataList1
            XDataListOutputT1= XDataListOutputT1+XDataListOutput1

            YDataListT1= YDataListT1+YDataList1
            YDataListOutputT1= YDataListOutputT1+YDataListOutput1

        if dt['v_point'] == "Right":
            XDataList1, XDataListOutput1= YAxisFuncRight(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
            YDataList1, YDataListOutput1= XAxisFuncRight(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)

            XDataListT1= XDataListT1+XDataList1
            XDataListOutputT1= XDataListOutputT1+XDataListOutput1

            YDataListT1= YDataListT1+YDataList1
            YDataListOutputT1= YDataListOutputT1+YDataListOutput1


    
    file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
    summary_df = pd.read_excel(file_name1)
    d1_point0, d1_point1, d2_point2, Left_Day, Left_Point, Right_Day, Right_Point = summary_df['d1_point0'].iloc[0], summary_df['d1_point1'].iloc[0], summary_df['d2_point2'].iloc[0], summary_df['Left_Day'].iloc[0], summary_df['Left_Point'].iloc[0], summary_df['Right_Day'].iloc[0], summary_df['Right_Point'].iloc[0] 


    TotalDataItem = XDataListT1+YDataListT1

    Data1 = [x for x in TotalDataItem if x['starting_point'] == d1_point0 and  x['Side'] == 'Left' and  x['Day'] == 1]
    Data2 = [x for x in TotalDataItem if x['starting_point'] == d1_point1 and  x['Side'] == 'Left' and  x['Day'] == 1]
    Data3 = [x for x in TotalDataItem if x['starting_point'] == d2_point2 and  x['Side'] == 'Left' and  x['Day'] == 2]
    Data4 = [x for x in TotalDataItem if x['starting_point'] == Left_Point and  x['Side'] == 'Left' and  x['Day'] == Left_Day]
    Data5 = [x for x in TotalDataItem if x['starting_point'] == Right_Point and  x['Side'] == 'Right' and  x['Day'] == Right_Day]
    Data6 = DuplicateRemove(Data1)+DuplicateRemove(Data2)+DuplicateRemove(Data3)+DuplicateRemove(Data4)+DuplicateRemove(Data5)
    return Data6


def DuplicateRemove(Data):
    DataList = []
    for m in range(len(Data)):
        if m == 0:
            DataList.append(Data[m])
        else:
            for k in DataList:
                if k['starting_point'] == Data[m]['starting_point'] and  k['Side'] == Data[m]['Side'] and k['Day'] == Data[m]['Day']:
                    pass
                else:
                    DataList.append(Data[m])   
    return DataList


def PVFunction(Data):
    try:
        data = Data[0]['output_value']
        return data
    except:
        return 0    

def MainPointerCalculation(starting_point, starting_value, rule_data, value_range_list2, SumList, daygap):
    file_name1 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
    summary_df = pd.read_excel(file_name1)
    d1_point0, d1_point1, d2_point2, Left_Day, Left_Point, Right_Day, Right_Point = summary_df['d1_point0'].iloc[0], summary_df['d1_point1'].iloc[0], summary_df['d2_point2'].iloc[0], summary_df['Left_Day'].iloc[0], summary_df['Left_Point'].iloc[0], summary_df['Right_Day'].iloc[0], summary_df['Right_Point'].iloc[0] 
    print("d1_point0 d1_point1 d2_point2 Left_Day Left_Point Right_Day Right_Point", d1_point0, d1_point1, d2_point2, Left_Day, Left_Point, Right_Day, Right_Point)
    uniqueCombination= [(d1_point0, d1_point1, d2_point2, Left_Point, Right_Point)]
    ValueList = []
    if len(str(d1_point0)) != 0:
        ValueList.append({
            'd1_point0': d1_point0,
            'v_day': 1,
            'v_point': "Left",
        })

    if len(str(d1_point1)) != 0:
        ValueList.append({
            'd1_point1': d1_point1,
            'v_day': 1,
            'v_point': "Left",
        })
    if len(str(d2_point2)) != 0:
        ValueList.append({
            'd2_point2': d2_point2,
            'v_day': 2,
            'v_point': "Left",
        })
    if len(str(Left_Point)) != 0:
        ValueList.append({
            'Left_Point': Left_Point,
            'v_day': Left_Day,
            'v_point': "Left",
        })

    if len(str(Right_Point)) != 0:
        ValueList.append({
            'Right_Point': Right_Point,
            'v_day': Right_Day,
            'v_point': "Right",
        })

    XDataListT1=[]    
    XDataListOutputT1=[]    
    YDataListT1=[]    
    YDataListOutputT1=[] 



    for dt in ValueList:
      
        if dt['v_point'] == "Left":
            XDataList1, XDataListOutput1=XAxisFuncLeft(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
            YDataList1, YDataListOutput1=YAxisFuncLeft(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)

            XDataListT1= XDataListT1+XDataList1
            XDataListOutputT1= XDataListOutputT1+XDataListOutput1

            YDataListT1= YDataListT1+YDataList1
            YDataListOutputT1= YDataListOutputT1+YDataListOutput1

        if dt['v_point'] == "Right":
            XDataList1, XDataListOutput1= YAxisFuncRight(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)
            YDataList1, YDataListOutput1= XAxisFuncRight(day=dt['v_day'], starting_point=starting_point, starting_value=starting_value, rule_data=rule_data, daygap=daygap, value_range_list2=value_range_list2)

            XDataListT1= XDataListT1+XDataList1
            XDataListOutputT1= XDataListOutputT1+XDataListOutput1

            YDataListT1= YDataListT1+YDataList1
            YDataListOutputT1= YDataListOutputT1+YDataListOutput1



    SList=[]
    Section={}

    Section['starting_point']=starting_point
    Section['starting_value']=starting_value
    Section['daygap']=daygap
    Section['value_range_0']=value_range_list2[0]
    Section['value_range_1']=value_range_list2[1]
    Section['created_time']=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    Section['d1_point0']=d1_point0
    Section['d1_point1']=d1_point1
    Section['d2_point2']=d2_point2

    TotalDataItem = XDataListT1+YDataListT1
    Data1 = [x for x in TotalDataItem if x['starting_point'] == d1_point0 and  x['Side'] == 'Left' and  x['Day'] == 1]
    Data2 = [x for x in TotalDataItem if x['starting_point'] == d1_point1 and  x['Side'] == 'Left' and  x['Day'] == 1]
    Data3 = [x for x in TotalDataItem if x['starting_point'] == d2_point2 and  x['Side'] == 'Left' and  x['Day'] == 2]
    Data4 = [x for x in TotalDataItem if x['starting_point'] == Left_Point and  x['Side'] == 'Left' and  x['Day'] == Left_Day]
    Data5 = [x for x in TotalDataItem if x['starting_point'] == Right_Point and  x['Side'] == 'Right' and  x['Day'] == Right_Day]
    

    
    Section['pv0']= PVFunction(Data1)
    Section['pv1']= PVFunction(Data2)
    Section['pv2']= PVFunction(Data3)
    Section['actual_value']=  Section['pv0']+Section['pv1']+Section['pv2']+PVFunction(Data4)-PVFunction(Data5)


    
    DataList2 = PointerValueRangeFunc(value_range_list2[0], starting_value, rule_data, ValueList, daygap, value_range_list2)
    DataList3 = PointerValueRangeFunc(value_range_list2[1], starting_value, rule_data, ValueList, daygap, value_range_list2)
    
   
    LeftSumMax=0
    RightSumMax=0
    for h in DataList2:
        if h['Side'] == 'Left':
            LeftSumMax+=h['output_value']
        if h['Side'] == 'Right':
            RightSumMax+=h['output_value']
            
    Section['maxv']=LeftSumMax-RightSumMax

    LeftSumMin=0
    RightSumMin=0
    for h in DataList3:
        if h['Side'] == 'Left':
            LeftSumMin+=h['output_value']
        if h['Side'] == 'Right':
            RightSumMin+=h['output_value']
            
    Section['minv']=LeftSumMin-RightSumMin
    Section['maxv_value']=((value_range_list2[0]-starting_point)-Section['maxv'])
    Section['minv_value']=((value_range_list2[1]-starting_point)-Section['minv'])
    Section['remarks']="sum_max_value"
    Section['first_run']="No"
    Section['RangeSum']=Section['maxv_value'] + Section['minv_value']

    file_name1 = main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
    output_df = pd.read_excel(file_name1)
    exist_data = output_df['first_run'].iloc[0]
    if exist_data == "YES" or exist_data == "Yes" or exist_data == "yes":
        Section['ActualP'] = (((output_df['actual_value'].iloc[0]-Section['actual_value'])/output_df['actual_value'].iloc[0])*100)

    Section['MaxP'] = round(((Section['maxv_value']/Section['RangeSum'])*100), 2)
    Section['MinP'] = round(((Section['minv_value']/Section['RangeSum'])*100), 2)
    Section['Left_Day'] = Left_Day
    Section['Left_Point'] = Left_Point
    Section['Left_pv'] = PVFunction(Data4)
    Section['Right_Day'] = Right_Day
    Section['Right_Point'] = Right_Point
    Section['Right_pv'] = PVFunction(Data5)

    SList.append(Section)

    df = pd.DataFrame(SList)

    ExcelFileWrite(main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx', df)

    file_name2 =  main_media_url+'/media/upload_file/investing/xlsx/summay_data_file.xlsx'
    summary_df2 = pd.read_excel(file_name2)
    return JsonConvertData(summary_df2)

    


